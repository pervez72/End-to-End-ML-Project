import os
import sys
from dataclasses import dataclass

# === ML & Metrics Libraries ===
from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

# === Custom Project Modules ===
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object, evaluate_models


# ===========================================
# ১️⃣ ModelTrainerConfig → Configuration Class
# ===========================================
# এই dataclass শুধু model save করার path রাখবে।
@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


# ===========================================
# ২️⃣ ModelTrainer → Core Model Training Class
# ===========================================
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()  # config object initialize

    def initiate_model_trainer(self, train_array, test_array):
        """
        ✅ This function trains multiple ML models, compares performance,
        and saves the best model.
        """
        try:
            logging.info("🔹 Splitting training and testing input data")

            # -------- Step 1: Separate features and target --------
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            # -------- Step 2: Define ML Models --------
            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoosting Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            # -------- Step 3: Define Hyperparameter Grid --------
            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                },
                "Random Forest": {
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'subsample': [0.6, 0.7, 0.8, 0.9],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    'learning_rate': [0.1, 0.01, 0.05, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                },
                "CatBoosting Regressor": {
                    'depth': [6, 8, 10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor": {
                    'learning_rate': [0.1, 0.01, 0.5, 0.001],
                    'n_estimators': [8, 16, 32, 64, 128, 256]
                }
            }

            # -------- Step 4: Evaluate All Models --------
            logging.info("🚀 Model training & evaluation started")

            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params
            )

            # -------- Step 5: Find the Best Model --------
            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            logging.info(f"🏆 Best Model Found: {best_model_name} (Score: {best_model_score:.4f})")

            # -------- Step 6: Threshold Check --------
            if best_model_score < 0.6:
                raise CustomException("❌ No suitable model found with acceptable accuracy")

            # -------- Step 7: Save the Best Model --------
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            logging.info(f"✅ Model saved successfully at: {self.model_trainer_config.trained_model_file_path}")

            # -------- Step 8: Evaluate on Test Data --------
            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)

            logging.info(f"🎯 Final R2 Score on Test Data: {r2_square:.4f}")
            return r2_square

        except Exception as e:
            raise CustomException(e, sys)
