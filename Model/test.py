import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics import classification_report

from Model.AnomalyDetection import AnomalyDetection

# Pre-processing data into fraud and non-fraud
df = pd.read_csv('Model/creditcard.csv')
df_features = df.iloc[:, :-1]
df_normalized = pd.DataFrame(preprocessing.normalize(df_features))
df_normalized['Class'] = df['Class']

df_nonfraud = df_normalized.loc[df['Class'] == 0]
df_fraud = df_normalized.loc[df['Class'] == 1]

# setting train and test data
df_features_nonfraud = df_nonfraud.iloc[:, :-1]
df_features_fraud = df_fraud.iloc[:, :-1]
df_features_all = df_normalized.iloc[:, : -1]

# test set will contain all data
# training set will only contain non-fraud data
# no y_train as all training data assumed to be non-fraud
X_test = df_features_all
y_test = df['Class']

X_train = df_features_nonfraud
print(f"Original number of non-fraud: {df_nonfraud.shape[0]}")
print(f"Original number of fraud: {df_fraud.shape[0]}")
print(X_train.shape)

# preparing train and test data
no_of_samples = 5000
# no_of_samples = len(df)
feature_columns = [1, 3]
# selected number of train data for training
X_train_selected = X_train[:no_of_samples]

if __name__ == "__main__":
    # training and prediction
    AD = AnomalyDetection()
    AD.fit(X_train_selected, feature_columns)

    # evaluation using test data
    y_pred = AD.predict(X_test, feature_columns)

    print(f"Number of non-fraud detected: {len(np.where(y_pred == 0)[0])}")
    print(f"Number of fraud detected: {len(np.where(y_pred == 1)[0])}\n")

    print(classification_report(y_test, y_pred))
