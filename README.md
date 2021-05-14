# DSAI-HW3
綠能交易

# Data analysis & Training Data
選擇使用target0的產電與用電資料，並分別預測產電量generation與用電量consumption

我們發現用電量在某些月份並不會太高，像是冬天春天，但是在6~8月之後用電量突增。
![4line](https://github.com/linzh0205/DSAI-HW3/blob/main/fig/fig_out0.png)

在發電量我們發現在某些時段發電量較少，像是晚上到凌晨時段。另外也發現每個agant發電量都差不多，圖中橘色與藍色為不同agant。
![4line](https://github.com/linzh0205/DSAI-HW3/blob/main/fig/fig1.png)


# Method & Model training
以LSTM模型訓練產電量與用電量，輸入過去7天(2018/9/1~9/30)共168小時的用電量與產電量預測未來一天24小時用電量與產電量。

發電量的預測結果如下圖。
![4line](https://github.com/linzh0205/DSAI-HW3/blob/main/fig/Figure_1.png)


# Trader Strategy
計算預測的用電量與產電量之間的差值，當用電量大於產電量表示不法自給自足電量，需要購買電來補足所需電量，接著會我們會出價2塊去平台買電。
反之用電量小於產電量表示產電是足夠給自己用的，但是我們選擇不交易。
