import numpy as np
import pandas as pd
import json

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.utils import resample

def grid_search() -> dict:

    search_space = {
        'n_estimators': np.arange(100, 1000, 50, int),  # number of trees in the forest
        'max_depth': np.arange(2, 60, 2, int),          # depth of each tree
        'min_samples_split': np.arange(2, 50, 2, int),  # minimum number of samples to split an internal node
        'min_samples_leaf': np.arange(1, 20, 2, int)    # 
    }

    rnd_forest = RandomForestClassifier(random_state=42)

    grid_search = GridSearchCV(estimator=rnd_forest, param_grid=search_space, cv=5, n_jobs=-1)

    # load data for grid search
    ljet_data = pd.read_csv('jet_data/ljet_train.csv')
    cjet_data = pd.read_csv('jet_data/cjet_train.csv')
    bjet_data = pd.read_csv('jet_data/bjet_train.csv')

    jet_data = pd.concat([ljet_data, cjet_data, bjet_data], axis=0).reset_index(drop=True)

    X = jet_data.columns.drop('mc_flavour')
    y = jet_data['mc_flavour']


    X_train, _, y_train, _ = train_test_split(X, y, train_size=0.8, random_state=42, stratify=y)

    # sample a fraction of the training dataset for hyperparameter tuning
    sample_fraction = 0.2
    X_train_sample, y_train_sample = resample(X_train, y_train, replace=False, n_samples=int(sample_fraction * len(X_train)), random_state=42)

    grid_search.fit(X_train_sample, y_train_sample)

    return grid_search.best_params_


if __name__ == '__main__':
    opt_hyperparameters = grid_search()

    with open('grid_parameters.json', 'w') as f:
        json.dump(opt_hyperparameters, f, indent=4)