import sqlite3
import pandas as pd

# Excelファイルからデータを読み込む
file_path = r'C:\Users\rc240\Desktop\app\my_project\x001247592.xlsx'  # ファイルのパスに変更してください
sheet_name = '厚労省マスタ'  # 例としてシート名を指定
df = pd.read_excel(file_path, sheet_name=sheet_name)

# 必要な列を選択する
df_filtered = df[['品名', '長期収載品と後発医薬品の価格差の４分の１']]

# SQLiteデータベースに接続（存在しない場合は作成）
conn = sqlite3.connect('product_database.db')
cursor = conn.cursor()

# 既存のテーブルを削除して再作成（データが上書きされる点に注意）
cursor.execute("DROP TABLE IF EXISTS products")

# テーブルを再作成
cursor.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price_difference REAL
)
''')

# データをデータベースに挿入
for index, row in df_filtered.iterrows():
    cursor.execute("INSERT INTO products (name, price_difference) VALUES (?, ?)", (row['品名'], row['長期収載品と後発医薬品の価格差の４分の１']))

# コミットして接続を閉じる
conn.commit()
conn.close()

print("データがデータベースに保存されました。")
