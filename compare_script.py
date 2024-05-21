import pandas as pd
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
import re


def extract_ml_values(description):
    return re.findall(r'\b\d+.*ml\b', description)


def extract_digit_values(data):
    return re.findall(r'\b\d+.*\b', data)


'''WRITE THE CONDITION FOR MATCHING'''


def find_best_match(flinn_desc, flinn_ml_values, flinn_digit_values, dataset, product_name_col):
    highest_similarity = 0
    best_match = None
    for _, row in dataset.iterrows():
        product_name = row.get(product_name_col, '')
        product_desc = product_name.lower() if pd.notna(product_name) else ''
        similarity = fuzz.token_set_ratio(flinn_desc, product_desc)
        if re.findall(r'\b\d+.*ml\b', flinn_desc):
            product_ml_values = extract_ml_values(product_desc)
            if set(flinn_ml_values) == set(product_ml_values):
                content_set = set(word_tokenize(flinn_desc.replace(',', '').replace('.', ''))) & set(
                    word_tokenize(product_desc.replace(',', '').replace('.', '')))
                if len(content_set) >= 3:
                    if similarity == 100:
                        return similarity, row.to_dict()
                    elif similarity > highest_similarity:
                        highest_similarity = similarity
                        best_match = row.to_dict()
        elif re.findall('\d+', str(flinn_desc)):
            product_digit_values = extract_digit_values(product_desc)
            if set(flinn_digit_values) and set(product_digit_values):
                content_set = set(word_tokenize(flinn_desc.replace(',', '').replace('.', ''))) & set(
                    word_tokenize(product_desc.replace(',', '').replace('.', '')))
                if len(content_set) >= 3:
                    if similarity == 100:
                        return similarity, row.to_dict()
                    elif similarity > highest_similarity:
                        highest_similarity = similarity
                        best_match = row.to_dict()
        else:
            content_set = set(word_tokenize(flinn_desc.replace(',', '').replace('.', ''))) & set(
                word_tokenize(product_desc.replace(',', '').replace('.', '')))
            if len(content_set) >= 3:
                if similarity == 100:
                    return similarity, row.to_dict()
                elif similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match = row.to_dict()
            elif len(content_set) == 2:
                if similarity == 100:
                    return similarity, row.to_dict()
                elif similarity > highest_similarity:
                    highest_similarity = similarity
                    best_match = row.to_dict()
    return highest_similarity, best_match


'''SOTRING THE DATA'''


def process_datasets(flinn_csv, frey_csv, nasco_csv, carolina_csv, vwr_csv, fisher_csv):
    combined_matches = []

    for _, flinn_row in flinn_csv.iterrows():
        flinn_names = flinn_row['Flinn_product_names']
        if pd.notna(flinn_names):
            flinn_desc = flinn_names.lower()
            print(flinn_desc)
            flinn_ml_values = extract_ml_values(flinn_desc)
            flinn_digit_values = extract_digit_values(flinn_desc)
            best_match_frey = find_best_match(flinn_desc, flinn_ml_values, flinn_digit_values, frey_csv, 'Frey_product_name')[1]
            best_match_nasco = find_best_match(flinn_desc, flinn_ml_values, flinn_digit_values, nasco_csv, 'Nasco_product_name')[1]
            best_match_carolina = find_best_match(flinn_desc, flinn_ml_values, flinn_digit_values, carolina_csv, 'Carolina_product_name')[1]
            best_match_vwr = find_best_match(flinn_desc, flinn_ml_values, flinn_digit_values, vwr_csv, 'VWR_product_name')[1]
            best_match_fisher = find_best_match(flinn_desc, flinn_ml_values, flinn_digit_values, fisher_csv, 'Fisher_product_name')[1]

            best_match = {
                **flinn_row.to_dict(),
                **(best_match_frey or {col: '' for col in frey_csv.columns}),
                **(best_match_nasco or {col: '' for col in nasco_csv.columns}),
                **(best_match_carolina or {col: '' for col in carolina_csv.columns}),
                **(best_match_vwr or {col: '' for col in vwr_csv.columns}),
                **(best_match_fisher or {col: '' for col in fisher_csv.columns})
            }

            combined_matches.append(best_match)

        combined_df = pd.DataFrame(combined_matches)
        combined_df.to_csv('master_file.csv', index=False)


if __name__ == '__main__':
    flinn_csv = pd.read_csv('Flinn_Products.csv')
    frey_csv = pd.read_csv('Frey_products.csv')
    nasco_csv = pd.read_csv('Nasco_products.csv')
    carolina_csv = pd.read_csv('Carolina_Products.csv')
    vwr_csv = pd.read_csv('VWR_WARDS_Products.csv')
    fisher_csv = pd.read_csv('Fisher_Products.csv')

    process_datasets(flinn_csv, frey_csv, nasco_csv, carolina_csv, vwr_csv, fisher_csv)
