import os,sys
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleIMputer #missign value 
from sklearn.preprocessing import StandardScaler #scaler down 
from sklearn.preprocessing import RobustScaler 
from sklearn.preprocesssing import FunctionTransformer  # arbitary func call korey 

from imblearn.combine import SMOTETomek #resample

from src.utilis import save_object

from dataclasses import dataclass


# class1-> configuration def korey 
@dataclass
class DataTransConfig:
    preprocessor_file_path = os.path.join('artifacts','preprocessor.pkl')


# class2-> data transfoamation initiate hoi 
class DataTrans:
    # ctor 
    def __init__(self):
        # object create korbo 
        self.data_trans_config = DataTransConfig()
    
    # pipeline create korbo 
    def create_pipeline(self):
        try:
            # na ke replace korar jonno custom function 
            replace_na_with_nan = lambda X: np.where(X=="na",np.nan,X)

            # pipiline create 
            preprocesseor = Pipeline(
                                        steps=[
                                            ("replace_na",FunctionTransformer(replace_na_with_nan)),#na replace korbo 
                                            ("Imputer",SimpleIMputer(strategy='constant',fill_value=0)),#misssing value handle 
                                            ("Scaler",StandardScaler()) #scale down korbo
                                        ]

                                    )
            
            return preprocesseor

        except Exception as e:
            raise CustomException(e, sys)


    # inititate data transformation 
    def initiate_data_transformation(self,train_data_path,test_data_path):
        try:
            # read the data 
            train_data = pd.read_csv(train_data_path)
            test_data = pd.read_csv(test_data_path)

            # segregate indep and depend feature 
            target_colm  = ['Good/Bad']
            target_colm_map = {"+1":0,"-1":1}

            x_train = train_data.drop(target_colm,axis=1)
            y_train = train_data[target_colm].map(target_colm_map)

            x_test = test_data.drop(target_colm,axis=1)
            y_test = test_data[target_colm].map(target_colm_map)

            #preprocesing korbo 
            preprocessor = self.create_pipeline()
            
            trans_x_train = preprocessor.fit_transform(x_train)
            trans_x_test = preprocessor.transform(x_test)

            # resample korbo 
            smt = SMOTETomek(sampling_strategy='auto')
            res_x_train ,res_y_train = smt.fit_resample(trans_x_train,y_train)
            res_x_test ,res_y_test = smt.fit_resample(trans_x_test,y_test)

            # preprocessor ke dump korbo pickle file e 
            save_object(file_path=self.data_trans_config.preprocessor_file_path, obj=preprocessor)

            # concat x and y 
            train_df = np.c_[res_x_train,np.array(res_y_train)]
            test_df = np.c_[res_x_test,np.array(res_y_test)]

            return (
                train_df,
                test_df,
                self.data_trans_config.preprocessor_file_path
            )
        
        except Exception as e:
            raise CustomException(e, sys)





