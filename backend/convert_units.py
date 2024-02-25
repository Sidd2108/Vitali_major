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
        
        try:
            return float(entry)  # Try converting to float
        except ValueError:
            return 0  # If the format doesn't match, return the original entry

def convert_string_to_dict(input_string):
    # Remove words within brackets along with brackets
    input_string = re.sub(r'\([^)]*\)', '', input_string).strip()

    # Split everything based on space
    entries = input_string.split()

    # Iterate through entries, join 'Vitamin' with immediate next list item, and remove separate 'Vitamin' and next alphabet entry
    i = 0
    while i < len(entries)-1:
        if entries[i] == "Total":
            entries[i] = f"{entries[i]} {entries[i + 1]}"
            del entries[i+1] 
        if entries[i].startswith('Vitamin') and len(entries[i]) == 7:
            entries[i] = f"{entries[i]} {entries[i + 1]}"
            del entries[i+1]
        if entries[i+1] == 'g' or entries[i+1] == 'mcg' or entries[i+1] == 'IU' or entries[i+1] == 'mg':
            entries[i] = f"{entries[i]} {entries[i+1]}"
            del entries[i+1]
        i += 1

    ingredient_dict = {}

    # Split the lines into names and values
    names = entries[:len(entries)//2]
    values = entries[len(entries)//2:]

    for name, value in zip(names, values):

        # Extract name and value
        name = name.upper()
        value = convert_units(value)

        # Add to the dictionary
        ingredient_dict[name] = value

    return ingredient_dict

# Example usage
# input_string = "Calories Total Carbohydrates Sugars Vitamin C (Ascorbic Acid) Vitamin E (as Alpha Tocopherol Acetate) Niacin Vitamin B6 (as Pyridoxine Hydrochloride) Vitamin B12 (as Methylcobalamin) Calcium (as Silicate, Phosphate and Citrate) Sodium Potassium 10 3g 29 500 mg 200 IU 60 mg 15 mg 90 mcg 152 mg 50 mg 40 mg"
# ingredient_list = convert_string_to_dict(input_string)
# print(ingredient_list)
