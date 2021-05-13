
# consumption:耗電 generation:產電
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import keras
from sklearn.preprocessing import MinMaxScaler 

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

def output(path, data):
    import pandas as pd

    df = pd.DataFrame(data, columns=["time", "action", "target_price", "target_volume"])
    df.to_csv(path, index=False)

    return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--consumption", default="../data/consumption_2.csv", help="input the consumption data path")
    parser.add_argument("--generation", default="./sample_data/generation.csv", help="input the generation data path")
    parser.add_argument("--bidresult", default="./sample_data/bidresult.csv", help="input the bids result path")
    parser.add_argument("--output", default="output.csv", help="output the bids path")

    args = parser.parse_args()

    sc = MinMaxScaler(feature_range = (0, 1))       #Data scaler
    training_scope = 15                             #We use path 15 hours value to predict the next hour
    feature_num = 0                                 #We choose the one feature(consumption) as training data
    
    load_data = preprocessing(args.consumption)
    load_data.data_load()
    load_data.select_feature(feature_num)
    load_data.data_scaler(sc, 0, inverse = False)

    model = keras.models.load_model("lstm.h5")
    X_test, y_test = load_data.build_test_data(training_scope)

    predicted_result  = model.predict(X_test, batch_size = 1)
    predicted_result = load_data.data_scaler(sc, predicted_result, inverse = True)
    print(predicted_result)

    # data = [["2021-05-11 00:00:00", "buy", 2.5, 3],
    #         ["2021-05-11 01:00:00", "sell", 3, 5],
    #         ["2021-05-11 02:00:00", "buy", 1.2, 2],
    #         ["2021-05-11 03:00:00", "buy", 1.6, 2],
    #         ["2021-05-11 04:00:00", "sell", 3, 5],
    #         ["2021-05-11 05:00:00", "sell", 3, 7],
    #         ["2021-05-11 06:00:00", "buy", 2.5, 3],
    #         ["2021-05-11 07:00:00", "sell", 3, 5],
    #         ["2021-05-11 08:00:00", "buy", 1.2, 2],
    #         ["2021-05-11 09:00:00", "buy", 1.6, 2],
    #         ["2021-05-11 10:00:00", "sell", 3, 5],
    #         ["2021-05-11 11:00:00", "sell", 3, 7]]
    # output(args.output, data)
    # print("done")
