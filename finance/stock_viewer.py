import plotly.graph_objects as go
from plotly.subplots import make_subplots

import pandas as pd
from datetime import datetime
import plotly.io as pio
pio.renderers.default = 'vscode' #1回設定しておけばいい！
import datetime as dt

class StockViewer:
  def __init__(self, df):
    self.df = df
    
  def getFigure(self, drop_breaks = False):
    df = self.df
    
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_width=[0.2, 0.7], x_title="Date")
    fig.add_trace(
        go.Candlestick(x=df.index,
                    open=df['open'],
                    high=df['high'],
                    low=df['low'],
                    close=df['close']),
                    row=1, col=1
    )

    fig.add_trace(go.Scatter(x=df.index, y=df["ema50"], name="EMA50", mode="lines"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["ema100"], name="EMA100", mode="lines"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df["ema200"], name="EMA200", mode="lines"), row=1, col=1)

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
  
  def getFigureDayWeekMonth(self, df_day, df_week, df_month):    
    # Base
    fig = make_subplots(rows=2, cols=2, shared_xaxes=True, vertical_spacing=0.05, row_width=[0.2, 0.7], x_title="Date")
    fig.update(layout_xaxis_rangeslider_visible=False) #追加

    # Day
    fig.add_trace(
        go.Candlestick(x=df_day.index,
                    open=df_day['open'],
                    high=df_day['high'],
                    low=df_day['low'],
                    close=df_day['close']),
                    row=1, col=1
    )

    fig.add_trace(go.Scatter(x=df_day.index, y=df_day["ema50"], name="EMA50", mode="lines"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_day.index, y=df_day["ema100"], name="EMA100", mode="lines"), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_day.index, y=df_day["ema200"], name="EMA200", mode="lines"), row=1, col=1)
    
    # # 株価データの日付データに含まれていない日付を抽出
    # d_all = pd.date_range(start=df_day.index[0],end=df_day.index[-1])
    # d_obs = [d.strftime('%Y-%m-%d') for d in df_day.index]
    # d_breaks = [d for d in d_all.strftime("%Y-%m-%d").tolist() if not d in d_obs]

    # fig.update_xaxes(
    #     rangebreaks=[dict(values=d_breaks)], # 非営業日を非表示設定
    #     tickformat='%Y/%m/%d' # 日付のフォーマット変更
    # )
    
    # # Week
    # fig.add_trace(
    #     go.Candlestick(x=df_week.index,
    #                 open=df_week['open'],
    #                 high=df_week['high'],
    #                 low=df_week['low'],
    #                 close=df_week['close']),
    #                 row=2, col=1
    # )

    # fig.add_trace(go.Scatter(x=df_week.index, y=df_week["ema50"], name="EMA50", mode="lines"), row=2, col=1)
    # fig.add_trace(go.Scatter(x=df_week.index, y=df_week["ema100"], name="EMA100", mode="lines"), row=2, col=1)
    # fig.add_trace(go.Scatter(x=df_week.index, y=df_week["ema200"], name="EMA200", mode="lines"), row=2, col=1)

    # Month
    fig.add_trace(
        go.Candlestick(x=df_month.index,
                    open=df_month['open'],
                    high=df_month['high'],
                    low=df_month['low'],
                    close=df_month['close']),
                    row=2, col=2
    )

    fig.add_trace(go.Scatter(x=df_month.index, y=df_month["ema50"], name="EMA50", mode="lines"), row=2, col=2)
    fig.add_trace(go.Scatter(x=df_month.index, y=df_month["ema100"], name="EMA100", mode="lines"), row=2, col=2)
    fig.add_trace(go.Scatter(x=df_month.index, y=df_month["ema200"], name="EMA200", mode="lines"), row=2, col=2)



    # fig.update_layout(
    #     title_text="Candle",
    #     xaxis=dict(
    #         rangeslider=dict(
    #             visible=False
    #         ),
    #         type="date"
    #     ),
    # )


    return fig