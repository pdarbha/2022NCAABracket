"""
This script generates the win probability of each team beating the other 65 teams
"""
import pandas as pd

training_data = pd.read_csv('training_data.csv')
training_data.dropna(inplace=True)
training_data.head()

# use if needed
def change_column_name(column_name):
  column_name = column_name.replace("_name", "")
  column_name = column_name.replace("_", " ")
  return column_name

training_data = training_data.drop(['Year'], axis = 1)
training_data = training_data.rename(columns={column:(change_column_name(column)) for column in training_data.columns})
training_data = training_data.rename(columns={'away':'away Team', 'home':'home Team'})

training_data = training_data.rename(columns={'away Win Percentage':'away Win %', 'home Win Percentage':'home Win %'})

print(list(training_data.columns))

print(training_data.shape)

from sklearn.model_selection import train_test_split, KFold
from sklearn.metrics import accuracy_score
import numpy as np

X = training_data.drop(['Win', 'away Team', 'home Team', 'away Seed', 'home Seed'],axis=1)
Y = training_data['Win']

print(X.shape, Y.shape)
print(np.sum(Y))

from sklearn.svm import SVC

max_accuracy = 0.0
accuracy_sum = 0.0
max_svm_model = None
split = 1
X_numpy = X.to_numpy()
Y_numpy = Y.to_numpy()
kf = KFold(n_splits=5, shuffle=True, random_state=45)
for train_index, val_index in kf.split(X_numpy):
    X_train,X_val = X_numpy[train_index,:],X_numpy[val_index,:]
    Y_train,Y_val = Y_numpy[train_index],Y_numpy[val_index]
    
    model = SVC(probability=True)
    model.fit(X_train,Y_train) 
    
    Y_pred = model.predict(X_val)
    
    accuracy = accuracy_score(Y_val,Y_pred)
    
    print('Accuracy for split {}: {}'.format(split,accuracy))
    
    if accuracy > max_accuracy:
        max_accuracy = accuracy
        max_svm_model = model
        
    split += 1
    accuracy_sum += accuracy

average_accuracy = accuracy_sum / 5
print(max_accuracy)
print(average_accuracy)

import csv
teams = {}
inv_teams = {}
stats = np.zeros((66,10))
with open('2022_data.csv', newline='') as final_data:
    reader = csv.DictReader(final_data)
    i = 0
    for row in reader:
        teams[i] = (row['Team'], row['Seed'])
        inv_teams[row['Team']] = i
        stats[i][0] = row['Win %']
        stats[i][1] = row['AdjEM']
        stats[i][2] = row['AdjO']
        stats[i][3] = row['AdjD']
        stats[i][4] = row['AdjT']
        stats[i][5] = row['Luck']
        stats[i][6] = row['AdjEM_SOS']
        stats[i][7] = row['OppO']
        stats[i][8] = row['OppD']
        stats[i][9] = row['AdjEM_NCSOS']
        i+=1

probabilities = np.zeros((66,66))
for i in range(0,66):
    for j in range(i+1,66):
        input = np.concatenate((stats[j],stats[i]))
        p = max_svm_model.predict_proba(input.reshape(1,-1))
        probabilities[i][j] = p[0][1]

pd.DataFrame(probabilities).to_csv('probabilities_2022.csv', header=None, index=None)
