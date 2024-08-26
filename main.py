from flask import Flask, render_template, request, jsonify
from src.db_connection import connect_to_db
from src.product_operations import get_product_price, get_product_names
from src.calculation import calculate_medical_points

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    points = None
    if request.method == 'POST':
        product_name = request.form['product_name']
        conn = connect_to_db('product_database.db')
        price = get_product_price(conn, product_name)
        conn.close()

        if price is not None:
            points = calculate_medical_points(price)

    return render_template('index.html', points=points)

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    conn = connect_to_db('product_database.db')
    product_names = get_product_names(conn, search)
    conn.close()
    return jsonify(matching_results=product_names)

if __name__ == '__main__':
    app.run(debug=True)
