# ------------------ Import Section ------------------
import sys
from dataclasses import dataclass
import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from src.exception import CustomException
from src.logger import logging
import os
from src.utils import save_object

# ------------------ Data Transformation Configuration ------------------
@dataclass
class DataTransformationConfig:
    # artifacts ফোল্ডারের মধ্যে preprocessor object সংরক্ষণ করা হবে
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")


# ------------------ Data Transformation Class ------------------
class DataTransformation:
    def __init__(self):
        # config initialize করা হচ্ছে
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self):
        '''
        এই function টি data transformation-এর জন্য preprocessing pipeline তৈরি করে।
        Numerical এবং Categorical data আলাদা করে handle করা হয়।
        '''
        try:
            # Numerical এবং Categorical columns আলাদা করা
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course",
            ]

            # -------- Numerical Pipeline --------
            # Step 1: Missing value handle (median দিয়ে)
            # Step 2: Standard scaling
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            # -------- Categorical Pipeline --------
            # Step 1: Missing value handle (most_frequent দিয়ে)
            # Step 2: OneHotEncoding (category → numeric)
            # Step 3: Scaling (mean=False → sparse matrix support করে)
            cat_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scaler", StandardScaler(with_mean=False))
                ]
            )

            # Log columns info
            logging.info(f"Categorical columns: {categorical_columns}")
            logging.info(f"Numerical columns: {numerical_columns}")

            # -------- Combine both pipelines --------
            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns),
                    ("cat_pipeline", cat_pipeline, categorical_columns)
                ]
            )

            return preprocessor
        
        except Exception as e:
            # Custom Exception raise করা হচ্ছে যদি কিছু error হয়
            raise CustomException(e, sys)
        

    def initiate_data_transformation(self, train_path, test_path):
        '''
        এই function টি পুরো data transformation process handle করে।
        Train/Test data পড়া, preprocessing apply করা, এবং preprocessor save করা।
        '''
        try:
            # -------- Step 1: Train এবং Test CSV file পড়া --------
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("✅ Train এবং Test data read complete হয়েছে।")

            # -------- Step 2: Preprocessing object পাওয়া --------
            preprocessing_obj = self.get_data_transformer_object()
            logging.info("✅ Preprocessing object পাওয়া গেছে।")

            # -------- Step 3: Target এবং Input features আলাদা করা --------
            target_column_name = "math_score"
            numerical_columns = ["writing_score", "reading_score"]

            input_feature_train_df = train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df = test_df[target_column_name]

            logging.info("✅ Train/Test features split করা হয়েছে।")

            # -------- Step 4: Transformation apply করা --------
            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            logging.info("✅ Preprocessing apply করা হয়েছে।")

            # -------- Step 5: Target array এর সাথে merge করা --------
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            # -------- Step 6: Preprocessor object save করা --------
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info(f"✅ Preprocessing object saved at {self.data_transformation_config.preprocessor_obj_file_path}")

            # -------- Step 7: Return final transformed data --------
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            raise CustomException(e, sys)
