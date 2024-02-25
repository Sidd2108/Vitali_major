import re

def convert_units(entry):
    if isinstance(entry, (int, float)):
        return entry
    entry = re.sub(r'^\.(\d+)', r'0.\1', str(entry))
    entry = re.sub(r'(\d+)\s*IU$', lambda match: str(0.025 * float(match.group(1))), entry)
    match = re.match(r'(\d+(\.\d+)?)\s*(mg|g|mcg)', entry)
    if match:
        number, _, unit = match.groups()
        number = float(number)
        if unit == 'mg':
            return number
        elif unit == 'g':
            return number * 1000
        elif unit == 'mcg':
            return number / 1000
    elif 'g' in entry:
        return 0
    else:
        return entry  # If the format doesn't match, return the original entry

def convert_string_to_dict(input_string):
    lines = input_string.strip().split('\n')
    ingredient_dict = {}

    # Split the lines into names and values
    names = lines[:len(lines)//2]
    values = lines[len(lines)//2:]

    for name, value in zip(names, values):
        # Remove words within brackets along with brackets
        name = re.sub(r'\([^)]*\)', '', name).strip()

        # Extract name and value
        name = name.upper()
        value = convert_units(value)

        # Add to the dictionary
        ingredient_dict[name] = value

    return ingredient_dict

# # Example usage
# input_string = """
# Calories
# Total Carbohydrates
# Sugars
# Vitamin C (Ascorbic Acid)
# Vitamin E (as Alpha Tocopherol Acetate)
# Niacin
# Vitamin B6 (as Pyridoxine Hydrochloride)
# Vitamin B12 (as Methylcobalamin)
# Calcium (as Silicate, Phosphate and Citrate)
# Sodium
# Potassium
# 10
# 3g
# 29
# 500 mg
# 200 IU
# 60 mg
# 15 mg
# 90 mcg
# 152 mg
# 50 mg
# 40 mg
# """

# ingredient_list = convert_string_to_dict(input_string)
# print(ingredient_list)
