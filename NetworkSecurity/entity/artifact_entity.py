from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_path_file:str
    test_path_file:str