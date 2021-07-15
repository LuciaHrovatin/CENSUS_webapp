from io import StringIO
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import datetime
import redis
from saver import MySQLManager

# password = "luca0405" # change with your password
# password = "Pr0tett0.98"
# saver = MySQLManager(host="localhost",
#                         port=3306,
#                         user="root",
#                         password=password,
#                         database = "project_bdt")
#
#
# # For REDIS training
# # 1 and 2
# #df = saver.execute_read_query(table_name="final")
#
# # 3 and 4
# df = saver.execute_read_query(table_name="final_individual")
#
#
# #train - test splitting procedure
# X_train, X_test, y_train, y_test = train_test_split(df, np.array([x for x in df[df.shape[1]-1]]), test_size=0.40, random_state=1)
#
# # for 1 and 3
# #X_train = X_train.drop([0, 1, 3, 8, 9, 10], axis=1)
# #X_train = X_train.to_numpy()
#
# # for 2 and 4
# X_train = X_train.drop([0, 1, 3, 4, 8, 9, 10], axis=1)
# X_train = X_train.to_numpy()
#
#
# #X_test = X_test.drop([0, 1, 3, 8, 9, 10], axis=1)
# #X_test = X_test.to_numpy()
#
# # # ---------------------------------------------- KNN ---------------------------------------
# # print("KNN: ")
# # clf = KNN(n_neighbors=5)
# # clf.fit(X_train, y_train)
# # print(clf.score(X_test, y_test))
#
#
# # choosing the best max_depth
# # for i in range(1, 10):
# #     cl_tree = DecisionTreeClassifier(max_depth=i, random_state=0)
# #     cl_tree.fit(X_train, y_train)
# #     print(cl_tree.score(X_test, y_test), i)
#
#
# # Decision tree training
# cl_tree = DecisionTreeClassifier(max_depth=8, random_state=0)
# cl_tree.fit(X_train, y_train)
# t_nodes = cl_tree.tree_.node_count
# t_left = cl_tree.tree_.children_left
# t_right = cl_tree.tree_.children_right
# t_feature = cl_tree.tree_.feature
# t_threshold = cl_tree.tree_.threshold
# t_value = cl_tree.tree_.value
# feature_names = df.columns.values
#
# # create a buffer to build up our command
# forrest_cmd = StringIO()
# # Case 1
# #forrest_cmd.write("ML.FOREST.ADD census:tree 0 ")
#
# # Case 2
# #forrest_cmd.write("ML.FOREST.ADD census_nosex:tree 0 ")
#
# # Case 3 (switch dataset)
# #forrest_cmd.write("ML.FOREST.ADD census_individuals:tree 0 ")
#
# # Case 4
# forrest_cmd.write("ML.FOREST.ADD census_ind_nosex:tree 0 ")
#
# # Traverse the tree starting with the root and a path of “.”
# stack = [(0, ".")]
#
# while len(stack) > 0:
#     node_id, path = stack.pop()
#
#     if t_left[node_id] != t_right[node_id]:
#         stack.append((t_right[node_id], path + "r"))
#         stack.append((t_left[node_id], path + "l"))
#         cmd = "{} NUMERIC {} {} ".format(path, feature_names[t_feature[node_id]], t_threshold[node_id])
#         forrest_cmd.write(cmd)
#
#     else:
#         cmd = "{} LEAF {} ".format(path, np.argmax(t_value[node_id]))
#         forrest_cmd.write(cmd)
#
# # execute command in Redis
# r = redis.Redis("localhost", 6380)
# r.execute_command(forrest_cmd.getvalue())
#
#
# def RandomForest(saver: MySQLManager, ncomp : int, sex: int, age: int, statciv: int, place: int):
#     i = datetime.datetime.now()
#     table = "final"
#     # If a person is less than 18 years old, he/she will not have a REDDITO!  --> ritornare 1 o 0
#     if (i.year - age) <= 18:
#         return 1
#
#     # If statciv is 1, then the dataset containing the individual census data will be considered
#     if statciv == 1:
#         table = "final_individual"
#
#     df = saver.execute_read_query(table_name=table)
#     y_train = np.array([x for x in df[df.shape[1] - 1]])
#
#     # If the choice was "Preferisco non dirlo" then, data will not include "sex" information
#     if not sex:
#         X_train = df.drop([0, 1, 3, 4, 8], axis=1)
#     else:
#         X_train = df.drop([0, 1, 3, 8], axis=1)
#     X_train = X_train.to_numpy()
#     clf = RandomForestClassifier(max_depth=6, random_state=1, bootstrap=True)
#     clf.fit(X_train, y_train)
#     if not sex:
#         return print(clf.predict([[ncomp, age, statciv, place]]))
#     result = clf.predict([[ncomp, sex, age, statciv, place]])[0]
#     return int(result)
#
