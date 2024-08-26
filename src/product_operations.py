def get_product_price(conn, product_name):
    """
    指定された製品名に基づいてデータベースから価格を取得する
    :param conn: データベース接続オブジェクト
    :param product_name: 検索する製品名
    :return: 製品の価格またはNone
    """
    cursor = conn.cursor()
    cursor.execute("SELECT price_difference FROM products WHERE name = ?", (product_name,))
    result = cursor.fetchone()

    if result:
        return result[0]  # 価格を返す
    else:
        return None  # 製品が見つからなかった場合はNoneを返す


def get_product_names(conn, search_term):
    cursor = conn.cursor()
    search_term = f"%{search_term}%"
    cursor.execute("SELECT name FROM products WHERE name LIKE ?", (search_term,))
    results = cursor.fetchall()
    return [row[0] for row in results]