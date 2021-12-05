from enum import Enum

class ModelType:
    LOG_REGRESSION = "LogisticRegression"
    GRID_LOG_REGRESSION = "GridLogisticRegression"
    TREE_CLASSIFIER = "TreeClassifier"
    RANDOM_FOREST = "RandomForest"
    RANDOM_FOREST_SMOTE = "RandomForestSmote" 
    NEURAL_NETWORK_SMOTE = "NeuralNetworkSmote"