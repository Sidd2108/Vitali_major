from flask import Flask,request, jsonify
import pandas as pd
from flask_cors import CORS
from backend.recommender_system import recommend_products
from backend.convert_units import convert_string_to_dict
from backend.scripts.amzn_scrape import scrape_amzn_products
from backend.scripts.flpkrt_scrape import scrape_flpkrt_products

app = Flask(__name__)
CORS(app, resources={r"/recommend": {"origins": "*"}}, allow_headers=["Content-Type", "Authorization"])
product_df = pd.read_csv("backend\converted_products.csv")
allowed_values_df = pd.read_csv("backend\dietary_Allowances.csv")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/recommend', methods = ['GET'])
def printmsg():
    return "Works, now try hitting POST request for same url with parameters"

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    # print(data)

    # Extract input parameters from the request
    gender = data.get('gender')
    ingredient_list = data.get('ingredient_list')
    ingredients = convert_string_to_dict(ingredient_list)
    category = data.get('category')
    # print(gender, category, ingredients)
    recommended_products_amzn = scrape_amzn_products(category=category)
    recommended_products_flpkrt = scrape_flpkrt_products(category=category)
    # merging two results
    recommended_products_result = {}
    all_keys = set(recommended_products_amzn.keys()) | set(recommended_products_flpkrt.keys())
    for key in all_keys:
        if key in recommended_products_amzn and key in recommended_products_flpkrt:
            recommended_products_result[key] = [recommended_products_amzn[key], recommended_products_flpkrt[key]]
        elif key in recommended_products_amzn:
            recommended_products_result[key] = [recommended_products_amzn[key]]
        elif key in recommended_products_flpkrt:
            recommended_products_result[key] = [recommended_products_flpkrt[key]]
    
    return recommended_products_result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)