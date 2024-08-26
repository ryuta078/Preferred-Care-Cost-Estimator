import sqlite3

def show_all_data(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()

    for row in rows:
        print(row)

    # データベース接続を閉じる
    conn.close()

# データベース名を指定して内容を確認
show_all_data('product_database.db')
