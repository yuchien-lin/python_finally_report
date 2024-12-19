import numpy as np  #用來進行數值運算
def pearson_correlation(data1,data2):
  n=len(data1)

  #計算平均數
  mean_data1 = sum(data1) / n
  mean_data2 = sum(data2) / n
  #計算標準差
  std_data1 = (sum((data1[i] - mean_data1) ** 2 for i in range(n)) / n)**0.5
  std_data2 = (sum((data2[i] - mean_data2) ** 2 for i in range(n)) / n)**0.5
  #計算z-score
  z_data1 = [(data1[i] - mean_data1) / std_data1 for i in range(n)]
  z_data2 = [(data2[i] - mean_data2) / std_data2 for i in range(n)]

  #計算pearson correlation
  pearson=sum(z_data1[i] * z_data2[i] for i in range(n)) / n
  #若分母為零，表示兩者無變異，即pearson相關係數為0
  if std_data1 == 0 or std_data2 == 0:
    return 0
  return pearson

#動態時間規劃(DTW)
np.set_printoptions(precision=10)

def euclidean_distance(num1, num2):   #計算歐氏距離
  return np.sqrt((num1 - num2)**2)    #兩值相減的絕對值->創建矩陣距離，所以euclidean_distance()是距離矩陣

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
