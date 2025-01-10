import yfinance as yf

class stock_data:
    def __init__(self,stcok_name,start_date,end_date):
        all_data = yf.download(stcok_name,start_date,end_date,auto_adjust=False,prepost=False)    #利用套件獲得股票部分資訊
        all_data.reset_index(inplace=True)                                                        #將日期從index轉成一欄的值
        self.stock_data_collect = {"date":[] ,"close_price": [] }                                 #創建一個字典屬性在此class
        self.stock_data_collect["close_price"] = all_data['Close'][stcok_name]                    #將收盤價存進字典對應位置
        self.stock_data_collect["date"] = all_data['Date'].dt.date.tolist()                       #將日期那欄轉成list

