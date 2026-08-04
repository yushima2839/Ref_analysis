import sqlite3
import pandas

# csvファイルのデータを取得
data = pandas.read_csv("results_2023_J1_demo.csv")


# sqlに接続
con = sqlite3.connect("jleague_Match_Results.db")

# insert実行
data.to_sql(
    "results_J1",        # 挿入先テーブル
    con,
    if_exists="append", 
    index=False          
)

con.close