import boto3
import requests as r
import json
import uuid
import datetime as dt

Access_Key_ID = '[xxx]'
Secret_Access_Key = '[xxx]'
dynamodb = boto3.resource('dynamodb', 
                          region_name = 'us-west-2', 
                          aws_access_key_id=Access_Key_ID, 
                          aws_secret_access_key=Secret_Access_Key)


agency = 'epa' #, 'samhsa' #'gao' , #tsa #'phmsa' 
table = dynamodb.Table(agency + '-fr-entries')

#url = 'https://www.federalregister.gov/api/v1/agencies/pipeline-and-hazardous-materials-safety-administration'
#url = 'https://www.federalregister.gov/api/v1/agencies/government-accountability-office'
#url = 'https://www.federalregister.gov/api/v1/agencies/substance-abuse-and-mental-health-services-administration'
#url = 'https://www.federalregister.gov/api/v1/agencies/environmental-protection-agency'
#url = 'https://www.federalregister.gov/api/v1/agencies/transportation-security-administration'

recent_articles_url = r.get(url).json()['recent_articles_url']

url_list = []
def get_next_url(url):    
    try:
        next_url = r.get(url).json()['next_page_url']
        url_list.append(next_url)
        get_next_url(next_url)
    except:
        pass
    return url_list

urls = get_next_url(recent_articles_url)

for j, e in enumerate(urls):
    data = r.get(e)
    for z, each in enumerate(data.json()['results']):
        results_dict = dict()
        results_dict['agency'] = agency
        current_ts = dt.datetime.now()
        results_dict['dw_ts'] = str(current_ts.strftime("%Y-%m-%d %H:%M:%S"))
        results_dict['id'] = str(uuid.uuid4())
        results_dict['title'] = each['title']
        results_dict['abstract'] = each['abstract']
        results_dict['document_number'] = each['document_number']
        results_dict['html_url'] = each['html_url']
        results_dict['pdf_url'] = each['pdf_url']
        results_dict['publication_date'] = each['publication_date']
        table.put_item(Item=results_dict)
        print('Step: {} // {} // {}'.format(j, z, current_ts.strftime("%Y-%m-%d %H:%M:%S")))
        
#Data on the first page.
for i, each in enumerate(r.get(r.get(url).json()['recent_articles_url']).json()['results']):
    results_dict = dict()
    current_ts = dt.datetime.now()
    results_dict['agency'] = agency
    results_dict['dw_ts'] = str(current_ts.strftime("%Y-%m-%d %H-%M-%S"))
    results_dict['id'] = str(uuid.uuid4())
    results_dict['title'] = each['title']
    results_dict['abstract'] = each['abstract']
    results_dict['document_number'] = each['document_number']
    results_dict['html_url'] = each['html_url']
    results_dict['pdf_url'] = each['pdf_url']
    results_dict['publication_date'] = each['publication_date']
    table.put_item(Item=results_dict)
    print('Step: {} // {}'.format(i, current_ts.strftime("%Y-%m-%d %H-%M-%S")))
