import data_processor
import trend_comparison
import visualization
import csv
class stock_integrate():
    def __init__(self,stock_name,start_date,end_date):                                  #初始化此object
        self.start_date = start_date                                                    # 將開始取得股票的日期存為此class屬性
        self.end_date = end_date                                                        # 將結束取得股票的日期存為此class屬性
        stock_data = data_processor.stock_data(stock_name,start_date,end_date)          # 用data_processor中的stock_data產生的股票資訊的object
        self.stock_num = 1                                                              # 讀取股票股票數量存成此class的屬性
        self.stock_date = stock_data.stock_data_collect['date']                         # 將股票資訊object中的股價日期取出來並存成此class的屬性
        self.all_stock_price = []                                                       # 用來存取每個收盤價以二維的形式存成此class的屬性
        self.all_stock_name = []                                                        # 將每一個股票的名稱存進此class物件的list
        self.all_stock_price.append(stock_data.stock_data_collect['close_price'])       # 將起始股票的價格已list的形式存進價格的lsit形成二微陣列
        self.all_stock_name.append(stock_name)                                          # 將起始股價名稱存進list
        self.similarities_matrix = []                                                   # 用來存取每一個股票比較後pearson以及dtw的數值
        self.similarities_matrix.append(["stock1","stock2","pearson_correlation","dtw_distance"])   # 將比較的說明列打上去
        self.max_pearson_correlation = []                                               # 將最大pearson的兩個股票名稱存為此class屬性
        self.min_pearson_correlation = []                                               # 將最小pearson的兩個股票名稱存為此class屬性
        self.max_min_pearson_value = [-1,1]                                             # 將最大及最小pearson的數值存為此class屬性，前者為最大後者為最小
        self.max_dtw_distance =[]                                                       # 將最大dtw的兩個股票名稱存為此class屬性
        self.min_dtw_distance = []                                                      # 將最小dtw的兩個股票名稱存為此class屬性
        self.max_min_dtw_value = [0,2**31]                                              # 將最大及最小dtw的數值存為此class屬性，前者為最大後者為最小
        self.all_dtw = []                                                               # 用來儲存所有原始的dtw
        self.dtw_sqrt = 0                                                               # 用來儲存所有原始的dtw平方的和
        self.dtw_sum = 0                                                                # 用來儲存dtw的和


        def add_stock(self,stcok_name):                                                              # 輸入名稱增加股票
        new_stock_data = data_processor.stock_data(stock_name,self.start_date,self.end_date)     # 獲得股票資料
        self.stock_num += 1                                                                      # 股票數量加1
        self.all_stock_price.append(new_stock_data.stock_data_collect['close_price'])            # 將收盤價存進屬性的收盤價list
        self.all_stock_name.append(stock_name)                                                   # 將名稱存進屬性的名稱list
        for order in range(self.stock_num-1):                                                    # 進行比較股價的pearson及dtw
          compare = [self.all_stock_name[order],stock_name]                                      # 先將要比的股價名稱存進list
          pearson_value = self.get_pearson_correlation(self.all_stock_name[order],stock_name)    # 獲得pearson值
          if(pearson_value > self.max_min_pearson_value[0]):                                     # 改變最大值，並將股票名稱存入
              self.max_min_pearson_value[0] = pearson_value
              self.max_pearson_correlation = compare
          if(pearson_value < self.max_min_pearson_value[1]):                                     # 改變最小值，並將股票名稱存入
              self.max_min_pearson_value[1] = pearson_value
              self.min_pearson_correlation = compare
          compare.append(pearson_value)                                                          # 將兩個股票的pearson加進list裡面
          dtw_value = self.get_dtw_distance(self.all_stock_name[order],stock_name)               # 獲得dtw值
          self.all_dtw.append(dtw_value)                                                         # 儲存所有原始的dtw值
          self.dtw_sum += dtw_value                                                              # 更新原始dtw的總和
          self.dtw_sqrt += dtw_value**2                                                          # 更新原始dtw平方總和
          dtw_average = self.dtw_sum / self.stock_num                                            # 計算原始dtw總和的平均
          dtw_var = (self.dtw_sqrt/self.stock_num - dtw_average**2)**0.5                         # 計算原始dtw的標準差
          dtw_value = (dtw_value - dtw_average)/dtw_var                                          # 標準化dtw
          dtw_value = round(dtw_value,3)                                                         # 取值到小數點第三位
          compare.append(dtw_value)                                                              # 將標準化的dtw加進list裡面
          self.similarities_matrix.append(compare)                                               # 將新的股票與之前輸入的股票計算的pearson以及dtw儲存
          self.max_min_dtw_value = [0,2**31]                                                     # 重新計算標準化後dtw的最大值以及最小值
          for i in range(len(self.all_dtw)):                                                     # 開始比較
            dtw_value = round((self.all_dtw[i] - dtw_average)/dtw_var , 3)                       # 將之前存入的dtw重新計算他們的標準化
            self.similarities_matrix[i+1][3] = dtw_value                                         # 將計算結果蓋過之前的數值
            if(dtw_value > self.max_min_dtw_value[0]):                                           # 改變最大值，並將股票名稱存入
              self.max_min_dtw_value[0] = dtw_value
              self.max_dtw_distance = self.similarities_matrix[i+1][0:2]
            if(dtw_value < self.max_min_dtw_value[1]):                                           # 改變最小值，並將股票名稱存入
              self.max_min_dtw_value[1] = dtw_value
              self.min_dtw_distance = self.similarities_matrix[i+1][0:2]
              # 將這兩個股票的關係存進class的similarities_matrix屬性



    def show_stock_chart(self):                      # 展示股價的散布點圖
        visualization.show_stock_chart(self.stock_date,self.all_stock_price,self.all_stock_name,self.stock_num)
    def find_index(self,stock1_name,stock2_name):
        stock1_index = -1                                                             # 用來找股票名稱對應的收盤價存在哪個index
        stock2_index = -1
        for name_order in range(self.stock_num):                                      # 遍布每一個名字來尋找
            if(self.all_stock_name[name_order] == stock1_name):                       # 相同名稱就將位置存起來
                stock1_index = name_order
            elif(self.all_stock_name[name_order] == stock2_name):
                stock2_index = name_order
        if(stock1_index == -1 or stock2_index == -1):                                 # 其中一個股票名稱有誤
            if(stock1_index == -1 and stock2_index == -1):                            # 兩個都是錯的
                print("your first stock and second stock is wrong name",end = " ")
            elif(stock1_index == -1):                                                 # 第一個是錯的
                print("your first stock is wrong name",end = " ")
            else:                                                                     # 只有第二個是錯的
                print("your second stock is wrong name",end = " ")
            print("please input again!")
            return -1,-1
        return stock1_index,stock2_index

    def get_pearson_correlation(self,stock1_name,stock2_name):                     # 獲得兩個股票的pearson的值
        stock1_index,stock2_index = self.find_index(stock1_name,stock2_name)       # 獲得兩支股票的index
        if(stock1_index == -1):                                                    # 兩個股票其中一個名稱錯誤
          return -1
        pearson_val = trend_comparison.pearson_correlation(self.all_stock_price[stock1_index],self.all_stock_price[stock2_index]) 
        #透過trend_comparison內的pearson_correlation來獲得pearson的值
        return round(pearson_val,3)


    def get_dtw_distance(self,stock1_name,stock2_name):                        # 獲得兩個股票的dtw的值
        stock1_index,stock2_index = self.find_index(stock1_name,stock2_name)   # 獲得兩支股票的index
        if(stock1_index == -1):                                                # 兩個股票其中一個名稱錯誤
          return -1
        dtw_value = trend_comparison.dtw_distance(self.all_stock_price[stock1_index],self.all_stock_price[stock2_index])
        return dtw_value

    def print_similarities_matrix(self):          #印出pearson及dtw最大最小的值
        for row in self.similarities_matrix:
          print(row)
        print("max pearson correltion is",self.max_pearson_correlation[0],"and",self.max_pearson_correlation[1],self.max_min_pearson_value[0])
        print("min pearson correltion is",self.min_pearson_correlation[0],"and",self.min_pearson_correlation[1],self.max_min_pearson_value[1])
        print("max dtw distance is",self.max_dtw_distance[0],"and",self.max_dtw_distance[1],self.max_min_dtw_value[0])
        print("min dtw distance is",self.min_dtw_distance[0],"and",self.min_dtw_distance[1],self.max_min_dtw_value[1])

    def create_similarities_csv(self):            #將每一個比較的結果輸出成csv檔出去
        with open('similarities.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(self.similarities_matrix)
            writer.writerow(["max pearson correltion is",self.max_pearson_correlation[0],"and",self.max_pearson_correlation[1],self.max_min_pearson_value[0]])
            writer.writerow(["min pearson correltion is",self.min_pearson_correlation[0],"and",self.min_pearson_correlation[1],self.max_min_pearson_value[1]])
            writer.writerow(["max dtw distance is",self.max_dtw_distance[0],"and",self.max_dtw_distance[1],self.max_min_dtw_value[0]])
            writer.writerow(["min dtw distance is",self.min_dtw_distance[0],"and",self.min_dtw_distance[1],self.max_min_dtw_value[1]])

stock_compare = stock_integrate('2330.TW','2021-01-01','2024-01-01')
stock_compare.add_stock('2454.TW')
stock_compare.add_stock('2002.TW')
stock_compare.show_stock_chart()
stock_compare.print_similarities_matrix()
stock_compare.create_similarities_csv()
