import sqlite3

def check_columns(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # テーブルの構造を確認
    cursor.execute("PRAGMA table_info(products)")
    columns = cursor.fetchall()
    
    for column in columns:
        print(column)
    
    conn.close()

# データベース名を指定してスキーマを確認
check_columns('product_database.db')


