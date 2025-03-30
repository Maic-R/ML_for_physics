import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample

def grid_search() -> dict:

    search_space = {
        'n_estimators': np.arange(150, 500, 50, int),   # number of trees in the forest
        'max_depth': np.arange(1, 30, 10, int),          # depth of each tree
        'min_samples_split': np.arange(1, 30, 10, int),  # minimum number of samples to split an internal node
        'min_samples_leaf': np.arange(1, 20, 5, int)    # 
    }

    rnd_forest = RandomForestClassifier(random_state=42)

    grid_search = GridSearchCV(estimator=rnd_forest, param_grid=search_space, cv=5, n_jobs=-1, verbose=1)

    # load data for grid search
    ljet_data = pd.read_csv('jet_data/ljet_train.csv')
    cjet_data = pd.read_csv('jet_data/cjet_train.csv')
    bjet_data = pd.read_csv('jet_data/bjet_train.csv')

    jet_data = pd.concat([ljet_data, cjet_data, bjet_data], axis=0).reset_index(drop=True)

    features_for_training = jet_data.columns.drop(['mc_flavour', 'PT']) # use all the features except PT. Remove label column

    X = jet_data[features_for_training] # input for random forest are data of the selected features
    y = jet_data['mc_flavour'] # output: label of the jet

    X_train, _, y_train, _ = train_test_split(X, y, train_size=0.8, random_state=42, stratify=y)

    # sample a fraction of the training dataset for hyperparameter tuning
    sample_fraction = 0.2
    X_train_sample, y_train_sample = resample(X_train, y_train, replace=False, n_samples=int(sample_fraction * len(X_train)), random_state=42)

    grid_search.fit(X_train_sample, y_train_sample)

    return grid_search.best_params_


if __name__ == '__main__':
    opt_hyperparameters = grid_search()

    print('Optimized hyperparamters: ', opt_hyperparameters)