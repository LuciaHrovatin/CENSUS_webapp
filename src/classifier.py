from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from io import StringIO
from typing import Optional
import numpy as np
import redis
from src.saver import MySQLManager


def redis_training(table: str, saver: MySQLManager, case: int, no_sex: Optional[bool] = False):
    """
    Redis training phase. 4 different models can be trained modifying the input parameters.
    :param str table: name of the table to consider (either final or final_individual)
    :param MySQLManager saver: allows the connection to MySQL server
    :param int case: defines which model has to be trained
    :param bool no_sex: the default value is False, if set to True it trains models without the sex variable
    """
    df = saver.execute_read_query(table_name=table)

    y_train = np.array([x for x in df.iloc[:, df.shape[1] - 1]])

    columns_to_exclude = [0, 2, 7]

    # exclude the column that corresponds to "sex"
    if no_sex:
        columns_to_exclude.append(3)

    X_train = df.drop(columns_to_exclude, axis=1)

    # Decision tree training
    cl_tree = DecisionTreeClassifier(max_depth=8, random_state=0)
    cl_tree.fit(X_train, y_train)
    t_nodes = cl_tree.tree_.node_count
    t_left = cl_tree.tree_.children_left
    t_right = cl_tree.tree_.children_right
    t_feature = cl_tree.tree_.feature
    t_threshold = cl_tree.tree_.threshold
    t_value = cl_tree.tree_.value

    feature_names = X_train.columns.values

    # buffer to build the Redis command
    forrest_cmd = StringIO()

    if case == 1:
        forrest_cmd.write("ML.FOREST.ADD census:tree 0 ")
    elif case == 2:
        forrest_cmd.write("ML.FOREST.ADD census_nosex:tree 0 ")
    elif case == 3:
        forrest_cmd.write("ML.FOREST.ADD census_individual:tree 0 ")
    elif case == 4:
        forrest_cmd.write("ML.FOREST.ADD census_ind_no_sex:tree 0 ")

    # traverse the tree
    stack = [(0, ".")]

    while len(stack) > 0:
        node_id, path = stack.pop()

        if t_left[node_id] != t_right[node_id]:
            stack.append((t_right[node_id], path + "r"))
            stack.append((t_left[node_id], path + "l"))
            cmd = "{} NUMERIC {} {} ".format(path, feature_names[t_feature[node_id]], t_threshold[node_id])
            forrest_cmd.write(cmd)
        else:
            cmd = "{} LEAF {} ".format(path, np.argmax(t_value[node_id]))
            forrest_cmd.write(cmd)
    print(forrest_cmd.getvalue())
    # execute command in Redis
    r = redis.StrictRedis(host="localhost", port=6380)
    r.execute_command(forrest_cmd.getvalue())



def redis_prediction(x_to_predict, key_tree: str) -> int:
    """
    This function returns a prediction of the income bracket of an individual or household
    :param x_to_predict: array of new data entered by the user
    :param str key_tree: key of the ML trained model stored on Redis server
    :return: the predicted Irpef income group
    """
    feature_names = list(range(0, len(x_to_predict[0])))

    r = redis.StrictRedis(host="localhost", port=6380)
    r_pred = np.full(len(x_to_predict), -1, dtype=int)

    for i, x in enumerate(x_to_predict):
        cmd = "ML.FOREST.RUN {}:tree ".format(key_tree)
        # iterate over each feature in the test record to build up the feature:value pairs
        for j, x_val in enumerate(x):
            cmd += "{}:{},".format(feature_names[j], x_val)

        cmd = cmd[:-1]
        r_pred[i] = int(r.execute_command(cmd))
    return r_pred[0]


def redis_classifier(ncomp: int, sex: int, age: int, statciv: int, place: int) -> int:
    """
    This function recalls the appropriate trained ML model depending on the input parameters
    :param int ncomp: number of components per family
    :param int sex: sex of the respondent
    :param int age: year of birth of the respondent
    :param int statciv: marital status of the respondent
    :param int place: region of residence
    :return: predicted Irpef income group
    """
    X_test = [[ncomp, sex, age, statciv, place]]

    # If statciv is 1, then the dataset containing the individual census data will be considered
    if statciv == 1:
        if not sex:
            X_test = [[ncomp, age, statciv, place]]
            return redis_prediction(X_test, "census_ind_no_sex")
        return redis_prediction(X_test, "census_individual")

    # If the choice was "Preferisco non specificare" then, data will not include "sex" information
    if not sex:
        X_test = [[ncomp, age, statciv, place]]
        return redis_prediction(X_test, "census_nosex")
    return redis_prediction(X_test, "census")


def random_forest(ncomp: int, sex: int, age: int, statciv: int, place: int) -> int:
    """
    This function has been implemented in the web interface hosted on Pythonanywhere
    :param int ncomp: number of components per family
    :param int sex: sex of the respondent
    :param int age: year of birth of the respondent
    :param int statciv: marital status of the respondent
    :param int place: region of residence
    :return: predicted Irpef income group
    """
    saver = MySQLManager(host="localhost",
                         port=3310,
                         user="root",
                         password="password",
                         database="project_bdt")
    table = "final"

    # If statciv is 1, then the dataset containing the individual census data will be considered
    if statciv == 1:
        table = "final_individual"

    df = saver.execute_read_query(table_name=table)
    y_train = np.array([x for x in df.iloc[:, df.shape[1] - 1]])

    # If the choice was "Preferisco non dirlo" then, data will not include "sex" information
    if not sex:
        X_train = df.drop(["nquest", "nord", "sex", "y"], axis=1)
    else:
        X_train = df.drop(["nquest", "nord", "y"], axis=1)
    X_train = X_train.to_numpy()
    clf = RandomForestClassifier(max_depth=6, random_state=1, bootstrap=True)

    # train the model
    clf.fit(X_train, y_train)

    # return the prediction on the new data
    if not sex:
        return int(clf.predict([[ncomp, age, statciv, place]])[0])

    return int(clf.predict([[ncomp, sex, age, statciv, place]])[0])
