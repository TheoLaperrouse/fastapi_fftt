from mailjet_rest import Client
from dotenv import dotenv_values

config = dotenv_values(".env")

def send_mail(recipient, subject, text):
    '''Send a mail to recipient with text'''
    api_key = config['MJ_APIKEY_PUBLIC']
    api_secret = config['MJ_APIKEY_PRIVATE']
    mailjet = Client(auth=(api_key, api_secret))
    data = {
        'Messages': [
            {
            "From": {
                "Email": "fftt_api@gmail.com",
                "Name": "Me"
            },
            "To": [
                {
                "Email": recipient,
                "Name": "You"
                }
            ],
            "Subject": f'FastAPI FFTT : {subject}',
            "TextPart": text
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.json()
