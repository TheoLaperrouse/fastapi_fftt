from mailjet_rest import Client

config = dotenv_values(".env")

def send_mail(recipient, data):
    API_KEY = config['MJ_APIKEY_PUBLIC']
    API_SECRET = config['MJ_APIKEY_PRIVATE']
    mailjet = Client(auth=(API_KEY, API_SECRET))
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
            "Subject": "My first Mailjet Email!",
            "TextPart": data
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return result.json()