import time
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.cluster import OPTICS
from sklearn.svm import OneClassSVM


class AnomalyDetection:
    """
    AnomalyDetection object.
    """

    def __init__(self, eps: float = 0.02, percent: float = 0.20, gamma: float = 0.01, drop_rate: float = 0.2):
        """
        Initialises the AnomalyDetection object.

        Here is where we set the hyperparameters that will be used. Note that tuning of hyperparameters is necessary.

        :param eps: Float representing the Epsilon. Maximum distance between each point to consider for REDBSCAN.
        :param percent: Float representing the proportion of data points to retain (e.g. 0.2 to keep 20% of the data) for REDBSCAN.
        :param gamma: Float representing the coefficient for SVDD rbf kernel
        :param drop_rate: Float representing the rate of points to drop while reducing data in REDBSCAN.
        """
        self.data = None
        self.eps = eps
        self.percent = percent
        self.gamma = gamma
        self.svm = None
        self.drop_rate = drop_rate
        self.feature_columns = None

    def get_trained_features(self) -> List[int]:
        """
        Gets input feature columns the model was trained on.

        :return: List representing the start and end index of columns to be used
        """
        return self.feature_columns

    def DBSCAN(self, data: np.ndarray, eps: float) -> np.ndarray:
        """
        Density-Based Spatial Clustering of Applications with Noise algorithm from sklearn.

        :param data: Numpy array representing the training data.
        :param eps: Float representing the eps.
        :return: Numpy array representing the training data.
        """
        start = time.time()
        print("Starting DBSCAN...")
        clustering_optics = OPTICS(eps=eps, cluster_method='dbscan').fit(data)
        cluster_labels = clustering_optics.labels_
        labels = cluster_labels.astype(int)
        end = time.time()
        print("DBSCAN completed!")
        print(f"Time taken for DBSCAN: {end - start} seconds\n")

        return labels

    # feature_data is the from original data, input type numpy array
    # labels is the labels found from DBSCAN
    # eps is the max distance from each pt to sample
    # percent is selection of top proportion with highest distance calculated
    def REDBSCAN(self, feature_data: np.ndarray, labels: np.ndarray, eps: float, percent: float, drop_rate: float) -> pd.DataFrame:
        """
        Radar Elliptical Density-Based Spatial Clustering of Applications with Noise algorithm from sklearn.

        :param feature_data: Numpy array representing the original training data.
        :param labels: Numpy array representing the labels found from DBSCAN.
        :param eps: Float representing the max distance from each point to sample.
        :param percent: Float representing the selection of top proportion with highest distance calculated.
        :param drop_rate: Float representing the rate of points to drop while reducing data.
        :return: DataFrame representing the reduced points.
        """
        print("Starting REDBSCAN...")
        start = time.time()
        boundary_pts = []
        dropped = []
        for index, x in enumerate(feature_data):
            if index in dropped:
                continue
            dist, dropped_pts = self.find_total_distance(x, feature_data, labels, labels[index], eps, drop_rate)
            boundary_pts.append({'pt': x, 'dist': dist})
            for i in dropped_pts:
                if i not in dropped:
                    dropped.append(i)

        boundary_pts.sort(key=lambda x: x['dist'], reverse=True)
        df_reduced_pts = self.format_reduced_points(boundary_pts, percent)

        end = time.time()
        print("REDBSCAN completed!")
        print(f"Time taken for REDBSCAN: {end - start} s\n")

        return df_reduced_pts

    @staticmethod
    def find_total_distance(pt: np.ndarray, data: np.ndarray, labels: np.ndarray, cluster: int, eps: float, drop_rate: float) -> Tuple[float, list]:
        """
        Finds the euclidean distance.

        :param pt:
        :param data:
        :param labels:
        :param cluster:
        :param eps:
        :param drop_rate:
        :return:
        """
        distance = 0
        no_pts = 0
        rank = {}

        for index, x in enumerate(data):
            if labels[index] == cluster:
                dist = np.linalg.norm(pt - x)
                if dist <= eps:
                    distance += dist
                    no_pts += 1
                    rank[index] = dist

        {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}

        dropped_pts = [*rank]
        dropped_pts = dropped_pts[:int(drop_rate * len(dropped_pts))]

        return distance / no_pts, dropped_pts

    @staticmethod
    def format_reduced_points(reduced_pts: List[dict], percent: float) -> pd.DataFrame:
        """
        Formats the reduced points.

        :param reduced_pts:
        :param percent:
        :return: DataFrame representing the reduced points.
        """
        length_pts = len(reduced_pts)
        selected_pts = reduced_pts[:int(length_pts * percent)]

        points = [d['pt'] for d in selected_pts]
        df_reduced_pts = pd.DataFrame(points)

        return df_reduced_pts

    def reduce(self) -> pd.DataFrame:
        """
        Reduce the data points based on hyperparameters set in the constructor using the REDBSCAN algorithm.

        :return: DataFrame representing the reduced points.
        """
        print("=" * 50)
        print("=" * 17 + "Reducing data" + "=" * 20)
        print("=" * 50)

        # select data based on input parameters
        if self.feature_columns:
            start, end = self.feature_columns
            data_selected = self.data.iloc[:, start:end].to_numpy()
        else:
            data_selected = self.data.to_numpy()

        # run DBSCAN
        df_dbscan_labels = self.DBSCAN(data_selected, 0.02)
        # running REDBSCAN
        reduced_pts = self.REDBSCAN(data_selected, df_dbscan_labels, self.eps, self.percent, self.drop_rate)

        return reduced_pts

    def fit(self, data: pd.DataFrame, feature_columns: Optional[List[int]] = None) -> None:
        """
        Reduce, fit (with the reduced points) and train the data provided.

        Note that the reduction of data points is done already.
        No option to remove the reduction of data points step as it is too computationally expensive

        :param data: Numpy array representing the data used for training
        :param feature_columns: List representing the start and end index of columns to be used
        :return: None
        """
        print(f"Anomaly Detection parameters: eps = {self.eps}, percent = {self.percent}, gamma = {self.gamma}, drop_rate = {self.drop_rate}\n")

        if feature_columns:
            print(f"Selected feature columns: column {feature_columns[0]} to coumn {feature_columns[1]}\n")
        else:
            print("All feature columns to be used\n")

        start = time.time()
        self.feature_columns = feature_columns
        self.data = data

        # reduce points with redbscan
        reduced_pts = self.reduce()

        # svdd training
        print("=" * 50)
        print("=" * 17 + "Training SVDD" + "=" * 20)
        print("=" * 50)
        print("Starting SVDD training...")

        svdd_start = time.time()
        training_pts_toList = reduced_pts.values.tolist()
        svm = OneClassSVM(kernel='rbf', gamma=self.gamma)
        svm.fit(training_pts_toList)
        self.svm = svm
        end = time.time()

        print("SVDD training completed!")
        print(f"SVDD time take: {end - svdd_start}\n")

        print("=" * 50)
        print(f"Total time taken: {end - start}\n")

    def predict(self, data: pd.DataFrame, feature_columns: Optional[List[int]] = None) -> np.ndarray:
        """
        Predict incoming data based on trained SVDD model.

        :param data: Numpy array representing the data used for prediction
        :param feature_columns: List representing the start and end index of columns to be used
        :return: Numpy array representing the predicted class where 0 is non-fraud and 1 is fraud.
        """
        if feature_columns:
            start, end = feature_columns
            pred = self.svm.predict(data.iloc[:, start:end])
        else:
            pred = self.svm.predict(data)

        # reformat y_pred (run in sequence)
        pred[pred == 1] = 0
        pred[pred == -1] = 1

        return pred
