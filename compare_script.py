import pandas as pd
from fuzzywuzzy import fuzz
from nltk.tokenize import word_tokenize
import re


def extract_ml_values(description):
    ml_values = re.findall(r'\b\d+.*ml\b', description)
    return ml_values


def extract_digit_values(data):
    digit_values = re.findall(r'\b\d+.*\b', data)
    return digit_values


if __name__ == '__main__':
    flinn_csv = pd.read_csv('Flinn_products.csv')
    frey_csv = pd.read_csv('Frey_products.csv')
    nasco_csv = pd.read_csv('Nasco_products.csv')
    # carolina_csv = pd.read_csv('Carolina_products.csv')
    # vwr_csv = pd.read_csv('VWR_products.csv')
    # fisher_csv = pd.read_csv('Fisher_products.csv')
    frey_matches = []
    nasco_matches = []
    carolina_matches = []
    vwr_matches = []
    fisher_matches = []
    for i, flinn_row in flinn_csv.iterrows():
        flinn_names = flinn_row['Flinn_product_name']
        if pd.notna(flinn_names):
            flinn_desc = flinn_names.lower()
            flinn_digit_values = extract_digit_values(flinn_desc)
            flinn_ml_values = extract_ml_values(flinn_desc)
            '''FREY PRODUCT'''
            for j, frey_row in frey_csv.iterrows():
                frey_names = frey_row.get('Frey_product_name', '')
                frey_desc = frey_names.lower() if pd.notna(frey_names) else ''

                if frey_desc:
                    if re.findall(r'\b\d+.*ml\b', flinn_desc):
                        frey_ml_values = extract_ml_values(frey_desc)
                        if flinn_ml_values and frey_ml_values and set(flinn_ml_values) == set(frey_ml_values):
                            similarity = fuzz.token_set_ratio(flinn_desc, frey_desc)
                            if similarity >= 80:
                                frey_matches.append({**flinn_row.to_dict(), **frey_row.to_dict()})

                    elif re.findall(r'\b\d+.*\b', flinn_desc):
                        frey_digit_values = extract_digit_values(frey_desc)
                        if set(flinn_digit_values) == set(frey_digit_values):
                            similarity = fuzz.token_set_ratio(flinn_desc, frey_desc)
                            if similarity >= 80:
                                frey_matches.append({**flinn_row.to_dict(), **frey_row.to_dict()})

                    else:
                        if set(word_tokenize(flinn_desc)) & set(word_tokenize(frey_desc)):
                            similarity = fuzz.token_set_ratio(flinn_desc, frey_desc)
                            if similarity >= 80:
                                frey_matches.append({**flinn_row.to_dict(), **frey_row.to_dict()})
            '''NASCO PRODUCT'''
            for k, nasco_row in nasco_csv.iterrows():
                nasco_names = nasco_row.get('Nasco_product_name', '')
                nasco_desc = nasco_names.lower() if pd.notna(nasco_names) else ''

                if nasco_desc:
                    if re.findall(r'\b\d+.*ml\b', flinn_desc):
                        nasco_ml_values = extract_ml_values(nasco_desc)
                        if flinn_ml_values and nasco_ml_values and set(flinn_ml_values) == set(nasco_ml_values):
                            similarity = fuzz.token_set_ratio(flinn_desc, nasco_desc)
                            if similarity >= 80:
                                nasco_matches.append({**flinn_row.to_dict(), **nasco_row.to_dict()})
                    elif re.findall(r'\b\d+.*\b', flinn_desc):
                        nasco_digit_values = extract_digit_values(nasco_desc)
                        if set(flinn_digit_values) == set(nasco_digit_values):
                            similarity = fuzz.token_set_ratio(flinn_desc, nasco_desc)
                            if similarity >= 80:
                                nasco_matches.append({**flinn_row.to_dict(), **nasco_row.to_dict()})
                    else:
                        if set(word_tokenize(flinn_desc)) & set(word_tokenize(nasco_desc)):
                            similarity = fuzz.token_set_ratio(flinn_desc, nasco_desc)
                            if similarity >= 80:
                                nasco_matches.append({**flinn_row.to_dict(), **nasco_row.to_dict()})
            # '''CAROLINA PRODUCT'''
            # for l, carolina_row in carolina_csv.iterrows():
            #     carolina_names = carolina_row.get('carolina_product_name', '')
            #     carolina_desc = carolina_names.lower() if pd.notna(carolina_names) else ''
            #
            #     if carolina_desc:
            #         if re.findall(r'\b\d+.*ml\b', flinn_desc):
            #             carolina_ml_values = extract_ml_values(carolina_desc)
            #             if flinn_ml_values and carolina_ml_values and set(flinn_ml_values) == set(carolina_ml_values):
            #                 similarity = fuzz.token_set_ratio(flinn_desc, carolina_desc)
            #                 if similarity >= 80:
            #                     carolina_matches.append({**flinn_row.to_dict(), **carolina_row.to_dict()})
            #         elif re.findall(r'\b\d+.*\b', flinn_desc):
            #             carolina_digit_values = extract_digit_values(carolina_desc)
            #             if set(flinn_digit_values) == set(carolina_digit_values):
            #                 similarity = fuzz.token_set_ratio(flinn_desc, carolina_desc)
            #                 if similarity >= 80:
            #                     carolina_matches.append({**flinn_row.to_dict(), **carolina_row.to_dict()})
            #         else:
            #             if set(word_tokenize(flinn_desc)) & set(word_tokenize(carolina_desc)):
            #                 similarity = fuzz.token_set_ratio(flinn_desc, carolina_desc)
            #                 if similarity >= 80:
            #                     carolina_matches.append({**flinn_row.to_dict(), **carolina_row.to_dict()})
            #     '''VWR PRODUCT'''
            #     for m, vwr_row in vwr_csv.iterrows():
            #         vwr_names = vwr_row.get('VWR_product_name', '')
            #         vwr_desc = vwr_names.lower() if pd.notna(vwr_names) else ''
            #
            #         if vwr_desc:
            #             if re.findall(r'\b\d+.*ml\b', flinn_desc):
            #                 vwr_ml_values = extract_ml_values(vwr_desc)
            #                 if flinn_ml_values and vwr_ml_values and set(flinn_ml_values) == set(
            #                         vwr_ml_values):
            #                     similarity = fuzz.token_set_ratio(flinn_desc, vwr_desc)
            #                     if similarity >= 80:
            #                         vwr_matches.append({**flinn_row.to_dict(), **vwr_row.to_dict()})
            #             elif re.findall(r'\b\d+.*\b', flinn_desc):
            #                 vwr_digit_values = extract_digit_values(vwr_desc)
            #                 if set(flinn_digit_values) == set(vwr_digit_values):
            #                     similarity = fuzz.token_set_ratio(flinn_desc, vwr_desc)
            #                     if similarity >= 80:
            #                         vwr_matches.append({**flinn_row.to_dict(), **vwr_row.to_dict()})
            #             else:
            #                 if set(word_tokenize(flinn_desc)) & set(word_tokenize(vwr_desc)):
            #                     similarity = fuzz.token_set_ratio(flinn_desc, vwr_desc)
            #                     if similarity >= 80:
            #                         vwr_matches.append({**flinn_row.to_dict(), **vwr_row.to_dict()})
            #         '''FISHER PRODUCTS'''
            #         for n, fisher_row in fisher_csv.iterrows():
            #             fisher_names = fisher_row.get('Fisher_product_name', '')
            #             fisher_desc = fisher_names.lower() if pd.notna(fisher_names) else ''
            #
            #             if fisher_desc:
            #                 if re.findall(r'\b\d+.*ml\b', flinn_desc):
            #                     fisher_ml_values = extract_ml_values(fisher_desc)
            #                     if flinn_ml_values and fisher_ml_values and set(flinn_ml_values) == set(
            #                             fisher_ml_values):
            #                         similarity = fuzz.token_set_ratio(flinn_desc, fisher_desc)
            #                         if similarity >= 80:
            #                             fisher_matches.append({**flinn_row.to_dict(), **fisher_row.to_dict()})
            #                 elif re.findall(r'\b\d+.*\b', flinn_desc):
            #                     fisher_digit_values = extract_digit_values(fisher_desc)
            #                     if set(flinn_digit_values) == set(fisher_digit_values):
            #                         similarity = fuzz.token_set_ratio(flinn_desc, fisher_desc)
            #                         if similarity >= 80:
            #                             fisher_matches.append({**flinn_row.to_dict(), **fisher_row.to_dict()})
            #                 else:
            #                     if set(word_tokenize(flinn_desc)) & set(word_tokenize(fisher_desc)):
            #                         similarity = fuzz.token_set_ratio(flinn_desc, fisher_desc)
            #                         if similarity >= 80:
            #                             fisher_matches.append({**flinn_row.to_dict(), **fisher_row.to_dict()})

    frey_df = pd.DataFrame(frey_matches)
    nasco_df = pd.DataFrame(nasco_matches)
    # carolina_df = pd.DataFrame(carolina_matches)
    # vwr_df = pd.DataFrame(vwr_matches)
    # fisher_df = pd.DataFrame(fisher_matches)
    merged_df = pd.concat([frey_df, nasco_df], axis=1)
    # merged_df = pd.concat([frey_df, nasco_df, carolina_df, vwr_df, fisher_df], axis=1)
    merged_df = merged_df.loc[:,~merged_df.columns.duplicated()]

    merged_df.to_csv('master_file.csv', index=False)

