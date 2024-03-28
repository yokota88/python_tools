import sqlite3
import pandas as pd

class StockSqlite:
  def __init__(self, db_path):
    self.db_path = db_path

  # コネクションを取得する関数
  def get_db(self):
      db = sqlite3.connect(self.db_path)
      return db
  
  def get_data(self, symbol):
      try:
          with self.get_db() as conn:
              cursor = conn.cursor()
              
              # 降順で1000個取得して昇順に並べ替え
              cursor.execute("""
                  SELECT * FROM (
                      SELECT * FROM stock_data WHERE symbol = ? ORDER BY date DESC LIMIT 1000
                  ) ORDER BY date ASC;
              """, (symbol,))            
              
              data = cursor.fetchall()
              columns = [desc[0] for desc in cursor.description]

          result = []
          for row in data:
              result.append(dict(zip(columns, row)))
          
          df = pd.DataFrame(result)
          df["date"] = pd.to_datetime(df["date"])
          df = df.set_index("date")
          df["date"] = df.index
          return df
      
      except Exception as e:
          # エラーメッセージを表示
          print("Error:", e)
          return pd.DataFrame()

  @staticmethod
  def convertToFlat(data):
    pass