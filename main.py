from NetworkSecurity.components.data_ingestion import DataIngestion
from NetworkSecurity.components.data_validation import DataValidation
from NetworkSecurity.exception.exception import NetworkSecurityException
from NetworkSecurity.logging.logger import logging
from NetworkSecurity.entity.config_entity import DataIngestionConfig
from NetworkSecurity.entity.config_entity import DataValidationConfig
from NetworkSecurity.entity.config_entity import TrainingPipelineConfig

import sys


if __name__ == '__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data Ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Inititaion completed")
        print(dataingestionartifact)
        data_validation_config=DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(
            data_ingestion_artifact=dataingestionartifact,
            data_validation_config=data_validation_config
            )
        logging.info("Initiate the data Validation")
        data_validation_artifact= data_validation.initiate_data_validation()
        logging.info("Data Validation Completed")   
        print(data_validation_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    
