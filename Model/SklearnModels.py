import itertools

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

# from sklearn.covariance import EllipticEnvelope
# from sklearn.neighbors import LocalOutlierFactor
# from sklearn.svm import OneClassSVM

"""
https://towardsdatascience.com/unsupervised-learning-for-anomaly-detection-44c55a96b8c1
https://www.kaggle.com/vardaanbajaj/unsupervised-anomaly-detection-for-fraud-detection
"""

# Reading
df = pd.read_csv('Model/creditcard.csv')
print(df.shape)

# Sampling
# data = df.sample(frac=0.2, random_state=1)
data = df
print(data.shape)

# class distribution
num_classes = pd.value_counts(df['Class'], sort=True)
print(num_classes)
num_classes.plot(kind='bar')
plt.title("Transaction Class Distribution")
plt.xticks(range(2), ["Normal", "Fraud"])
plt.xlabel("Class")
plt.ylabel("Frequency")
plt.show()

fraud = df[df['Class'] == 1]
normal = df[df['Class'] == 0]
print(fraud.shape, normal.shape)

# Time vs Class relationship
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
f.suptitle('Time of transaction v/s Amount by Class type')
ax1.scatter(fraud.Time, fraud.Amount)
ax1.set_title('Fraud')
ax2.scatter(normal.Time, normal.Amount)
ax2.set_title('Normal')
plt.xlabel('Time (in secs)')
plt.ylabel('Amount')
plt.xlim((0, 20000))
plt.show()

# Amount vs Class relationship
f, (ax1, ax2) = plt.subplots(2, 1, sharex=True)
f.suptitle('Amount per transaction by class')
bins = 10
ax1.hist(fraud.Amount, bins=bins)
ax1.set_title('Fraud')
ax2.hist(normal.Amount, bins=bins)
ax2.set_title('Normal')
plt.xlabel('Amount ($)')
plt.ylabel('Number of Transactions')
plt.xlim((0, 20000))
plt.yscale('log')
plt.show()

# Proportion of Class
fraud = data[data['Class'] == 1]
normal = data[data['Class'] == 0]
anomaly_fraction = len(fraud) / float(len(normal))
print(f"Fraction of anomaly in data: {anomaly_fraction}")
print("Fraud Cases: " + str(len(fraud)))
print("Normal Cases: " + str(len(normal)))

# Distribution of all features
data.hist(figsize=(15, 15), bins=64)
plt.show()

# Drop Time, V1 and V4
data.drop(['Time', 'V1', 'V24'], axis=1, inplace=True)
columns = data.columns.tolist()
target = 'Class'
columns = [c for c in columns if c != 'Class']

X, y = np.array(data.drop('Class', axis=1)), np.array(data.Class)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=40, stratify=y)
# X_train = data.iloc[:45000, :-1]
# y_train = data.iloc[:45000, -1]
# X_test = data.iloc[45000:, :-1]
# y_test = data.iloc[45000:, -1]

print(X_train.shape, X_test.shape)
print(y_train.shape, y_test.shape)

# Model
# model = LocalOutlierFactor(contamination=anomaly_fraction)
model = IsolationForest(n_estimators=10, warm_start=True)
# model = EllipticEnvelope(contamination=anomaly_fraction)
# model = OneClassSVM(nu=anomaly_fraction)

# Prediction
y_train_pred = model.fit_predict(X_train)
y_train_pred[y_train_pred == 1] = 0
y_train_pred[y_train_pred == -1] = 1
y_test_pred = model.fit_predict(X_test)
y_test_pred[y_test_pred == 1] = 0
y_test_pred[y_test_pred == -1] = 1

classes = np.array(['0', '1'])


# Evaluation
def plot_confusion_matrix(cm, classes, title='Confusion matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()


cm_train = confusion_matrix(y_train, y_train_pred)
plot_confusion_matrix(cm_train, ["Normal", "Fraud"])

cm_test = confusion_matrix(y_test, y_test_pred)
plot_confusion_matrix(cm_test, ["Normal", "Fraud"])

# Training
print(f"Total fraud transactions detected in training: {cm_train[1][1]} / {cm_train[1][1] + cm_train[1][0]}")
print(f"Total non-fraud transactions detected in training: {cm_train[0][0]} / {cm_train[0][1] + cm_train[0][0]}")
print(f"Probability to detect a fraud transaction in training: {cm_train[1][1] / (cm_train[1][1] + cm_train[1][0])}")
print(f"Probability to detect a non-fraud transaction in training: {cm_train[0][0] / (cm_train[0][1] + cm_train[0][0])}")
print(f"Accuracy of model on the training: {100 * (cm_train[0][0] + cm_train[1][1]) / (sum(cm_train[0]) + sum(cm_train[1]))}")

# Test
print(f"Total fraud transactions detected in test: {cm_test[1][1]} / {cm_test[1][1] + cm_test[1][0]}")
print(f"Total non-fraud transactions detected in test: {cm_test[0][0]} / {cm_test[0][1] + cm_test[0][0]}")
print(f"Probability to detect a fraud transaction in test: {cm_test[1][1] / (cm_test[1][1] + cm_test[1][0])}")
print(f"Probability to detect a non-fraud transaction in test: {cm_test[0][0] / (cm_test[0][1] + cm_test[0][0])}")
print(f"Accuracy of model on the test: {100 * (cm_test[0][0] + cm_test[1][1]) / (sum(cm_test[0]) + sum(cm_test[1]))}")

# Classification Report
# print(classification_report(y_train, y_train_pred))
print(classification_report(y_test, y_test_pred))
print(f"AUROC score: {roc_auc_score(y_test, y_test_pred)}")
