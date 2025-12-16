import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def identify_feature_types(X):
    categorical = []
    numerical = []

    for col in X.columns:
        if X[col].dtype == 'object' or X[col].dtype == 'bool':
            categorical.append(col)
        else:
            if X[col].nunique() < 10 and col not in ['age', 'balance', 'duration', 'campaign']:
                categorical.append(col)
            else:
                numerical.append(col)

    return categorical, numerical

 
    
def feature_engineering(X, is_training=True):
    X_fe = X.copy()

    for col in X_fe.columns:                                                    # category -> string
        if X_fe[col].dtype.name == 'category':
            X_fe[col] = X_fe[col].astype(str)



    if 'pdays' in X_fe.columns:
        X_fe['was_contacted'] = (X_fe['pdays'] != -1).astype(int)

        X_fe['days_since_contact'] = X_fe['pdays'].replace(-1, 999)

        X_fe['recent_contact'] = (X_fe['pdays'].between(0, 7)).astype(int)


    if 'previous' in X_fe.columns:
        X_fe['has_previous_contact'] = (X_fe['previous'] > 0).astype(int)

        X_fe['previous_contact_category'] = pd.cut(
            X_fe['previous'],
            bins=[-1, 0, 1, 3, 100],
            labels=['none', 'once', 'few', 'many']
        ).astype(str)



    if 'balance' in X_fe.columns:
        X_fe['balance_positive'] = (X_fe['balance'] > 0).astype(int)

        X_fe['balance_category'] = pd.cut(
            X_fe['balance'],
            bins=[-np.inf, 0, 500, 2000, np.inf],
            labels=['negative', 'low', 'medium', 'high']
        ).astype(str)

        X_fe['balance_log'] = np.sign(X_fe['balance']) * np.log1p(np.abs(X_fe['balance']))



    if 'housing' in X_fe.columns and 'loan' in X_fe.columns:
        housing_yes = (X_fe['housing'].astype(str).str.lower() == 'yes').astype(int)

        loan_yes = (X_fe['loan'].astype(str).str.lower() == 'yes').astype(int)

        X_fe['any_loan'] = ((housing_yes == 1) | (loan_yes == 1)).astype(int)

        X_fe['both_loans'] = ((housing_yes == 1) & (loan_yes == 1)).astype(int)



    if 'age' in X_fe.columns:
        X_fe['age_group'] = pd.cut(
            X_fe['age'],
            bins=[0, 25, 35, 45, 55, 65, 100],
            labels=['very_young', 'young', 'middle', 'mature', 'senior', 'elderly'] ).astype(str)

        X_fe['retirement_age'] = (X_fe['age'] >= 60).astype(int)



    if 'duration' in X_fe.columns:
        X_fe['duration_minutes'] = X_fe['duration'] / 60

        X_fe['long_call'] = (X_fe['duration'] > 300).astype(int)

        X_fe['short_call'] = (X_fe['duration'] < 100).astype(int)



    if 'campaign' in X_fe.columns:
        X_fe['campaign_category'] = pd.cut(
            X_fe['campaign'],
            bins=[0, 1, 2, 3, 100],
            labels=['first', 'second', 'third', 'many'] ).astype(str)

    
    if 'month' in X_fe.columns and 'age_group' in X_fe.columns:
        X_fe['month_age_interaction'] = X_fe['month'].astype(str) + "_" + X_fe['age_group'].astype(str)   #  month + age group

 
    if 'poutcome' in X_fe.columns and 'contact' in X_fe.columns:
        X_fe['contact_outcome'] = X_fe['contact'].astype(str) + "_" + X_fe['poutcome'].astype(str)        # Contact method & outcome

    return X_fe


def ENCODER(X):
        categorical_features, numerical=identify_feature_types(X)
        le_dict = {}
        X_encoded = X.copy()

        for col in categorical_features:
          le = LabelEncoder()
          X_encoded[col] = le.fit_transform(X[col].astype(str))
          le_dict[col] = le
        return X_encoded