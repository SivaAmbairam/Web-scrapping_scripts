import re
from module_package import *
import math


def write_visited_log(url):
    with open(f'Visited_VWR_urls.txt', 'a', encoding='utf-8') as file:
        file.write(f'{url}\n')


def read_log_file():
    if os.path.exists(f'Visited_VWR_urls.txt'):
        with open(f'Visited_VWR_urls.txt', 'r', encoding='utf-8') as read_file:
            return read_file.read().split('\n')
    return []


if __name__ == '__main__':
    timestamp = datetime.now().date().strftime('%Y%m%d')
    file_name = 'VWR_WARDS_Products'
    url = 'https://us.vwr.com/store/catalog/vwr_products.jsp'
    base_url = 'https://us.vwr.com'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }
    soup = get_soup(url, headers)
    content = soup.find_all('ul', class_='a-z_categorylist')
    for single_content in content:
        inner_content = single_content.find_all('a')
        for single_url in inner_content:
            product_category = single_url.text.strip()
            main_url = f'{base_url}{single_url["href"]}'
            print(f'main_url---------------->{main_url}')
            if main_url in read_log_file():
                continue
            inner_request = get_soup(main_url, headers)
            if inner_request is None:
                continue
            if inner_request.find('div', class_='col-xs-12 col-sm-3 pagination-label'):
                '''GET PAGINATION'''
                page_tag = strip_it(inner_request.find('div', class_='col-xs-12 col-sm-3 pagination-label').text.replace(',', ''))
                page_split = page_tag.split('of', 1)
                count = page_split[-1].strip()
                page_count = page_split[0].split('-', 1)[-1].strip()
                total_pages = math.ceil(int(count) / int(page_count))
                for i in range(1, int(total_pages) + 1):
                    page_link = f'{main_url}?pageNo={i}'
                    page_req = requests.get(page_link, headers=headers)
                    # if page_req.status_code == 403:
                    #     if page_link in read_log_file():
                    #         continue
                    #     print(f'page_link---------->{page_link}')
                    #     response = get_zenrowa(page_link, params = {'js_render': 'true', "premium_proxy": "true", "proxy_country": "us"})
                    #     page_soup = BeautifulSoup(response.text, 'html.parser')
                    #     '''PRODUCT URL'''
                    #     url_href = page_soup.find_all('h2', class_='search-item__title h4')
                    #     for single_href in url_href:
                    #         main_name = single_href.a.text.strip()
                    #         product_url = f'{base_url}{single_href.a["href"]}'
                    #         split_href = str(product_url).rsplit('/', 1)[0].split('product/')[-1].strip()
                    #         request_url = f'https://us.vwr.com/store/services/catalog/json/stiboOrderTableRender.jsp?productId={split_href}&catalogNumber=&discontinuedflag=&hasItemPages=false&specialCertRender=false&staticPage='
                    #         print(product_url)
                    #         if product_url in read_log_file():
                    #             continue
                    #         product_request = get_soup(request_url, headers)
                    #         if product_request is None:
                    #             continue
                    #         product_content = product_request.find_all('table', class_='table-stack table table-responsive table-product mb-2')
                    #         for single_product_content in product_content:
                    #             inner_data = single_product_content.find_all('tr', class_='product-row-main')
                    #             for single_data in inner_data:
                    #                 if single_data.find('td', attrs={'data-title': 'VWR Catalog Number'}):
                    #                     '''PRODUCT NAME'''
                    #                     product_item = single_data.find('td', attrs={'data-title': 'VWR Catalog Number'}).extract()
                    #                     try:
                    #                         extract_tag = single_data.find('td', attrs={'data-title': 'Unit'}).extract()
                    #                         inner_extract = single_data.find('td', attrs={'data-title': 'Supplier No.'}).extract()
                    #                     except:
                    #                         extract_tag = ''
                    #                         inner_extract = ''
                    #                     try:
                    #                         other_extract = single_data.find('td', attrs={'data-title': 'Quantity'}).extract()
                    #                     except:
                    #                         other_extract = ''
                    #                     try:
                    #                         price_extract = single_data.find('td', attrs={'data-title': 'Price'}).extract()
                    #                     except:
                    #                         price_extract = ''
                    #                     '''PRODUCT NAME'''
                    #                     try:
                    #                         data_tag = single_data.find_all('td')
                    #                         name_list = []
                    #                         for single_title in data_tag:
                    #                             content_text = single_title.text.strip()
                    #                             name_list.append(content_text)
                    #                         product_names = ' '.join(name_list)
                    #                         if main_name in product_names:
                    #                             product_name = product_names
                    #                         else:
                    #                             product_name = f'{main_name} {product_names}'
                    #                     except:
                    #                         product_name = main_name
                    #                     '''PRODUCT QUANTITY'''
                    #                     product_quantity = '1'
                    #                     '''PRODUCT ID'''
                    #                     product_id = strip_it(product_item.text)
                    #                     id_tag = product_item.find('span')['id'].replace("['", '').replace("']", '').split('_', 1)[-1].split('_', 1)[0].strip()
                    #                     product_req_url = f'https://us.vwr.com/store/services/pricing/json/skuPricing.jsp?skuIds={id_tag}&salesOrg=8000&salesOffice=0000&profileLocale=en_US&promoCatalogNumber=&promoCatalogNumberForSkuId=&forcePromo=false'
                    #                     price_request = get_json_response(product_req_url, headers)
                    #                     for single_price in price_request:
                    #                         product_price = single_price['salePrice']
                    #                         print('current datetime------>', datetime.now())
                    #                         dictionary = {
                    #                             'VWR_product_category': product_category,
                    #                             'VWR_product_sub_category': 'NA',
                    #                             'VWR_product_id': product_id,
                    #                             'VWR_product_name': product_name,
                    #                             'VWR_product_quantity': product_quantity,
                    #                             'VWR_product_price': product_price,
                    #                             'VWR_product_url': product_url
                    #                         }
                    #                         articles_df = pd.DataFrame([dictionary])
                    #                         articles_df.drop_duplicates(subset=['VWR_product_id', 'VWR_product_name'], keep='first',
                    #                                                     inplace=True)
                    #                         if os.path.isfile(f'{file_name}.csv'):
                    #                             articles_df.to_csv(f'{file_name}.csv', index=False, header=False, mode='a')
                    #                         else:
                    #                             articles_df.to_csv(f'{file_name}.csv', index=False)
                    #                         write_visited_log(product_url)
                    #     write_visited_log(page_link)
                    if page_req.status_code == 200:
                        page_soup = get_soup(page_link, headers)
                        '''PRODUCT URL'''
                        url_href = page_soup.find_all('h2', class_='search-item__title h4')
                        for single_href in url_href:
                            main_name = single_href.a.text.strip()
                            product_url = f'https://us.vwr.com{single_href.a["href"]}'
                            print(product_url)
                            split_href = str(product_url).rsplit('/', 1)[0].split('product/')[-1].strip()
                            request_url = f'https://us.vwr.com/store/services/catalog/json/stiboOrderTableRender.jsp?productId={split_href}&catalogNumber=&discontinuedflag=&hasItemPages=false&specialCertRender=false&staticPage='
                            product_request = get_soup(request_url, headers)
                            if product_request is None:
                                continue
                            product_content = product_request.find_all('tr', class_='product-row-main')
                            for single_data in product_content:
                                if single_data.find('td', attrs={'data-title': 'VWR Catalog Number'}):
                                    '''PRODUCT ID'''
                                    product_item = single_data.find('td', attrs={'data-title': 'VWR Catalog Number'}).extract()
                                    try:
                                        extract_tag = single_data.find('td', attrs={'data-title':'Unit'}).extract()
                                        inner_extract = single_data.find('td', attrs={'data-title':'Supplier No.'}).extract()
                                    except:
                                        extract_tag = ''
                                        inner_extract = ''
                                    try:
                                        other_extract = single_data.find('td', attrs={'data-title':'Quantity'}).extract()
                                    except:
                                        other_extract = ''
                                    try:
                                        price_extract = single_data.find('td', attrs={'data-title': 'Price'}).extract()
                                    except:
                                        price_extract = ''
                                    '''PRODUCT NAME'''
                                    try:
                                        data_tag = single_data.find_all('td')
                                        name_list = []
                                        for single_title in data_tag:
                                            content_text = single_title.text.strip()
                                            name_list.append(content_text)
                                        product_names = ' '.join(name_list)
                                        if main_name in product_names:
                                            product_name = product_names
                                        else:
                                            product_name = f'{main_name} {product_names}'
                                    except:
                                        product_name = main_name
                                    '''PRODUCT QUANTITY'''
                                    product_quantity = '1'
                                    product_id = strip_it(product_item.text)
                                    if product_id in read_log_file():
                                        continue
                                    id_tag = product_item.find('span')['id'].replace("['", '').replace("']", '').split('_', 1)[-1].split('_', 1)[0].strip()
                                    product_req_url = f'https://us.vwr.com/store/services/pricing/json/skuPricing.jsp?skuIds={id_tag}&salesOrg=8000&salesOffice=0000&profileLocale=en_US&promoCatalogNumber=&promoCatalogNumberForSkuId=&forcePromo=false'
                                    price_request = get_json_response(product_req_url, headers)
                                    for single_price in price_request:
                                        product_price = single_price['salePrice']
                                        print('current datetime------>', datetime.now())
                                        dictionary = {
                                            'VWR_product_category': product_category,
                                            'VWR_product_sub_category': 'NA',
                                            'VWR_product_id': product_id,
                                            'VWR_product_name': product_name,
                                            'VWR_product_quantity': product_quantity,
                                            'VWR_product_price': product_price,
                                            'VWR_product_url': product_url
                                        }
                                        articles_df = pd.DataFrame([dictionary])
                                        articles_df.drop_duplicates(subset=['VWR_product_id', 'VWR_product_name'], keep='first',
                                                                    inplace=True)
                                        if os.path.isfile(f'{file_name}.csv'):
                                            articles_df.to_csv(f'{file_name}.csv', index=False, header=False, mode='a')
                                        else:
                                            articles_df.to_csv(f'{file_name}.csv', index=False)
                                        write_visited_log(product_id)
            write_visited_log(main_url)
