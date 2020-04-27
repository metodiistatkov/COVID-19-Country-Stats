from __future__ import print_function
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText

from google.protobuf.any_pb2 import Any
from googleapiclient.discovery import build, Resource
import googleapiclient.errors as mail_errors
from httplib2 import Http
from oauth2client import tools, client, file
from oauth2client.client import Storage, OAuth2WebServerFlow

from Crawler import scrape

# Be careful! This scope gives full e-mail permissions (including deletion of mails)
# For more information about scopes check the relevant Gmail api sections
SCOPES: list = ['https://mail.google.com/']
COUNTRIES: list = ['Bulgaria', 'UK']
SUBJECT: str = 'COVID-19 Daily Stats'


# https://developers.google.com/gmail/api/guides/sending
def __create_message(sender: str, to: str, subject: str, message_text: str) -> dict:
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    encoded_message = urlsafe_b64encode(message.as_bytes())
    return {'raw': encoded_message.decode()}


def __send_message(service: Resource, user_id: str, message: str) -> str:
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    except mail_errors.HttpError as error:
        print('An error occurred: %s' % error)


def __send_emails(emails: list, service: Resource, msg_text: str) -> None:
    if not emails:
        print('Add at least one e-mail recipient!')
    else:
        for email in emails:
            message: dict = __create_message('me', email, SUBJECT, msg_text)
            outcome: str = __send_message(service, 'me', message)
            print(outcome)


def __get_info(countries: list) -> str:
    countries_info: list = list()
    for country in countries:
        info: str = scrape('https://www.worldometers.info/coronavirus/#countries', 'div', 'main_table_countries_div',
                           country)
        countries_info.append(info)

    result: str = '\n---------------------------\n'.join(countries_info)
    return result


def main():
    store: Storage = file.Storage('credentials.json')
    creds: Any = store.get()
    if not creds or creds.invalid:
        flow: OAuth2WebServerFlow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds: Any = tools.run_flow(flow, store)
    service: Resource = build('gmail', 'v1', http=creds.authorize(Http()))

    # get daily statistics regarding Covid-19 for the desired country
    msg_text: str = __get_info(COUNTRIES)
    emails: list = []  # populate emails of desired recipients
    __send_emails(emails, service, msg_text)


if __name__ == '__main__':
    main()
