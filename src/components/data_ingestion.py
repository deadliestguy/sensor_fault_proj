import os 
import sys

import pandas as pd
import numpy as np

from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import train_test_split

from dataclasses import dataclass 

from src.utilis import export_collection_as_df

# class 1-> configuration define korey
@dataclass
class DataIngestionConfig: 
    # init function lekhar dorkar nei -> cause dataclass use korchi
    raw_file_path = os.path.join('artifacts','raw.csv')
    train_file_path = os.path.join('artifacts','train.csv')
    test_file_path = os.path.join('artifacts','test.csv')



# class2 -> data ingestion korey 
class DataIngestion:

    # ctor 
    def __init__(self):
        # oporer calss er object banbo 
        self.data_ingestion_config = DataIngestionConfig()
    
    # data ingestion initiate korbo 
    def initiate_data_ingestion(self):
        logging.info("data ingestion has started")
        try:
            # read the data 
            df:pd.DataFrame = export_collection_as_df(db_name = MONGO_DATABASE_NAME,
                                                      collection_name =MONGO_COLLECTION_NAME )
            
            # direcotry banabo 
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_file_path),exist_ok=True)

            # store raa data to csv file 
            df.to_csv(self.data_ingestion_config.raw_file_path,index=False,header=True)

            # train test split 
            train_data , test_data = train_test_split(df,test_size=0.20,random_state=42)

            # store train and test data to csv file 
            train_data.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_data.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)

            logging.info("ingestion has completed")
            return(
                self.data_ingestion_config.train_file_path,
                self.data_ingestion_config.test_file_path
            )


        except Exception as e:
            raise CustomException(e, sys)


