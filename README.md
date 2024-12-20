> ### 主題目標：輸入三支股票，使用**Pearson相關係數**及**動態時間規劃**比較股票趨勢相似性。
1. 輸入股票的日收盤價資料，時間範圍相同。
2. Pearson相關係數：計算兩支股票的Pearson相關係數，衡量兩者的趨勢相似程度。
3. 動態時間規劃：使用動態時間規劃衡量不同時間序列的匹配程度。
4. 視覺化展示：繪製三支股票的趨勢走勢圖，並附上其對應的相似性指標數值。
5. 成果展示：運用兩種方法進行股票走勢分析，並提供結論

> ### 目錄
1. 數據分析工具介紹
2. 程式碼撰寫
3. 結論

> ### 資料抓取
從yahoo財經擷取股票資料
```python
!pip install yfinance
```
```python
import yfinance as yf
class stock_data:
     def __init__(self,stcok_name,start_date,end_date):
        all_data = yf.download(stcok_name,start_date,end_date)                      #利用套件獲得股票所有資訊
        all_data.reset_index(inplace=True)                                          #將日期從index轉成一欄的值
        self.stock_data_collect = {"date":[] ,"close_price": [] }                   #創建一個字典屬性在此class
        self.stock_data_collect["close_price"] = all_data['Close'][stcok_name]      #將收盤價存進字典對應位置
        self.stock_data_collect["date"] = all_data['Date'].dt.date.tolist()         #將日期那欄轉成list
```

> ### 數據分析工具介紹

1. **Pearson correlation coefficient**
- 驗證兩個標的之間的線性關係。常以r表示，且-１< r < 1 。
- | r | 越大，兩者相關程度越高；正負代表關係方向(類似斜率)

```python
import numpy as np  #用來進行數值運算
def pearson_correlation(data1,data2):
  n=len(data1)
```
計算相關數值
```python
  #計算平均數
  mean_data1 = sum(data1) / n
  mean_data2 = sum(data2) / n
  #計算標準差
  std_data1 = (sum((data1[i] - mean_data1) ** 2 for i in range(n)) / n)**0.5
  std_data2 = (sum((data2[i] - mean_data2) ** 2 for i in range(n)) / n)**0.5
  #計算z-score
  z_data1 = [(data1[i] - mean_data1) / std_data1 for i in range(n)]
  z_data2 = [(data2[i] - mean_data2) / std_data2 for i in range(n)]
```
計算pearson correlation
```python
  pearson=sum(z_data1[i] * z_data2[i] for i in range(n)) / n
  #若分母為零，表示兩者無變異，即pearson相關係數為0
  if std_data1 == 0 or std_data2 == 0:
    return 0
  return pearson
```

2. **Dynamic Time Warping**
- 用於計算兩個時間序列的相似度，即使在兩個擁有不同長度或節奏的時間序列下也適用。
- 也就是說，動態時間規劃在比較兩個時間序列時，允許它們在時間軸上進行局部縮放，以找出最佳對齊方式。
- 計算得出的結果越小，表示兩者趨勢越相似。


