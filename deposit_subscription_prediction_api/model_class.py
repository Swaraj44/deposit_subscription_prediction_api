class AdvancedBankMarketingPredictor:

    def __init__(self):
        self.models = {}               
        self.label_encoders = {}      
        self.categorical_features = [] 
        self.best_threshold = 0.5


    def predict_proba(self, X, X_enc):
        """
        Param:
        X :(pd.DataFrame)     raw input features (for CatBoost)
        X_enc :(pd.DataFrame) label-encoded features (for RandomForest)

        Ret:
             (np.ndarray)    ensemble probability for positive class
        """
        cb_proba = self.models["catboost"].predict_proba(X)[:, 1]
        rf_proba = self.models["random_forest"].predict_proba(X_enc)[:, 1]


        return 0.5 * cb_proba + 0.5 * rf_proba

 
    def predict(self, X, X_enc):
        proba = self.predict_proba(X, X_enc)
        return (proba >= self.best_threshold).astype(int)
