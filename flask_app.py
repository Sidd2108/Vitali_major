from flask import Flask,request, jsonify
import pandas as pd
from flask_cors import CORS
from backend.recommender_system import recommend_products
from backend.convert_units import convert_string_to_dict

app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "*"}})

product_df = pd.read_csv("backend\converted_products.csv")
allowed_values_df = pd.read_csv("backend\dietary_Allowances.csv")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()

    # Extract input parameters from the request
    gender = data.get('gender')
    ingredient_list = data.get('ingredient_list')
    ingredients = convert_string_to_dict(ingredient_list)
    category = data.get('category')

    # Call the recommendation function
    recommended_products_result = recommend_products(gender, ingredients, category, product_df, allowed_values_df)

    return jsonify(recommended_products_result)

if __name__ == '__main__':
    app.run(debug=True)