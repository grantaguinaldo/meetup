# Obtain interpretations.
from bs4 import BeautifulSoup as soup
import requests as r
import json
import re
import time
import datetime as dt
import random
import uuid

def get_panel_url(url):
    '''
    Takes a url and gets all of the urls from the sections in the left side bar.
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = r.get(url, headers=headers)
    page_data = soup(data.text, 'html.parser')
    panel_listing = page_data.find_all('div', class_='dot-regulations-sidebar-panel-listing')[0]
    url_list = [each.get('onclick') for each in panel_listing.find_all('li')]
    url_list_edit = []
    for i in url_list:
        start = i.find('/')
        end = i.find(';')
        url_string = 'https://www.phmsa.dot.gov' + i[start:end-1]
        url_list_edit.append(url_string)
    return url_list_edit

def get_page_urls(url):
    '''
    Takes a url, and get's all of the urls needed to paginate through the give section.
    '''
    results = []
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = soup(r.get(url, headers=headers).text, 'html.parser')
    try:
        last_page = int(data.find_all('ul', class_='pager')[0].find_all('a')[-1].get('href').split('=')[-1])
        results = [url + '?page=' + str(each) for each in range(last_page + 1)]
    except:
        results.append(url)
    return results

def parse_single_page(url):
    '''
    Obtains data from each page and stores in a list of dictionaries.
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = r.get(url, headers=headers)
    page_data = soup(data.text, 'html.parser')
    page_datatable_data = page_data.find_all('table', class_="dot-table dot-regulations-table tablesaw tablesaw-stack")[0]
    table_body_data = page_datatable_data.find_all('tr')
    base = 'https://www.phmsa.dot.gov' 
    results = []
    for each in table_body_data[1:]:
        current_ts = dt.datetime.now()
        results_dict = dict()
        results_dict['source_url'] = url
        results_dict['section'] = url[url.find('n/')+2:url.find('?')]
        results_dict['url'] = base + each.find_all('td')[0].find_all('a')[0].get('href')
        results_dict['response_url']  = base + each.find_all('a')[0].get('href')
        results_dict['date'] = each.find_all('td')[1].text.strip()
        results_dict['company'] = each.find_all('td')[2].text.strip()
        results_dict['company_contact'] = each.find_all('td')[3].text.strip()
        results_dict['date_scraped'] = str(current_ts.strftime("%Y-%m-%d %H:%M:%S"))
        results_dict['section'] = str(results_dict['source_url']).split('/')[-1].split('?')[0]
        results.append(results_dict)
    return results

def get_num_entires_on_single_page(url):
    '''
    Obtains the total number of entires on a single page as an int.
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = r.get(url, headers=headers)
    page_data = soup(data.text, 'html.parser')
    page_datatable_data = page_data.find_all('table', class_="dot-table dot-regulations-table tablesaw tablesaw-stack")[0]
    table_body_data = page_datatable_data.find_all('tr')
    table_len = len(table_body_data[1:])
    return table_len

def getUrl(url):
    '''
    Parses each `response_url` and gets the url of of the .pdf file. Structure 1.
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = r.get(url, headers=headers)
    page_data = soup(data.text, 'html.parser')
    class1 = 'dot-regulations-content-inner-wrapper'
    class2 = 'document--set file--attachment field field--name-field-document field--type-file field--label-hidden clearfix field__item'

    pdf_url1 = page_data.find_all('div', class_=class1)[0].find_all('a')[0].get('href').strip()
    if str(pdf_url1).split('.')[-1] == 'pdf':
        pdf_url = 'https://www.phmsa.dot.gov' + pdf_url1
    else:
        data = r.get('https://www.phmsa.dot.gov' + pdf_url1, headers=headers)
        page_data = soup(data.text, 'html.parser')
        pdf_url = page_data.find_all('div', class_=class2)[0].find('a').get('href')
    return pdf_url

def getUrl2(url):
    '''
    Parses each `response_url` and gets the url of of the .pdf file. Structure 1.
    '''
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    data = r.get(url, headers=headers)
    page_data = soup(data.text, 'html.parser')
    class1 = 'dot-regulations-content-inner-wrapper'
    class2 = 'field-item even'
    iurl = page_data.find_all('div', class_=class1)[0].find('a').get('href')
    full_url = 'https://www.phmsa.dot.gov' + iurl
    page_data2 = soup(r.get(full_url, headers=headers).text, 'html.parser')
    pdf_url =  page_data2.find_all('div', class_=class2)[0].find('a').get('href')
    return pdf_url

def main(data):
    '''
    Takes list of dictionaries and obtains url to each .pdf file.
    Returns a list of two elements. The first element is the 
        desired data and the second is a list of exceptions.
    '''
    except_list = []

    for i, each in enumerate(data):
        ts = time.time()
        current_ts = dt.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        idx = uuid.uuid1()
        url = each.get('response_url')
        if i % 100 == 0:
            print('Step: {} // {}'.format(i, current_ts))
        try:
            each['pdf_url'] = getUrl(url)
            each['idx'] = str(idx)
            each['unique_file_name'] = str(idx) + '_' + str(each.get('pdf_url')).split('/')[-1].split('.')[0].strip()
            each['file_name'] = str(each.get('pdf_url')).split('/')[-1].split('.')[0].strip()

        except:
            each['pdf_url'] = getUrl2(url)
            each['idx'] = str(idx)
            each['unique_file_name'] = str(idx) + '_' + str(each.get('pdf_url')).split('/')[-1].split('.')[0].strip()
            each['file_name'] = str(each.get('pdf_url')).split('/')[-1].split('.')[0].strip()

            print('*** Exception: {} // {} ***'.format(i, current_ts))
            except_list.append(i)
    return [data, except_list]

def check(parsed_data, raw_data):
    len_parsed_split = len([each['pdf_url'].split('.pdf')[1] for each in parsed_data[0] if each['pdf_url'].split('.pdf')[1] == ''])
    len_parsed = len(parsed_data[0])
    len_raw_data = len(raw_data)
    
    if len_parsed_split == len_raw_data:
        return True
    else:
        return False
      
part_191 = 'https://www.phmsa.dot.gov/regulations/title49/part/191'
# part_192 = 'https://www.phmsa.dot.gov/regulations/title49/part/192'

all_url = [i for j in [get_page_urls(url) for url in get_panel_url(part_191)] for i in j]
print('Step 1')
data = [i for j in [parse_single_page(url) for url in all_url] for i in j]
print('Step 2')
parsed_data = main(data)
print('Step 3')
check(parsed_data=parsed_data, raw_data=data)
