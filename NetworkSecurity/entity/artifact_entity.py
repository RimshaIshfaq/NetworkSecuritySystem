from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_path_file:str
    test_path_file:str

@dataclass
class DataValidationArtifact:
    validationstatus:bool
    valid_train_file_path:str
    valid_test_file_path:str    
    invalid_train_file_path:str
    invalid_test_file_path:str  
    drift_report_file_path:str
    