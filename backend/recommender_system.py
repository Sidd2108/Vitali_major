import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

import re
def dollars_to_rupees(dollar_price_str):
    # Extract numeric part from the input string using regex
    match = re.search(r'\d+\.\d+', dollar_price_str)
    
    if match:
        # Convert the extracted numeric part to a float
        dollar_price = float(match.group())
        
        rupee_price = dollar_price * 82.93
        
        return f"₹{rupee_price:.2f}"
    else:
        # Handle the case when no numeric part is found in the input string
        return "Invalid input for dollar_price"


def recommend_products(gender,ingredient_list, category, product_df, allowed_values_df) :
    recommended_products = pd.DataFrame()
    recommended_products_subset = pd.DataFrame()

    recommended_items = {}
    updated_ingredient_list = {}
    for nutrient, value in ingredient_list.items():
        # Check if nutrient is present in allowed_values_df for the specified gender
        matching_rows = allowed_values_df[(allowed_values_df["Nutrient"] == nutrient) & (allowed_values_df["Gender"] == gender)]

        if not matching_rows.empty: 
            matching_row = matching_rows.iloc[0]
            allowed_range = matching_row["Allowance (mg)"]
            
            if not (value - 0.1 * value <= allowed_range <= value + 0.1 * value):
                print(f"Updating {nutrient} value to allowed range for {gender}.")
                updated_ingredient_list[nutrient] = allowed_range
            else:
                updated_ingredient_list[nutrient] = value
        else:
            print(f"No information found for {nutrient} for {gender}. Keeping the original value.")
            updated_ingredient_list[nutrient] = value

    # print("Updated Ingredient List:")
    # print(updated_ingredient_list)

    ingredient_columns = product_df.columns[5:]
    product_ingredients = product_df[ingredient_columns]

    updated_ingredient_df = pd.DataFrame([updated_ingredient_list])
    common_ingredients = list(set(updated_ingredient_df.columns).intersection(set(product_ingredients.columns)))

    # Ensure the order of columns matches between updated_ingredient_df and product_ingredients
    updated_ingredient_df = updated_ingredient_df[common_ingredients]
    product_ingredients = product_ingredients[common_ingredients]

    updated_ingredient_df = updated_ingredient_df.dropna(axis=0)
    product_ingredients = product_ingredients.dropna(axis=0)

    def clean_ingredient_values(df):
        cleaned_df = df.copy()
        for col in df.columns:
            cleaned_df[col] = df[col].apply(lambda x: re.sub(r"[^\d\-+\.]", "", str(x)))
        return cleaned_df

    product_ingredients = clean_ingredient_values(product_ingredients)
    # print(updated_ingredient_list)
    # print(product_ingredients)
    if updated_ingredient_df.empty or product_ingredients.empty:
        print("Insufficient data after removing NaN values.")
    else:
        cosine_similarities_ingredient = cosine_similarity(updated_ingredient_df, product_ingredients)
        similarity_threshold_ingredient = 0.87
        similar_product_indices_ingredient = [i for i, sim in enumerate(cosine_similarities_ingredient[0]) if sim > similarity_threshold_ingredient]

        vectorizer = CountVectorizer()
        category_matrix = vectorizer.fit_transform([category] + list(product_df['Category']))

        # Calculate cosine similarity for category
        cosine_similarities_category = cosine_similarity(category_matrix[0], category_matrix[1:])[0]
        similarity_threshold_category = 0.8
        similar_product_indices_category = [i for i, sim in enumerate(cosine_similarities_category) if sim > similarity_threshold_category]

        # Find products that are similar in both ingredients and category
        similar_product_indices = list(set(similar_product_indices_ingredient) & set(similar_product_indices_category))

        if similar_product_indices:
            
            recommended_products = product_df.iloc[similar_product_indices]
            recommended_products_subset = recommended_products[["Brand", "Rating", "Flavor", "Price", "Category"]]

            for _, row in recommended_products_subset.iterrows():
                brand = row['Brand']
                if brand not in recommended_items:
                    recommended_items[brand] = {
                        "Brand": row['Brand'],
                        "Rating": row['Rating'],
                        "Flavor": row['Flavor'],
                        "Price": dollars_to_rupees(row['Price']),
                        "Category": row['Category']
                    }
                filtered_details = {k: v for k, v in recommended_items[brand].items() if pd.notna(v) and str(v) != "{{vm.sku.name}}"}
                if filtered_details :
                    recommended_items[brand] = filtered_details
        else:
            print("No similar products found.")

    return recommended_items
