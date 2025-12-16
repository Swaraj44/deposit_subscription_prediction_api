from config.feature_engineering import feature_engineering, identify_feature_types,ENCODER
from sklearn.preprocessing import LabelEncoder


def data_process_for_pred(X):
  X_fe = feature_engineering(X)
  cat_cols, num_cols = identify_feature_types(X_fe)

  for c in cat_cols:                                    # missing values handling
    X_fe[c] = X_fe[c].fillna("missing").astype(str)

  for n in num_cols:
    X_fe[n] = X_fe[n].fillna(X_fe[n].median())

  X_enc = ENCODER(X_fe)                                 # encode for RF


  return X_fe, X_enc