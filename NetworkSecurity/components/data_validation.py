#from NetworkSecurity.entity.artifact_entity import Data1ngestionArtifact

from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.entity.artifact_entity import  DataIngestionArtifact, DataValidationArtifact
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.utils.main_utils.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self._schema_config= read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    

    def validate_number_of_columns(self, dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self._schema_config)
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {dataframe.columns}")
            if len(dataframe.columns)==number_of_columns:
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)


    def initiate_data_validation(Self)->DataValidationArtifact:
        try:
            train_File_path=self.data_ingestion_artifact.trained_path_file
            test_File_path=self.data_ingestion_artifact.test_path_file

            #read teh data from train and test file
            train_dataframe=DataValidation.read_data(train_File_path)
            test_dataframe=DataValidation.read_data(test_File_path)

            #validate number of columns
            status=self.validate_number_of_columns(train_dataframe)
            if not status:
                error_message=f"Train data does not contain all the required columns"/n
            status=self.validate_number_of_columns(test_dataframe)
            if not status:
                error_message=f"Test data does not contain all the required columns"/n

            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path,index=False,header=True
                )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path,index=False,header=True
                )

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
            #let's check data drift
    def detect_dataset_drift(base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_sample_dist=ks_2samp(d1,d2)
                if is_sample_dist.p_value>=threshold:
                    is_found=False
                else:
                    is_found=True
                    status=False
                
                report.update({column:{
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
                }})
            
            drift_report_file_path=self.data_validation_config.drift_report_file_path

            #create directory
            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report,replace=True)
        except Exception as e:
            raise NetworkSecurityException(e, sys)
