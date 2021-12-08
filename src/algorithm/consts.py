from enum import Enum


class ModelType:
    GRID_LOG_REGRESSION = "GridLogisticRegression"
    K_MEANS = "KMeans"
    LOG_REGRESSION = "LogisticRegression"
    RANDOM_FOREST = "RandomForest"
    RANDOM_FOREST_COMPLETE = "RandomForestComplete"  # Contains kbest, grid and smote
    RANDOM_FOREST_SMOTE = "RandomForestSmote"
    NEURAL_NETWORK_SMOTE = "NeuralNetworkSmote"
    SVM = "Svm"
    TREE_CLASSIFIER = "TreeClassifier"
