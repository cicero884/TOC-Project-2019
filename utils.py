import requests


GRAPH_URL = "https://graph.facebook.com/v2.6"
ACCESS_TOKEN = "EAAB1HwHN4VwBAHJZAkPeWtBSxii3XB1AEYVJvkgb4Pwbp6w3xdEZBCHxAL0Ya3r9C6df2qSD463EbrlxGtGr1GovWUtfFHA1PYPu7ByO8vx7bEU9fDentxxqwdAC96w3ZABfJQe7sWskB8fxJp2qE94IP1YqJocdff2DedYt7k7kA5x4lnT"


def send_text_message(id, text):
    url = "{0}/me/messages?access_token={1}".format(GRAPH_URL, ACCESS_TOKEN)
    payload = {
        "recipient": {"id": id},
        "message": {"text": text}
    }
    response = requests.post(url, json=payload)

    if response.status_code != 200:
        print("Unable to send message: " + response.text)
    return response


"""
def send_image_url(id, img_url):
    pass

def send_button_message(id, text, buttons):
    pass
"""
