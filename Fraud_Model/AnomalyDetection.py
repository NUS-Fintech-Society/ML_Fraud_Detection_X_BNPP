from sklearn.cluster import OPTICS
import numpy as np
import time
from sklearn.svm import OneClassSVM 

"""
1. AnomolyDetection(eps,percent,gamma) - initialise the hyperparameters
    - eps: maximum distance between each point to consider for REDBSCAN
    - percent: proportion of datapoints to keep (e.g. 0.2 to keep 20% of the data)
    - gamma: coefficient for SVDD rbf kernel
    - Drop_rate: rate of points to drop while reducing data

2. reduce() - reduce the data points based on hyperparameters set in 1.

3. fit(data) - reduce, fit and train the data provided
    - note that the reduction of datapoints is done already
    - no option to remove the reduction of datapoints step as it is too computationally expensive

4. predict(data) - predict incoming data based on trained SVDD model
    - can be dataframe, but must be a series
"""
class AnomolyDetection():

  #set data and hyperparameters
  def __init__(self,eps = 0.02, percent = 0.20, gamma = 0.01, drop_rate = 0.2):
    self.data = None
    self.eps = eps
    self.percent = percent
    self.gamma = gamma
    self.svm = None
    self.drop_rate = drop_rate
    self.feature_columns = None
  
  #reduce data points using REDBSCAN algo
  def reduce(self):
    print("="*50)
    print("="*17 + "Reducing data" + "="*20)
    print("="*50)
    #select data based on input parameters
    if self.feature_columns:
      data_selected = self.data.iloc[:,self.feature_columns[0]:self.feature_columns[1]].to_numpy()
    else:
      data_selected = self.data.to_numpy()
    #run DBSCAN
    df_dbscan_labels = self.DBSCAN(data_selected, 0.02)
    #running REDBSCAN
    reduced_pts = self.REDBSCAN(data_selected,df_dbscan_labels,self.eps,self.percent,self.drop_rate)
    return reduced_pts

  #fit svdd with reduced points
  def fit(self,data, feature_columns = None):
    print("Anomoly Detection: eps = {}, percent = {}, gamma = {}, drop_rate = {}".format(self.eps,self.percent,self.gamma,self.drop_rate))
    if feature_columns:
      print("Selected feature columns: column {} to column {}".format(feature_columns[0],feature_columns[1]))
    else:
      print("All feature columns to be used")
    start = time.time()
    self.feature_columns = feature_columns
    self.data = data
    #reduce points with redbscan
    reduced_pts = self.reduce()
    #svdd training
    print("="*50)
    print("="*17 + "Training SVDD" + "="*20)
    print("="*50)
    print("Starting SVDD training...")
    svdd_start = time.time()
    training_pts_toList = reduced_pts.values.tolist()
    svm = OneClassSVM(kernel='rbf', gamma=self.gamma) 
    svm.fit(training_pts_toList)
    self.svm = svm
    end = time.time()
    print("SVDD training done")
    print("SVDD time taken:{}".format(end-svdd_start))
    print("="*50)
    print("Total Time taken: {}".format(end-start))
  
  #predict data
  # 1 is non fraud, -1 is fraud
  def predict(self,data, feature_columns = None):
    if feature_columns:
      return self.svm.predict(data.iloc[:,feature_columns[0]:feature_columns[1]])
    else:
      return self.svm.predict(data)

  #get input feature columns the model was trained on
  def get_trained_features(self):
    return self.feature_columns

  def DBSCAN(self,data,eps):
    start = time.time()
    print("Starting DBSCAN...")
    clustering_optics = OPTICS(eps = eps, cluster_method = 'dbscan').fit(data)
    end = time.time()
    print("DBSCAN DONE")
    print("Time taken for DBSCAN: {} seconds".format(end-start))
    cluster_labels = clustering_optics.labels_
    #df_dbscan = np.column_stack((data,cluster_labels))
    #df_dbscan = pd.DataFrame(df_dbscan,columns = ['x','y','labels'])
    #df_dbscan['labels'] = df_dbscan['labels'].astype(int)
    labels = cluster_labels.astype(int)
    return labels

  #feature_data is the from original data, input type numpy array 
  #labels is the labels found from DBSCAN
  #eps is the max distance from each pt to sample
  #percent is selection of top proportion with highest distance calculated

  def REDBSCAN(self,feature_data,labels,eps,percent,drop_rate):
    print("Starting REDBSCAN...")
    start = time.time()
    boundary_pts = []
    dropped = []
    counter = 0
    for index, x in enumerate(feature_data):
      if index in dropped:
        continue
      counter +=1
      dist, dropped_pts = self.findTotalDistance(x,feature_data,labels,labels[index],eps,drop_rate)
      boundary_pts.append({
          'pt': x,
          'dist': dist
      })
      boundary_pts.sort(key = lambda x: x['dist'], reverse = True)
      df_reduced_pts = self.formatReducedPts(boundary_pts,percent)
      for i in dropped_pts:
        if i not in dropped:
          dropped.append(i)
    end = time.time()
    print("REDBSCAN DONE")
    print("Time taken: {} s".format(end-start))
    return df_reduced_pts

  def findTotalDistance(self,pt,data,labels,cluster,eps,drop_rate):
    distance = 0
    no_pts = 0
    rank = {}
    for index, x in enumerate(data):
      if labels[index] == cluster:
        dist = np.linalg.norm(pt-x)
        if dist <= eps:
          distance += dist
          no_pts += 1
          rank[index] = dist
    {k: v for k, v in sorted(rank.items(), key=lambda item: item[1])}
    dropped_pts = [*rank]
    dropped_pts = dropped_pts[:int(drop_rate*len(dropped_pts))]
    return distance/no_pts, dropped_pts

  def formatReducedPts(self,reduced_pts,percent):
    length_pts = len(reduced_pts)
    selected_pts = reduced_pts[:int(length_pts*percent)]
    #dropped_pts = reduced_pts[int(length_pts*percent):]
    #dropped_pts = [x['index'] for x in dropped_pts]
    points = [d['pt'] for d in selected_pts]
    df_reduced_pts = pd.DataFrame(points)
    #optional step
    #df_reduced_pts.columns = ['x','y']
    return df_reduced_pts