```python
def euclidean_distance(a, b):                               #計算歐氏距離
  return np.abs(a - b)                                      #兩值相減的絕對值->創建矩陣距離，所以euclidean_distance()是距離矩陣

def dtw_distance(data1, data2):                             #計算DTW距離
  len_data1, len_data2 = len(data1), len(data2)             #把第一條序列的長度指派給變數n，第二條序列的長度指派給變數m

  matrix_dtw = np.zeros((len_data1, len_data2))             #累積距離矩陣的大小為n乘以m,指派給變數C，所以C是累積距離矩陣
  matrix_dtw[0,0] = euclidean_distance(data1[0], data2[0])  #初始化矩陣，計算第一個元素的距離

  for i in range(1, len_data1):                             #初始化第一列
    matrix_dtw[i, 0] = matrix_dtw[i-1, 0] + euclidean_distance(data1[i], data2[0])
    #第一列的每個元素累積的距離＝從上一個累積下來的累積距離矩陣＋這一個的距離矩陣(只有i變化，j固定在位置0）

  for j in range(1, len_data2):                             #初始化第一行
    matrix_dtw[0, j] = matrix_dtw[0, j-1] + euclidean_distance(data1[0], data2[j])
    #第一行的每個元素累積的距離＝從上一個累積下來的累積距離矩陣＋這一個的距離矩陣(只有j變化，i固定在位置0）

  for i in range(1, len_data1):                             #會跑一遍序列一的所有元素
    for j in range(1, len_data2):                           #會跑一遍序列二的所有元素
      matrix_dtw[i, j] = euclidean_distance(data1[i], data2[j])+min(matrix_dtw[i-1, j],matrix_dtw[i, j-1],matrix_dtw[i-1, j-1])

      #序列series1的第i個元素與序列series2的第j個元素之間的歐式距離＋前一個位置（C[i-1, j],C[i, j-1],C[i-1, j-1])到目前位置C[i, j]的最小累積距離
      #C[i-1, j]序列series1[i-1]與序列series2[j]對齊
      #C[i, j-1]序列series1[i]與序列series2[j-1]對齊
      #C[i-1, j-1]序列series1[i-1]與序列series2[j-1]對齊
  return matrix_dtw[len_data1 - 1, len_data2 - 1]
```

> ### 散佈圖繪製

```python
import matplotlib.pyplot as plt

def show_stock_chart(data,all_price,all_stock_name,data_num):  # 傳入資料
    plt.figure(figsize=(10, 6))        # 設定圖表大小
    plt.title("Stock Chart")           # 設圖表標籤
    plt.xlabel("Date")                 # 設置X標籤
    plt.ylabel("Close Price")          # 設置Y標籤

    for order in range (data_num):
        plt.scatter(date, all_price[order], s = 2, marker = 'o', label=all_stock_name[order])#畫散布圖 點的大小設為2
        everyday_order = np.array([x for x in range(len(date))])
        price = np.array(all_price[order])
        coeffs = np.polyfit(everyday_order, price, 1)                                        # 一次回歸，返回斜率和截距
        regression_line = coeffs[0] * everyday_order + coeffs[1]  # y = mx + b
        plt.plot(date, regression_line, linestyle='-',linewidth=7, alpha=0.4)                # 繪製回歸線

    # 設圖例邊框、圖例背景為白色、圖例邊框為黑色、字體大小
    plt.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='black', fontsize=8)
    plt.grid(True)   #開啟網格線，比較好看
    plt.show()
```

