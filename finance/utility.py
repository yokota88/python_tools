import pandas as pd
import numpy as np

agg_dict = {
    "open": "first", 
    "high": "max",
    "low": "min",
    "close": "last",
    "volume": "sum"
}
class Utility:
  def __init__(self):
    pass

  @staticmethod
  def convertToFlat(data):
    return [item for sublist in data.tolist() for item in sublist]
  
  @staticmethod
  def convertToWithoutNan(data):
    return [None if np.isnan(x) else x for x in data]
  

  @staticmethod
  def calcSMA(data, window_size):
    return data.rolling(window_size).mean()

  @staticmethod
  def calcEMA(data, window_size):
    return data.ewm(span=window_size, adjust=False).mean()

  @staticmethod
  def toWeekly(data):
    out = data.set_index("date").resample("W").agg(agg_dict)
    out["date"] = out.index
    return out
  
  @staticmethod
  def toMonthly(data):
    out = data.set_index("date").resample("ME").agg(agg_dict)
    out["date"] = out.index
    return out
  
  @staticmethod
  def calcIndicator(df, types):
    df_out = pd.DataFrame()
    for k, v in types.items():
      if(k.lower()=="sma"):
        for span in v:
          col_name = 'indicator_sma' + str(span)
          df_out[col_name] = Utility.calcSMA(data=df, window_size=span)
          
      elif(k.lower()=="ema"):
        for span in v:
          col_name = 'indicator_ema'+ str(span)
          df_out[col_name] = Utility.calcEMA(data=df, window_size=span)
        
    return df_out