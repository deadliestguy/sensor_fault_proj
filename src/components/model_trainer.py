import os,sys
import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging

# Model selection -> classification problem 
from sklearn.svm import  SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import accuracy_score  #for accuracy 

from src.utilis import evaluate_model
from src.utilis import save_object 

from dataclasses import dataclass
# class 1-> congiguration defin korey 
@dataclass
class ModelTrainerConfig:
    model_file_path  = os.path.join('artifacts','model.pkl')


# class 2-> model training initiate hoi 
class ModelTrainer:
    # ctor 
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    # training hoi 
    def initiate_model_training(self,train_arr,test_arr):
        try:
            # segregate x and y 
            x_train = train_arr[:,:-1]
            y_train = train_arr[:,-1]
            x_test = test_arr[:,:-1]
            y_test = test_arr[:,-1]

            # models 
            models={
                    "svc": SVC(),
                    "KNeighborsClassifier" : KNeighborsClassifier(),
                    "DecisionTreeClassifier": DecisionTreeClassifier(),
                    "RandomForestClassifier" : RandomForestClassifier(),
                    "XGBClassifier": XGBClassifier(),
                    "AdaBoostClassifier" :AdaBoostClassifier()
                    }
            # evaluate model performace 
            model_rep:dic = evaluate_model(x_train,y_train,x_test,y_test,models)

            # finding best model 
            best_model_score = max(sorted(model_rep.values()))
            best_model_name = list(models.keys())[list(models.values()).index(best_model_score)]

            best_model_obj  = models[best_model_name]

            # addition 
            if best_model_score <0.6:
                raise Exception("no best model found")
            
            # save the model 
            save_object(self.model_trainer_config.model_file_path,best_model_obj)





        except Exception as e:
            raise CustomException(e, sys)