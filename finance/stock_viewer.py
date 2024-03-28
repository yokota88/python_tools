import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
from datetime import datetime
import plotly.io as pio
pio.renderers.default = 'vscode' #1回設定しておけばいい！
import datetime as dt

class StockViewer:
  def __init__(self, df=pd.DataFrame(), drop_breaks=False):
    self.fig = self.create(df, drop_breaks)
    return
  
  def show(self):
    return self.fig.show()
  
  def create(self, df=pd.DataFrame(), drop_breaks = False):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_width=[0.2, 0.7], x_title="Date")
    fig.add_trace(
        go.Candlestick(x=df.index,
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close']),
                    row=1, col=1
    )

    colms = df.columns.values
    extract_col = "indicator_"
    for col in colms:
      if extract_col in col:
        target_col = col.replace(extract_col, "")
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=target_col, mode="lines"), row=1, col=1)

    fig.update_layout(
        title_text="Candle",
        xaxis=dict(
            rangeslider=dict(
                visible=False
            ),
            type="date"
        ),
    )

    # Volume
    fig.add_trace(
        go.Bar(x=df.index, y=df["volume"], showlegend=False),
        row=2, col=1
    )

    if(drop_breaks):
      # 株価データの日付データに含まれていない日付を抽出
      d_all = pd.date_range(start=df.index[0],end=df.index[-1])
      d_obs = [d.strftime('%Y-%m-%d') for d in df.index]
      d_breaks = [d for d in d_all.strftime("%Y-%m-%d").tolist() if not d in d_obs]

      fig.update_xaxes(
          rangebreaks=[dict(values=d_breaks)], # 非営業日を非表示設定
          tickformat='%Y/%m/%d' # 日付のフォーマット変更
      )

    return fig
  