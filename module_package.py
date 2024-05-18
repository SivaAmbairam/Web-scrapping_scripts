from bs4 import BeautifulSoup
import pandas as pd
import requests
import json
import re
import os
import time
from datetime import datetime
from zenrows import ZenRowsClient

def clean_header(head):
    header_dict = {}
    split_new_line = head.split('\n')
    for x in split_new_line:
        if x != '':
            x = x.lstrip(':').split(': ')
            header_dict[x[0]] = x[1]
    for n in header_dict.items():
        output = f"'{n[0]}': '{n[-1]}',"
        print(output)


def status_log(r):
    """Pass response as a parameter to this function"""
    url_log_file = 'url_log.txt'
    if not os.path.exists(os.getcwd() + '\\' + url_log_file):
        with open(url_log_file, 'w') as f:
            f.write('url, status_code\n')
    with open(url_log_file, 'a') as file:
        file.write(f'{r.url}, {r.status_code}\n')


def retry(func, retries=3):
    """Decorator function"""
    retry.count = 0

    def retry_wrapper(*args, **kwargs):
        attempt = 0
        while attempt < retries:
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ConnectionError as e:
                attempt += 1
                total_time = attempt * 10
                print(f'Retrying {attempt}: Sleeping for {total_time} seconds, error: ', e)
                time.sleep(total_time)
            if attempt == retries:
                retry.count += 1
                url_log_file = 'url_log.txt'
                if not os.path.exists(os.getcwd() + '\\' + url_log_file):
                    with open(url_log_file, 'w') as f:
                        f.write('url, status_code\n')
                with open(url_log_file, 'a') as file:
                    file.write(f'{args[0]}, requests.exceptions.ConnectionError\n')
            if retry.count == 3:
                print("Stopped after retries, check network connection")
                raise SystemExit

    return retry_wrapper


@retry
def get_soup_verify(url, headers=None):
    r = requests.Session().get(url, headers=headers, timeout=120, verify=False)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    elif 499 >= r.status_code >= 400:
        print(f'client error response, status code {r.status_code} \nrefer: {r.url}')
        status_log(r)
    elif 599 >= r.status_code >= 500:
        print(f'server error response, status code {r.status_code} \nrefer: {r.url}')
        count = 1
        while count != 10:
            print('while', count)
            r = requests.Session().get(url, headers=headers, timeout=120, verify=False)
            print('status_code: ', r.status_code)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                return soup
            else:
                print('retry ', count)
                count += 1
                time.sleep(count * 2)
    else:
        status_log(r)
        return None

@retry
def get_zenrowa(url, params=None):
    api_list = ['1e8cb006ec4177a86afaa3567dbfdb3d2e870c5b', 'f8d6d1f2fea9a90579597c47d7b81ff0ea990d11']
    for single_api in api_list:
        client = ZenRowsClient(single_api)
        r = client.get(url, params = params)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            return soup
        elif 499 >= r.status_code >= 400:
            print(f'client error response, status code {r.status_code} \nrefer: {r.url}')
            status_log(r)
        elif 599 >= r.status_code >= 500:
            print(f'server error response, status code {r.status_code} \nrefer: {r.url}')
            count = 1
            while count != 10:
                print('while', count)
                client = ZenRowsClient(api_list)
                r = client.get(url, params=params)
                print('status_code: ', r.status_code)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    return soup
                else:
                    print('retry ', count)
                    count += 1
                    time.sleep(count * 2)
            else:
                status_log(r)
                return None


@retry
def get_soup(url, headers=None):
    r = requests.Session().get(url, headers=headers, timeout=300)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'html.parser')
        return soup
    elif 499 >= r.status_code >= 400:
        print(f'client error response, status code {r.status_code} \nrefer: {r.url}')
        status_log(r)
    elif 599 >= r.status_code >= 500:
        print(f'server error response, status code {r.status_code} \nrefer: {r.url}')
        count = 1
        while count != 10:
            print('while', count)
            r = requests.Session().get(url, headers=headers, timeout=300)
            print('status_code: ', r.status_code)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                return soup
            else:
                print('retry ', count)
                count += 1
                time.sleep(count * 2)
    else:
        status_log(r)
        return None


@retry
def post_soup(url, headers=None, payload=None):
    r = requests.Session().post(url, headers=headers, json=payload, timeout=30, verify=False)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, features="html.parser")
        return soup
    elif 499 >= r.status_code >= 400:
        print(f'client error response, status code {r.status_code} \nrefer: {r.url}')
        status_log(r)
    elif 599 >= r.status_code >= 500:
        print(f'server error response, status code {r.status_code} \nrefer: {r.url}')
        count = 1
        while count != 10:
            print('while', count)
            r = requests.Session().post(url, headers=headers, json=payload, verify=False)
            print('status_code: ', r.status_code)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                return soup
            else:
                print('retry ', count)
                count += 1
                time.sleep(count * 2)
    else:
        status_log(r)
        return None


