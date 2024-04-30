# ekhane frequently use kora function gulo likhi 

from src.exception import CustomException
from src.constant import *

from sklearn.metrics import accuracy_score

import pickle 

# mogo db collection ke dataframe e convert korey 
def export_collection_as_df(db_name,collection_name):
    try:
        # clint create 
        mongo_client = MongoClient(MONGO_DB_URL)
        # collection 
        collection = mongo_client[db_name][collection_name]
        # convert it to df 
        df =  pd.DataFrame(list(collection.find()))
        # remove _id colm 
        if "_id" in df.columns.to_list():
            df = df.drop(columns=["_id"],axis=1)
        # na take replace with np.nan
        df = df.replace("na",np.nan)

        return df 


    except Exception as e:
        raise CustomException(e, sys)

# model er performance evauate korar jonno 
def evaluate_model(x_train,y_train,x_test,y_test,models):
    try:
        model_rep={}
        for i in len(models):
            # model create 
            model = list(models.values())[i]
            #traine the model 
            model.fit(x_train,y_train)
            # predict 
            y_test_pred = model.predict(x_test)
            # accuracy 
            score = accuracy_score(y_test,y_test_pred)

            # append in report 
            model_rep [list(model.keys())[i]] = score 

            return model_rep
        
    except Exception as e:
        raise CustomException(e, sys)

# pickle file dump korar jonno 
def save_object(file_path,obj):
    # directory banabo 
    os.makedirs(os.path.dirname(file_path),exist_ok=True)
    # file ke open korbo 
    with open(file_path,"wb") as f:
        pickle.dump(obj, f)