> ### 實際應用
```python
!pip install import-ipynb
import import_ipynb
```
```
from google.colab import drive
drive.mount("/content/drive")
%cd '/content/drive/MyDrive/Colab Notebooks'
import data_processor
import trend_comparison
import visualization
import csv
```
初始化class所創建的object
```python
class stock_integrate():
    def __init__(self,stcok_name,start_date,end_date):             #初始化此object
        self.start_date = start_date                               # 將開始取得股票的日期存為此class屬性
        self.end_date = end_date                                   # 將結束取得股票的日期存為此class屬性
        stock_data = data_processor.stock_data(stcok_name,start_date,end_date)
        # 用data_processor中的stock_data產生的股票資訊的object
        self.stock_num = 1                                         # 讀取股票股票數量存成此class的屬性
        self.stock_date = stock_data.stock_data_collect['date']    # 將股票資訊object中的股價日期取出來並存成此class的屬性
        self.all_stock_price = []                                  # 用來存取每個收盤價以二維的形式存成此class的屬性
        self.all_stock_name = []                                   # 將每一個股票的名稱存進此class物件的list
        self.all_stock_price.append(stock_data.stock_data_collect['close_price'])
        # 將起始股票的價格已list的形式存進價格的lsit形成二微陣列
        self.all_stock_name.append(stcok_name)                     # 將起始股價名稱存進list
        self.similarities_matrix = []                              # 用來存取每一個股票比較後pearson以及dtw的數值
        self.similarities_matrix.append(["stock1","stock2","pearson_correlation","dtw_distance"])
        # 將比較的說明列打上去
        self.max_pearson_correlation = []                          # 將最大pearson的兩個股票名稱存為此class屬性
        self.min_pearson_correlation = []                          # 將最小pearson的兩個股票名稱存為此class屬性
        self.max_min_pearson_value = [-1,1]                        # 將最大及最小pearson的數值存為此class屬性，前者為最大後者為最小
        self.max_dtw_distance =[]                                  # 將最大dtw的兩個股票名稱存為此class屬性
        self.min_dtw_distance = []                                 # 將最小dtw的兩個股票名稱存為此class屬性
        self.max_min_dtw_value = [0,2**31]                         # 將最大及最小dtw的數值存為此class屬性，前者為最大後者為最小
```
增加股票的方法
```python
    def add_stock(self,stcok_name):            # 輸入名稱增加股票
        new_stock_data = data_processor.stock_data(stcok_name,self.start_date,self.end_date)
        # 獲得股票資料   
        self.stock_num += 1                                         # 股票數量加1
        self.all_stock_price.append(new_stock_data.stock_data_collect['close_price'])
        # 將收盤價存進屬性的收盤價list
        self.all_stock_name.append(stcok_name)                      # 將名稱存進屬性的名稱list
        for order in range(self.stock_num-1):                       # 進行比較股價的pearson及dtw
          compare = [self.all_stock_name[order],stcok_name]         # 先將要比的股價名稱存進list
          pearson_value = self.get_pearson_correlation(self.all_stock_name[order],stcok_name)
          # 獲得pearson值
          if(pearson_value > self.max_min_pearson_value[0]):        # 改變最大值，並將股票名稱存入
              self.max_min_pearson_value[0] = pearson_value                   
              self.max_pearson_correlation = compare                      
          if(pearson_value < self.max_min_pearson_value[1]):        # 改變最小值，並將股票名稱存入
              self.max_min_pearson_value[1] = pearson_value                   
              self.min_pearson_correlation = compare                      
          compare.append(pearson_value)                             # 將兩個股票的pearson加進list裡面
          dtw_value = self.get_dtw_distance(self.all_stock_name[order],stcok_name)
          # 獲得dtw值
          if(dtw_value > self.max_min_dtw_value[0]):                # 改變最大值，並將股票名稱存入
            self.max_min_dtw_value[0] = dtw_value                         
            self.max_dtw_distance = compare                            
          if(dtw_value < self.max_min_dtw_value[1]):                # 改變最小值，並將股票名稱存入
            self.max_min_dtw_value[1] = dtw_value
            self.min_dtw_distance = compare
          compare.append(dtw_value)                                 # 將兩個股票的dtw加進list裡面   
          self.similarities_matrix.append(compare)                  # 將這兩個股票的關係存進class的similarities_matrix屬性
```
畫出散布圖的方法
```python
    def show_stock_chart(self):                        # 展示股價的散布點圖
        visualization.show_stock_chart(self.stock_date,self.all_stock_price,self.all_stock_name,self.stock_num)
```
得到pearson correlation的方法
```python
    def get_pearson_correlation(self,stock1_name,stock2_name):      # 獲得兩個股票的pearson的值
        stock1_index = -1                                           # 用來找股票名稱對應的收盤價存在哪個index
        stock2_index = -1
        for name_order in range(self.stock_num):                    # 遍布每一個名字來尋找
            if(self.all_stock_name[name_order] == stock1_name):     # 相同名稱就將位置存起來
                stock1_index = name_order
            elif(self.all_stock_name[name_order] == stock2_name):
                stock2_index = name_order
        if(stock1_index == -1 or stock1_index == -1):               # 其中一個股票名稱有誤
            if(stock1_index == -1 and stock2_index == -1):          # 兩個都是錯的
                print("your first stock and second stock is wrong name",end = " ")
            elif(stock1_index == -1):                               # 第一個是錯的
                print("your first stock is wrong name",end = " ")
            else:                                                   # 只有第二個是錯的
                print("your second stock is wrong name",end = " ")
            print("please input again!")
            return                                    
        pearson_val = trend_comparison.pearson_correlation(self.all_stock_price[stock1_index],self.all_stock_price[stock2_index])
        #透過trend_comparison內的pearson_correlation來獲得pearson的值
        return round(pearson_val,3)
```
得到dtw distance的方法
```python                                                                                           
   def get_dtw_distance(self,stock1_name,stock2_name):          # 獲得兩個股票的pearson的值
        stock1_index = -1                                       # 用來找股票名稱對應的收盤價存在哪個index
        stock2_index = -1
        for name_order in range(self.stock_num):                # 遍布每一個名字來尋找
            if(self.all_stock_name[name_order] == stock1_name): # 相同名稱就將位置存起來
                stock1_index = name_order
            elif(self.all_stock_name[name_order] == stock2_name):
                stock2_index = name_order
        if(stock1_index == -1 or stock1_index == -1):           # 其中一個股票名稱有誤
            if(stock1_index == -1 and stock2_index == -1):      # 兩個都是錯的
                print("your first stock and second stock is wrong name",end = " ")
            elif(stock1_index == -1):                           # 第一個是錯的
                print("your first stock is wrong name",end = " ")
            else:                                               # 只有第二個是錯的
                print("your second stock is wrong name",end = " ")
            print("please input again!")
            return
        dtw_value = trend_comparison.dtw_distance(self.all_stock_price[stock1_index][:(len(self.all_stock_price[stock1_index])//2)],self.all_stock_price[stock2_index])
        #dtw 只傳一半的數據，因為dtw能算不同長度的數據
        return round(dtw_value,3)
```
印出所有股票互相的 pearson correlation 以及 dtw distance 並印出pearson及dtw最大最小的值
```python
    def print_similarities_matrix(self):        #印出pearson及dtw最大最小的值
        for row in self.similarities_matrix:
            print(row)
        print("max pearson correltion is",self.max_pearson_correlation[0],"and",self.max_pearson_correlation[1],self.max_min_pearson_value[0])
        print("min pearson correltion is",self.min_pearson_correlation[0],"and",self.min_pearson_correlation[1],self.max_min_pearson_value[1])
        print("max dtw distance is",self.max_dtw_distance[0],"and",self.max_dtw_distance[1],self.max_min_dtw_value[0])
        print("min dtw distance is",self.min_dtw_distance[0],"and",self.min_dtw_distance[1],self.max_min_dtw_value[1])
```
將所有股票互相的 pearson correlation 以及 dtw distance 並印出pearson及dtw最大最小的值寫成csv檔
```python
    def create_similarities_csv(self):         #將每一個比較的結果輸出成csv檔出去
        with open('similarities.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.similarities_matrix)
            writer.writerow(["max pearson correltion is",self.max_pearson_correlation[0],"and",self.max_pearson_correlation[1],self.max_min_pearson_value[0]])
            writer.writerow(["min pearson correltion is",self.min_pearson_correlation[0],"and",self.min_pearson_correlation[1],self.max_min_pearson_value[1]])
            writer.writerow(["max dtw distance is",self.max_dtw_distance[0],"and",self.max_dtw_distance[1],self.max_min_dtw_value[0]])
            writer.writerow(["min dtw distance is",self.min_dtw_distance[0],"and",self.min_dtw_distance[1],self.max_min_dtw_value[1]])
```
成果展示
```python
stock_compare = stock_integrate('2330.TW','2021-01-01','2024-01-01')
stock_compare.add_stock('2454.TW')
stock_compare.add_stock('2002.TW')
stock_compare.show_stock_chart()
stock_compare.print_similarities_matrix()
stock_compare.create_similarities_csv()

```
![image](https://github.com/user-attachments/assets/1b4e49e9-b168-417e-824d-3040169ac1cd)
> ### 結論
**結論 :**​
Pearson相關係數越大，DTW值越小 。股票可能受到類似市場因素的影響，因此其趨勢表現非常接近。​
**分析:​**
DTW 可以比較長度不同的序列，這使得它特別適合於處理不規則的數據或不等長的時間序列，且適用度較廣泛 如 : 語音信號、生物數據（如心跳或腦電波）、圖像特徵等各種數據。​
Pearson相關係數是一個無單位的純數字，樣本數量較少時，Pearson相關係數的估計可能不穩定，需要足夠的數據來獲得可靠的結果，可應用於:金融分析、心理學、與教育醫學研究、市場分析​