@retry
def get_json_response(url, headers=None):
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        data_ = r.json()
        return data_
    elif 499 >= r.status_code >= 400:
        print(f'client error response, status code {r.status_code} \nrefer: {r.url}')
        status_log(r)
    elif 599 >= r.status_code >= 500:
        print(f'server error response, status code {r.status_code} \nrefer: {r.url}')
        count = 1
        while count != 10:
            print('while', count)
            r = requests.get(url, headers=headers)
            print('status_code: ', r.status_code)
            if r.status_code == 200:
                data_ = r.json()
                return data_
            else:
                print('retry ', count)
                count += 1
                time.sleep(count * 2)
    else:
        status_log(r)
        return None


@retry
def post_json_response(url, headers=None, payload=None):
    ses = requests.session()
    r = ses.post(url, headers=headers, json=payload)
    if r.status_code == 200:
        return r.json()
    elif 499 >= r.status_code >= 400:
        print(f'client error response, status code {r.status_code} \nrefer: {r.url}')
        status_log(r)
    elif 599 >= r.status_code >= 500:
        print(f'server error response, status code {r.status_code} \nrefer: {r.url}')
        count = 1
        while count != 10:
            print('while', count)
            r = ses.post(url, headers=headers, json=payload)
            print('status_code: ', r.status_code)
            if r.status_code == 200:
                return r.json()
            else:
                print('retry ', count)
                count += 1
                time.sleep(count * 2)
    else:
        status_log(r)
        return None


def write_visited_log(url):
    with open(f'Visited_urls.txt', 'a', encoding='utf-8') as file:
        file.write(f'{url}\n')


def read_log_file():
    if os.path.exists(f'Visited_urls.txt'):
        with open(f'Visited_urls.txt', 'r', encoding='utf-8') as read_file:
            return read_file.read().split('\n')
    return []


def get_dictionary(product_ids=None, product_names=None, product_quantities=None, product_prices=None,
                   product_urls=None):
    dictionary_1 = {
        'product_id': product_ids,
        'product_name': product_names,
        'product_quantity': product_quantities,
        'product_price': product_prices,
        'product_url': product_urls
    }
    return dictionary_1


def strip_it(text):
    return re.sub(r"\s+", ' ', text).strip()


def get_main_urls(soup):
    """Extract main URLs from the homepage soup object"""
    main_urls = []
    for link in soup.find_all('a', href=True):
        url = link['href']
        if "category" in url:  # Adjust this condition based on the actual structure
            main_urls.append(url)
    return main_urls


def get_category_urls(soup):
    """Extract category URLs from the category page soup object"""
    category_urls = []
    for link in soup.find_all('a', href=True):
        url = link['href']
        if "subcategory" in url:  # Adjust this condition based on the actual structure
            category_urls.append(url)
    return category_urls


def get_product_urls(soup):
    """Extract product URLs from the product list page soup object"""
    product_urls = []
    for link in soup.find_all('a', href=True):
        url = link['href']
        if "product" in url:  # Adjust this condition based on the actual structure
            product_urls.append(url)
    return product_urls


def extract_product_data(soup):
    """Extract product data from the product page soup object"""
    product_id = soup.find('span', {'class': 'product-id'}).text.strip()
    product_name = soup.find('h1', {'class': 'product-title'}).text.strip()
    product_quantity = soup.find('span', {'class': 'product-quantity'}).text.strip()
    product_price = soup.find('span', {'class': 'product-price'}).text.strip()
    product_url = soup.find('link', {'rel': 'canonical'})['href']

    product_data = get_dictionary(
        product_ids=product_id,
        product_names=product_name,
        product_quantities=product_quantity,
        product_prices=product_price,
        product_urls=product_url
    )
    return product_data


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # Main URL to start scraping
    main_url = 'https://example.com'  # Replace with the actual main URL

    visited_urls = read_log_file()

    if main_url not in visited_urls:
        main_soup = get_soup_verify(main_url, headers=headers)
        main_urls = get_main_urls(main_soup)
        write_visited_log(main_url)

        for category_url in main_urls:
            if category_url not in visited_urls:
                category_soup = get_soup_verify(category_url, headers=headers)
                category_urls = get_category_urls(category_soup)
                write_visited_log(category_url)

                for product_url in category_urls:
                    if product_url not in visited_urls:
                        product_soup = get_soup_verify(product_url, headers=headers)
                        product_urls = get_product_urls(product_soup)
                        write_visited_log(product_url)

                        for final_product_url in product_urls:
                            if final_product_url not in visited_urls:
                                final_product_soup = get_soup_verify(final_product_url, headers=headers)
                                product_data = extract_product_data(final_product_soup)
                                print(product_data)  # Process the extracted data as needed
                                write_visited_log(final_product_url)


if __name__ == "__main__":
    main()
