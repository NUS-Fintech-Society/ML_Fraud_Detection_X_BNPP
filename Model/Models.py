from typing import Union

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


class AutoEncoder:
    """
    AutoEncoder object
    """

    def __init__(self):
        pass

    def preprocess(self, data) -> pd.DataFrame:
        pass

    def fit(self, data) -> None:
        pass

    def predict(self, data) -> Union[list, np.ndarray]:
        pass


class IsolationForest:
    """
    IsolationForest object
    """

    def __int__(self):
        pass

    def preprocess(self, data) -> pd.DataFrame:
        pass

    def fit(self, data) -> None:
        pass

    def predict(self, data) -> Union[list, np.ndarray]:
        pass


class LocalOutlierFactor:
    """
    LocalOutlierFactor object
    """

    def __int__(self):
        pass

    def preprocess(self, data) -> pd.DataFrame:
        pass

    def fit(self, data) -> None:
        pass

    def predict(self, data) -> Union[list, np.ndarray]:
        pass


if __name__ == '__main__':
    # Reading
    df = pd.read_csv('Dataset/data/df_simulated.csv')
    labels = df['Behaviour ID']
    training = df.drop('Behaviour ID', axis=1)

    # Model
    model = AutoEncoder()
    # Pre-processing
    df_processed = model.preprocess(training)
    # Training
    model.fit(df_processed)
    # Predicting
    pred = model.predict(df_processed)

    # Evaluating
    confusion_matrix(labels, pred)
