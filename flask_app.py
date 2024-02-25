from flask import Flask,request, jsonify
import pandas as pd
from backend.recommender_system import recommend_products
# import pandas as pd

app = Flask(__name__)

product_df = pd.read_csv("backend\converted_products.csv")
allowed_values_df = pd.read_csv("backend\dietary_Allowances.csv")


@app.route('/recommend', methods=['POST'])
def get_recommendations():
    data = request.get_json()

    # Extract input parameters from the request
    gender = data.get('gender')
    ingredient_list = data.get('ingredient_list')
    category = data.get('category')

    # Call the recommendation function
    recommended_products_result = recommend_products(gender, ingredient_list, category, product_df, allowed_values_df)

    return jsonify(recommended_products_result)

if __name__ == '__main__':
    app.run(debug=True)