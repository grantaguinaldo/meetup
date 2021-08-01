from mailchimp3 import MailChimp
import datetime as dt
from string import Template

index = open('phmsa-email-template.html', 'r').read()
string_template = Template(str(index))

current_ts = dt.datetime.now()
date = str(current_ts.strftime("%B %d, %Y"))

body_text = 'Body Text. Lorem ipsum dolor sit amet, consectetuer adipiscing elit.'
intro_text = '<strong>' + date + '</strong>' + ': SMYS has found updates to the Federal Register.'

API_KEY = API_KEY
USER_NAME = USER_NAME

def create_campaign(API_KEY, USER_NAME, body_text, intro_text):
    client = MailChimp(mc_api=API_KEY, mc_user=USER_NAME)

    current_ts = dt.datetime.now()
    ts = str(current_ts.strftime("%Y-%m-%d %H:%M:%S"))
    data = {'recipients': {'list_id': 'ad1c784b97'}, 
                           'settings': {'subject_line': 'PHMSA Updates ' + ts, 
                                        'from_name': 'Grant T. Aguinaldo', 
                                        'reply_to': 'grant@grantaguinaldo.com'},
                           'type': 'regular'}

    create_new_campaign = client.campaigns.create(data=data) 
    updated_campaign = client.campaigns.content.update(campaign_id=create_new_campaign['id'], 
                                    data={'message': 'Updates from SMYS.', 
                                          'html': string_template.safe_substitute(body_text=body_text, 
                                                                                  intro_text=intro_text)})
    return updated_campaign   

create = create_campaign(API_KEY=API_KEY, USER_NAME=USER_NAME, body_text=body_text, intro_text=intro_text)
