import matplotlib.pyplot as plt
import numpy as np

def show_stock_chart(date,all_price,all_stock_name,data_num):  # 傳入資料
    plt.figure(figsize=(10, 6))               # 設定圖表大小
    plt.title("Stock Chart")                  # 設圖表標籤
    plt.xlabel("Date")                        # 設置X標籤
    plt.ylabel("Close Price")                 # 設置Y標籤

    for order in range (data_num):
        plt.scatter(date, all_price[order], s = 2, marker = 'o', label=all_stock_name[order]) #畫散布圖 點的大小設為2
        everyday_order = np.array([x for x in range(len(date))])
        price = np.array(all_price[order])
        coeffs = np.polyfit(everyday_order, price, 1)                           # 一次回歸，返回斜率和截距
        regression_line = coeffs[0] * everyday_order + coeffs[1]                # y = mx + b
        plt.plot(date, regression_line, linestyle='-',linewidth=7, alpha=0.4)   # 繪製回歸線

    # 設圖例邊框、圖例背景為白色、圖例邊框為黑色、字體大小
    plt.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='black', fontsize=8)
    plt.grid(True)   #開啟網格線，比較好看
    plt.show()
