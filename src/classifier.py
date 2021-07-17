from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from io import StringIO
from typing import Optional
import numpy as np
import redis
from saver import MySQLManager


def redis_training(table: str, saver: MySQLManager, case: int, no_sex: Optional[bool] = False):
    df = saver.execute_read_query(table_name=table)

    y_train = np.array([x for x in df.iloc[:, df.shape[1] - 1]])

    columns_to_exclude = [0, 2, 7]

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


    # create a buffer to build the Redis command
    forrest_cmd = StringIO()

    if case == 1:
        forrest_cmd.write("ML.FOREST.ADD census:tree 0 ")
    elif case == 2:
        forrest_cmd.write("ML.FOREST.ADD census_nosex:tree 0 ")
    elif case == 3:
        forrest_cmd.write("ML.FOREST.ADD census_individuals:tree 0 ")
    else:
        forrest_cmd.write("ML.FOREST.ADD census_ind_nosex:tree 0 ")

    # Traverse the tree starting with the root and a path of “.”
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

    # execute command in Redis
    r = redis.StrictRedis(host="localhost", port=6380)
    r.execute_command(forrest_cmd.getvalue())

# choosing the best max_depth
# for i in range(1, 10):
#     cl_tree = DecisionTreeClassifier(max_depth=i, random_state=0)
#     cl_tree.fit(X_train, y_train)
#     print(cl_tree.score(X_test, y_test), i)

def redis_prediction(x_to_predict, key_tree: str) -> int:
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

    X_test = [[ncomp, sex, age, statciv, place]]

    # If statciv is 1, then the dataset containing the individual census data will be considered
    if statciv == 1:
        if not sex:
            X_test = [[ncomp, age, statciv, place]]
            return redis_prediction(X_test, "census_ind_nosex")
        return redis_prediction(X_test, "census_individuals")

    # If the choice was "Preferisco non dirlo" then, data will not include "sex" information
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
