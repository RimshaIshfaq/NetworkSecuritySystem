import yaml
from NetworkSecurity.exception.exception import NetworkSecurityException    
from NetworkSecurity.logging.logger import logging
import os, sys
import numpy as np
import dill
import pickle   
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV


def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path, 'r') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def write_yaml_file(file_path:str, content:object, replace:bool =False)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

def save_numpy_array_data(file_path:str, array:np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,'wb') as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
def save_object(file_path:str, obj:object)->None:
    try:
        logging.info("Entered the save_object method of utils")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of  Mainutils class")

    except Exception as e:
        raise NetworkSecurityException(e,sys)

def load_object(file_path: str, ) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exist")
        with open(file_path, "rb") as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from e


def load_numpy_array_data(file_path: str)->np.array:
        try:
            with open(file_path, "rb") as file_obj:
                return np.load(file_obj)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from e
        
def evaluate_models(x_train, y_train, x_test, y_test, models, params):
    try:
        from sklearn.model_selection import GridSearchCV
        from sklearn.metrics import accuracy_score
        
        report = {}

        for model_name, model in models.items():
            para = params.get(model_name, {})  # get parameters safely for each model

            try:
                gs = GridSearchCV(model, para, cv=3)
                gs.fit(x_train, y_train)

                model.set_params(**gs.best_params_)
                model.fit(x_train, y_train)

                y_train_pred = model.predict(x_train)
                y_test_pred = model.predict(x_test)

                train_score = accuracy_score(y_train, y_train_pred)
                test_score = accuracy_score(y_test, y_test_pred)

                report[model_name] = test_score
                print(f"{model_name} trained successfully with score {test_score:.4f}")

            except Exception as e:
                print(f"Skipping {model_name} due to parameter error: {e}")
                continue

        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)
