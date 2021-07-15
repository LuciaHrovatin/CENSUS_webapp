import datetime
import numpy as np
import redis
#from training_classifier import feature_names


def redis_prediction(X_test, key_tree: str) -> int:

    r = redis.StrictRedis('localhost', 6380)
    r_pred = np.full(len(X_test), -1, dtype=int)

    for i, x in enumerate(X_test):
        cmd = "ML.FOREST.RUN {}:tree ".format(key_tree)

        # iterate over each feature in the test record to build up the
        # feature:value pairs
        for j, x_val in enumerate(x):
            cmd += "{}:{},"#.format(feature_names[j], x_val)

        cmd = cmd[:-1]
        r_pred[i] = int(r.execute_command(cmd))
    return r_pred[0]


def redis_classifier(ncomp : int, sex: int, age: int, statciv: int, place: int) -> int:
    i = datetime.datetime.now()
    # If a person is less than 18 years old, he/she will not have a REDDITO!  --> ritornare 1 o 0
    if (i.year - age) <= 18:
        return 1

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


