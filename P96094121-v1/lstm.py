import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout,BatchNormalization
from sklearn.preprocessing import MinMaxScaler 
from tensorflow.keras import regularizers

class preprocessing():    
    def __init__(self, train):
        self.train = train
        # self.test = test

    def data_load(self):
        self.train = pd.read_csv(self.train,  header = None)
        # self.test = pd.read_csv(self.test, header = None)
        self.train = self.train.drop([0])
        self.train = self.train.drop([0],axis=1)
        self.test = self.train
        # self.train = pd.concat([self.train,self.test], axis = 0)

    def data_scaler(self, scaler, prices, inverse):
        if inverse is False:
            self.train_set = self.train_set.values.reshape(-1,1)
            self.training_set_scaled = scaler.fit_transform(self.train_set)
        else:
            return scaler.inverse_transform(prices)

    def select_feature(self, feature_num):
        self.train_set = self.train.iloc[:,feature_num] 
        
        return self.train_set
    def build_train_data(self, scope):
        self.training_data = self.training_set_scaled[0:5086]
        X_train = []
        y_train = []

        for i in range(scope, len(self.training_data), 1):
            X_train.append(self.training_data[i-scope: i, 0])
            y_train.append(self.training_data[i, 0])
        X_train, y_train = np.array(X_train), np.array(y_train)
        X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
        y_train = np.reshape(y_train, (y_train.shape[0], 1))
        # print(X_train.shape)
        # print(self.training_data.shape)
        return X_train, y_train

    def build_test_data(self, scope):
        self.testing_data = self.training_set_scaled[5086:]
        X_test = []
        y_test = []

        for i in range(scope, len(self.testing_data)):
            X_test.append(self.testing_data[i-scope: i, 0])
            y_test.append(self.testing_data[i, 0])
        X_test, y_test = np.array(X_test), np.array(y_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        y_test = np.reshape(y_test, (y_test.shape[0], 1))
        # print(X_test.shape)
        # print(self.testing_data.shape)
        return X_test, y_test

def regressor(X_train,y_train):
    keras.backend.clear_session()
    regressor = Sequential()

    regressor.add(LSTM(units = 16,
                    batch_input_shape = (1 ,X_train.shape[1], 1),
                    stateful= True
                    ))
    
    regressor.add(Dense(units = 1))
    regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')
    regressor.fit(X_train, y_train, epochs = 10, batch_size = 1)
    regressor.save('lstm.h5')
    return regressor

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="../data/consumption.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="../data/generation.csv", help="input the generation data path")
    args = parser.parse_args()
    
    sc = MinMaxScaler(feature_range = (0, 1))       #Data scaler
    training_scope = 15                             #We use path 15 hours value to predict the next hour
    feature_num = 0                                 #We choose the one feature(consumption) as training data
    ### Load Data
    load_data = preprocessing(args.consumption)
    load_data.data_load()
    load_data.select_feature(feature_num)
    load_data.data_scaler(sc, 0, inverse = False)
    X_train, y_train = load_data.build_train_data(training_scope)
    X_test, y_test = load_data.build_test_data(training_scope)
    y_test = load_data.data_scaler(sc,y_test,inverse=True)

    ### predicted consumption
    regressor(X_train,y_train)
    model = keras.models.load_model("lstm.h5")
    predicted_result  = model.predict(X_test, batch_size = 1)
    predicted_result = load_data.data_scaler(sc, predicted_result, inverse = True)
    print(predicted_result)
    plt.plot(predicted_result, color = 'red', label = 'predict')
    plt.plot(y_test, color = 'black', label = 'ans')
    plt.legend()
    plt.show()