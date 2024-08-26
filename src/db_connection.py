import sqlite3

def connect_to_db(db_name):
    """データベースに接続し、接続オブジェクトを返す"""
    return sqlite3.connect(db_name)
