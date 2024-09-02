import streamlit as st
import unicodedata
from src.db_connection import connect_to_db
from src.product_operations import get_product_price, get_product_names
from src.calculation import calculate_medical_points

# Streamlitアプリケーションのヘッダー
st.title("診療報酬点数計算")

# データベースから全薬品名を取得
conn = connect_to_db('product_database.db')
product_names = get_product_names(conn, "")
conn.close()

# ユーザー入力を標準化する関数
def normalize_input(input_str):
    return unicodedata.normalize('NFKC', input_str).lower()

# 7つの薬を選択する領域と、それぞれに対応する1日量の入力フィールドを追加
medications = []
dosages = []

for i in range(7):
    col1, col2 = st.columns(2)
    
    with col1:
        # 薬の名前を入力してもらい、動的に選択肢を更新する
        medication = st.selectbox(f"薬 {i+1} を選択してください:", [""] + product_names, key=f"medication_{i}")
    
    with col2:
        if medication != "":
            dosage = st.text_input(f"薬 {i+1} の1日量を入力してください (整数または少数):", key=f"dosage_{i}")
            if dosage:
                dosage = float(dosage) if '.' in dosage else int(dosage)
        else:
            dosage = None
    
    medications.append(medication)
    dosages.append(dosage)

# 合計の日数を入力するフィールド
total_days = st.number_input("合計の日数を入力してください:", min_value=1, step=1)

# カスタムの丸め処理を実装
def custom_rounding(value):
    if value <= 0.5:
        return 1
    elif value % 1 == 0.5:
        return int(value)  # 切り捨て
    else:
        return round(value)

# 計算ボタン
if st.button("計算"):
    total_points = 0
    all_fields_valid = True

    for medication, dosage in zip(medications, dosages):
        if medication != "":
            if dosage is None or dosage == 0:
                st.error(f"{medication} の1日量を正しく入力してください。")
                all_fields_valid = False
            else:
                conn = connect_to_db('product_database.db')
                price = get_product_price(conn, medication)
                conn.close()

                if price is not None:
                    # 価格を点数に変換
                   calculate_medical_points(price)
                    
                    # 1日量に基づく計算結果を丸める
                    daily_points = custom_rounding(points_per_unit * dosage)
                    
                    # その後で合計日数を掛け合わせる
                    total_medication_points = daily_points * total_days
                    
                    st.success(f"{medication} の総診療報酬点数: {total_medication_points} 点")
                    total_points += total_medication_points
                else:
                    st.error(f"{medication} が見つかりませんでした。")
                    all_fields_valid = False

    if all_fields_valid:
        # 総診療報酬点数を円に換算（10倍）し、消費税10%を追加
        total_yen = total_points * 10
        total_yen_with_tax = total_yen * 1.1
        st.success(f"総金額 (消費税込): {total_yen_with_tax:.0f} 円")
    else:
        st.error("すべての薬と1日量を正しく入力してください。")
