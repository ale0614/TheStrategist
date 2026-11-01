import os
import numpy as np
import pandas as pd
import matplotlib as plt
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.compose import ColumnTransformer

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
clean_laps = pd.read_csv(os.path.join(PROJECT_ROOT, 'data', 'cleaned', 'all_laps_2022_2023_2024.csv'))
X=clean_laps[['TyreLife', 'LapNumber', 'Stint', 'Compound', 'Driver', 'Location']]
Y=clean_laps['LapTimeSeconds']

x_train = X[clean_laps['Season'] != 2024]
x_test  = X[clean_laps['Season'] == 2024]
y_train = Y[clean_laps['Season'] != 2024]
y_test  = Y[clean_laps['Season'] == 2024]
#Tranform the ones that have words instead of numbers
#USE OneHotencoder
categorical=['Driver', 'Compound', 'Location']
numerical=['LapNumber', 'TyreLife', 'Stint']
#y is the thing im trying to predict
#x the thing i use to predict
preprocessor=ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical),
        ('num', 'passthrough', numerical)

    ]
)
x_train_encoded = preprocessor.fit_transform(x_train)
x_test_encoded = preprocessor.transform(x_test)


model=GradientBoostingRegressor()
model.fit(x_train_encoded, y_train)
pred=model.predict(x_test_encoded) #answer

mae=mean_absolute_error(y_test, pred) # average de mi error
rmse = np.sqrt(mean_squared_error(y_test, pred)) #bigger mistakes

results = x_test.reset_index(drop=True).copy()

results['Actual'] = y_test.reset_index(drop=True)
results['Predicted'] = pred
results['Error'] = abs(results['Actual'] - results['Predicted'])

train_circuits = set(x_train['Location'].unique())
test_circuits = set(x_test['Location'].unique())

# Average error without Shanghai
#mae_known = known_circuits['Error'].mean()

'''unseen_circuits = test_circuits - train_circuits

print("Circuits not seen during training:")
print(unseen_circuits)'''
'''                                                                                    TESTING SHANGAI ERROR
# Results for circuits the model has seen before
known_circuits = results[results['Location'] != 'Shanghai']



# Average error for Shanghai only
shanghai = results[results['Location'] == 'Shanghai']
mae_shanghai = shanghai['Error'].mean()

results['SignedError']=results['Predicted']-results['Actual']
shanghai = results[results['Location'] == 'Shanghai']

# Display averages
print("\nSHANGHAI AVERAGES:")
print(shanghai[['Actual', 'Predicted', 'SignedError']].mean())

print("Shanghai overpredictions:",
    (shanghai['SignedError'] > 0).sum())

print("Shanghai underpredictions:",
    (shanghai['SignedError'] < 0).sum())


print("Overall MAE:", mae)
print("MAE without Shanghai:", mae_known)
print("Shanghai MAE:", mae_shanghai)
print("Shanghai laps:", len(shanghai))'''

print("\nWORST 20 PREDICTIONS:")
print(
    results.sort_values('Error', ascending=False).head(20)
)

print("\nAVERAGE ERROR BY CIRCUIT:")
print(
    results.groupby('Location')['Error']
    .mean()
    .sort_values(ascending=False)
)

print("\nAVERAGE ERROR BY COMPOUND:")
print(
    results.groupby('Compound')['Error']
    .mean()
    .sort_values(ascending=False)
)
print("MAE:", mae)
print("RMSE:", rmse)
print(results.head(20))
print("Training rows:", len(x_train))
print("Testing rows:", len(x_test))
#print(clean_laps['Season'].unique())'''



'''
A 2D table or matrix where every row is a separate data sample, and every column is an individual measurement
or characteristic
Divide your X and y into training sets 
to teach the model, and testing sets training sets (X_train, y_train)
testing sets (X_test, y_test) to check its accuracy later.

'''
