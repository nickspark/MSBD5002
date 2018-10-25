import pandas as pd

def is_number(s):
# to judge whether the feature value is integer
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def feature_eng(data):
#build two feature values together to create a new feature
    data['isHusband'] = 0
    data.loc[data['relationship'] == ' Husband', 'isHusband'] = 1
    data.loc[data['Marital-status'] == ' Married-civ-spouse', 'isHusband'] = 1

#if feature value is not interger, factorize it
    for name in data.columns:

        if (is_number(data[name].values[1]) != True):
            data[name] = pd.factorize(data[name].values)[0] + 1
        else:
            data[name] += 1

    return data