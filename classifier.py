# TODO #
# Primo tentativo di implementazione dei modelli.
# 1. Creare un data-lake da cui prendersi direttamente i dati...fare il passaggio tramite SQL risulta VERBOSO

import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis as QDA
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.model_selection import train_test_split
import datetime

from saver import MySQLManager

# password = "luca0405" # change with your password
# password = "Pr0tett0.98"
# saver = MySQLManager(host="localhost",
#                        port=3306,
#                        user="root",
#                        password=password,
#                        database = "project-bdt")


#df = saver.execute_read_query(table_name="final")

# train - test splitting procedure
# X_train, X_test, y_train, y_test = train_test_split(df, np.array([x for x in df[df.shape[1]-1]]), test_size=0.40, random_state=1)
# #
# last = df.shape[1]-1
# X_train = X_train.drop([0, 1, 3, 8, 9, 10], axis=1)
# X_train = X_train.to_numpy()
#
# X_test = X_test.drop([0, 1, 3, 8, 9, 10], axis=1)
# X_test = X_test.to_numpy()
#
# print(X_train.shape, X_test.shape)
#
# # --------------------------------------------- LDA ----------------------------------------
#
# print("LDA: ")
# clf = LDA()
# clf.fit(X_train, y_train)
# print(clf.score(X_test, y_test)) # mean accuracy
#
# #---------------------------------------------- QDA ----------------------------------------
#
# print("QDA: ")
# clf = QDA()
# clf.fit(X_train, y_train)
# print(clf.score(X_test, y_test)) # mean accuracy
#
# # ---------------------------------------------- KNN ---------------------------------------
#
# print("KNN: ")
# clf = KNN(n_neighbors=5)
# clf.fit(X_train, y_train)
# print(clf.score(X_test, y_test))
#
#
# # ---------------------------------------------- RandomForests -----------------------------
#
# print("Random Forests: ")
# clf = RandomForestClassifier(max_depth=6, random_state=1, bootstrap=True)
# clf.fit(X_train, y_train)
# print(clf.score(X_test, y_test)) # mean accuracy
#
# # -------------------------


def RandomForest(saver: MySQLManager, ncomp : int, sex: int, age: int, statciv: int, place: int):
    i = datetime.datetime.now()
    table = "final"
    # If a person is less than 18 years old, he/she will not have a REDDITO!  --> ritornare 1 o 0
    if (i.year - age) <= 18:
        return 1.0

    # If statciv is 1, then the dataset containing the individual census data will be considered
    if statciv == 1:
        table = "final_individual"

    df = saver.execute_read_query(table_name=table)
    y_train = np.array([x for x in df[df.shape[1] - 1]])

    # If the choice was "Preferisco non dirlo" then, data will not include "sex" information
    if not sex:
        X_train = df.drop([0, 1, 3, 4, 8, 9, 10], axis=1)
    else:
        X_train = df.drop([0, 1, 3, 8, 9, 10], axis=1)
    X_train = X_train.to_numpy()
    print("Random Forests internal function: ")
    clf = RandomForestClassifier(max_depth=6, random_state=1, bootstrap=True)
    clf.fit(X_train, y_train)
    if not sex:
        return print(clf.predict([[ncomp, age, statciv, place]]))
    result = clf.predict([[ncomp, sex, age, statciv, place]])[0]
    return int(result)

#print(type(RandomForest(saver, 2, 1, 1968, 3, 4)))