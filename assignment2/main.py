import pandas as pd
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
import lightgbm as lgb
import xgboost as xgb
from xgboost import XGBClassifier

import preprocess


def f(str):
    if '>' in str:
        return 1
    else:
        return 0


if __name__ == '__main__':
#read the data
    train_data = pd.read_csv("./data/trainFeatures.csv")
    label = pd.read_csv("./data/trainLabels.csv", header=None)
    test_data = pd.read_csv('./data/testFeatures.csv')
    len_train = len(train_data)
#put the traninset and the testset together to factorize and then split them
    data = preprocess.feature_eng(train_data.append(test_data, ignore_index=True))
    train_data = data[:len_train]
    test_data = data[len_train:]
#model used
    clf = XGBClassifier(n_estimators=1000)
    clf1 = RandomForestClassifier(n_estimators=500)
    clf2 = BaggingClassifier(KNeighborsClassifier(), max_samples=0.5, max_features=0.5)
    clf3 = AdaBoostClassifier(n_estimators=2000)
    clf4 = GradientBoostingClassifier(n_estimators=1000)
    clf5 = ExtraTreesClassifier(n_estimators=1000)
    clf6 = lgb.LGBMClassifier(boosting_type='gbdt', n_estimators=2000)
    eclf = VotingClassifier(estimators=[('rf', clf1), ('bagging', clf2), ('adab', clf3), ('gtb', clf4)], voting='soft', weights=[2,1,2,2])
    # kf = model_selection.KFold(n_splits=10, shuffle=False, random_state=1)
    # scores = model_selection.cross_val_score(clf, train_data, label, cv=kf)
    # print('XGB:', scores.mean())
    # scores = model_selection.cross_val_score(clf1, train_data, label, cv=kf)
    # print('RF:', scores.mean())
    # scores = model_selection.cross_val_score(clf2, train_data, label, cv=kf)
    # print('bagging:', scores.mean())
    # scores = model_selection.cross_val_score(clf3, train_data, label, cv=kf)
    # print('ada:', scores.mean())
    # scores = model_selection.cross_val_score(clf4, train_data, label, cv=kf)
    # print('GTB:', scores.mean())
    # scores = model_selection.cross_val_score(clf5, train_data, label, cv=kf)
    # print('ET:', scores.mean())
    # scores = model_selection.cross_val_score(clf6, train_data, label, cv=kf)
    # print('lgbm:', scores.mean())
#train    
    clf.fit(train_data,label)
    predicted = clf.predict(test_data)
    df = pd.DataFrame(predicted)
    print(df)
    df.to_csv('./data/A2_zwangec_20550960_prediction.csv', index = 0, header = 0)

