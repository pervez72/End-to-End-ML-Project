# ======================================
# 📦 Import Required Libraries
# ======================================

import sys
import os
import pandas as pd
from src.exception import CustomException  # Custom exception class for better error handling
from src.utils import load_object          # Utility function to load saved model/preprocessor objects


# ======================================
# 🔮 PredictPipeline Class
# ======================================
class PredictPipeline:
    """
    This class handles the prediction workflow:
    1. Loads the pre-trained model and preprocessor.
    2. Transforms input data using the preprocessor.
    3. Runs predictions using the trained model.
    """

    def __init__(self):
        # No initialization needed for now
        pass

    def predict(self, features):
        """
        Run predictions on the provided input features.

        Parameters:
        -----------
        features : pandas.DataFrame
            The user input data (structured as DataFrame) to be predicted.

        Returns:
        --------
        preds : numpy.ndarray
            The predicted output from the trained ML model.
        """
        try:
            # -------------------------------
            # 1️⃣ Define paths to model files
            # -------------------------------
            model_path = os.path.join("artifacts", "model.pkl")  # trained model
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")  # preprocessor (encoder, scaler, etc.)

            # -------------------------------
            # 2️⃣ Load model and preprocessor
            # -------------------------------
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            # -------------------------------
            # 3️⃣ Preprocess input features
            # -------------------------------
            data_scaled = preprocessor.transform(features)

            # -------------------------------
            # 4️⃣ Make predictions
            # -------------------------------
            preds = model.predict(data_scaled)

            # Return prediction results
            return preds

        except Exception as e:
            # Raise a custom exception with detailed traceback info
            raise CustomException(e, sys)



# ======================================
# 📊 CustomData Class
# ======================================
class CustomData:
    """
    This class structures raw user input (from HTML form)
    into a proper pandas DataFrame format for model prediction.
    """

    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int
    ):
        """
        Initialize input features provided by the user.

        Each parameter represents a feature used in the ML model.
        """
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_course
        self.reading_score = reading_score
        self.writing_score = writing_score


    def get_data_as_data_frame(self):
        """
        Converts the user input into a pandas DataFrame
        so it can be directly passed into the ML pipeline.

        Returns:
        --------
        pandas.DataFrame
            A single-row DataFrame with the input features.
        """
        try:
            # Create dictionary of input data
            custom_data_input_dict = {
                "gender": [self.gender],
                "race_ethnicity": [self.race_ethnicity],
                "parental_level_of_education": [self.parental_level_of_education],
                "lunch": [self.lunch],
                "test_preparation_course": [self.test_preparation_course],
                "reading_score": [self.reading_score],
                "writing_score": [self.writing_score],
            }

            # Convert to DataFrame
            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            # If something goes wrong, raise a custom error
            raise CustomException(e, sys)
