from mailchimp3 import MailChimp
import datetime as dt
from string import Template

# This is the email template.
index = open('phmsa-email-template.html', 'r').read()
string_template = Template(str(index))

# String that is included in the email. 
# This will be the data from the API call, formatted as a string.
body_text = 'Lorem ipsum dolor sit amet, consectetuer adipiscing elit. \
             Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque \
             penatibus et magnis dis parturient montes, nascetur ridiculus mus. \
             Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. \
             Nulla consequat massa quis enim. Donec pede justo, fringilla vel, \
             aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet \
             a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. \
             Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. \
             Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, \
             consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, \
             viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus \
             varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies \
             nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. \
             Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem \
             quam semper libero, sit amet adipiscing sem neque sed ipsum. \
             Nam quam nunc, blandit vel, luctus pulvinar, hendrerit id, lorem. \
             Maecenas nec odio et ante tincidunt tempus. \
             Donec vitae sapien ut libero venenatis faucibus.'

API_KEY = API_KEY
USER_NAME = USER_NAME

client = MailChimp(mc_api=API_KEY, mc_user=USER_NAME)

current_ts = dt.datetime.now()
ts = str(current_ts.strftime("%Y-%m-%d %H:%M:%S"))
data = {'recipients': {'list_id': 'ad1c784b97'}, 
                       'settings': {'subject_line': 'Test List From Python Script ' + ts + ' html', 
                                    'from_name': 'Meet SMYS', 
                                    'reply_to': 'hello@meetsmys.com'},
                       'type': 'regular'}

create_new_campaign = client.campaigns.create(data=data) 
updated_campaign = client.campaigns.content.update(campaign_id = create_new_campaign['id'], 
                                data={'message': 'some test', 
                                      'html': string_template.safe_substitute(code=body_text)})
