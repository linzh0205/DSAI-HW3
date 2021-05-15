# DSAI-HW3
綠能交易

# Data analysis & Training Data
選擇使用target0的產電與用電資料，並分別預測產電量generation與用電量consumption

我們發現用電量在某些月份並不會太高，像是冬天春天(1~5月)，但是在6~8月之後用電量突增

可以推斷出9/1~30用電量會跟8月的差不多且會稍微上升

![4line](https://github.com/linzh0205/DSAI-HW3/blob/main/fig/fig_out0.png)

在發電量我們發現在某些時段發電量較少，像是晚上到凌晨時段。另外也發現每個agant發電量都差不多，圖中橘色與藍色為不同agant

而且發電量與用電量比較後，在6~8月時期發電量都是不足的

![4line](https://github.com/linzh0205/DSAI-HW3/blob/main/fig/fig1.png)


# Method & Model training
以LSTM模型訓練產電量與用電量，輸入過去7天(2018/9/1~9/30)共168小時的用電量與產電量預測未來一天24小時用電量與產電量

我們發現在8點~18點的發電量較高不過在其餘時段發電量幾乎為零，所以只留下發電量較高的11小時進行預測，並在預測完後將幾乎為零的發電量時段補回時間序列中

發電量的預測結果如下圖

![4line](https://github.com/linzh0205/DSAI-HW3/blob/main/fig/Figure_1.png)

用電量預測結果如下圖

![4line](https://github.com/linzh0205/DSAI-HW3/blob/main/fig/consumption_result_2.png)

# Trader Strategy
預計是要計算預測的用電量與產電量之間的差值，當用電量大於產電量表示不法自給自足電量，需要購買電來補足所需電量，接著會我們會出價去平台買電

反之用電量小於產電量表示產電是足夠給自己用的，但是我們選擇不交易

不過我們發現在交易時必須精準的知道用電量與產電量之間的差值才能夠以不虧損的情況下補足電量

但是我們訓練出來的預測模型尚未能夠精準預測未來9/1~30的用電量與產電量

因此我們選擇使用保守的規則來進行電量的交易，目的是不出現浪費的電將電費降低

由先前可以知道24小時的用電量是差不多的，大概介於2至4(KW)，但是發電量僅在早上8點~19點共11小時才有明顯的產電

因此我們會在其餘時間買電，以target value = 2 target price=1.5交易，有發電的11小時不做交易


## Run the code
在pipenv環境下執行main.py
Python版本為:Python 3.8
```
pipenv install --python3.8
```
```
pipenv shell
```
安裝套件:
```
pipenv install requests
```

在pipenv下執行main.py:
```
pipenv run python main.py
```
