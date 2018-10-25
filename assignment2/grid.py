from sklearn.model_selection import GridSearchCV
import pandas as pd
import GTB
from sklearn import model_selection
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from xgboost import XGBClassifier
import lightgbm as lgb
import preprocess

if __name__ == '__main__':

    train_data = pd.read_csv("./data/trainFeatures.csv")
    train_data = preprocess.feature_eng(train_data)
    label = pd.read_csv("./data/trainLabels.csv", header=None)

#pass parameters range in to GridSearchCV so it can test automatically
    parameters_xgb = {'n_estimators': list(range(500,2501,100)), 'learning_rate': [0.01, 0.02, 0.05, 0.1, 0.2, 0.3], 'max_depth':list(range(3,15,2)), 'min_child_weight': list(range(1,10,2))}

    xgb = XGBClassifier()
    lgbm = lgb.LGBMClassifier(boosting_type='gbdt', n_estimators=3000)
    clf_xgb = GridSearchCV(xgb, parameters_xgb)
    clf_xgb.fit(train_data, label[0].values)
#output the best parameters
    print('xgb: ', clf_xgb.best_params_)
