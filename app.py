# Python libraries that we need to import for our bot
import random
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
ACCESS_TOKEN = 'EAAI7rFN3VwgBAPEWabCGV5GbSrWIAtLf2elh4hCOQElZBR5FHp15tCVqaXZBANrtzK2ZCmdhPDNZBCVtCwrKSxg7JnnEu51CZBqbmTnY5Vui99PtB0t9v5ZB2XjkC4d3A5sNwvq0vxMNMEIfnnkjF7xNFS5dKN1kqgQfGZBFbmXrNZBPCzePvtIv'
VERIFY_TOKEN = 'u++57drXp8pWo8blt7Ym+vffSOLFGS2C/GfKYTGKKJo='
bot = Bot(ACCESS_TOKEN)


# We will receive messages that Facebook sends our bot at this endpoint
@app.route("/", methods=['GET', 'POST'])
def receive_message():
    if request.method == 'GET':
        """Before allowing people to message your bot, Facebook has implemented a verify token
        that confirms all requests that your bot receives came from Facebook."""
        token_sent = request.args.get("hub.verify_token")
        return verify_fb_token(token_sent)
    # if the request was not get, it must be POST and we can just proceed with sending a message back to user
    else:
        # get whatever message a user sent the bot
        output = request.get_json()
        for event in output['entry']:
            messaging = event['messaging']
            for message in messaging:
                if message.get('message'):
                    # Facebook Messenger ID for user so we know where to send response back to
                    recipient_id = message['sender']['id']
                    if message['message'].get('text'):
                        response_sent_text = get_automated_message(message['message'].get('text'))
                        send_message(recipient_id, response_sent_text)
                    # if user sends us a GIF, photo,video, or any other non-text item
                    if message['message'].get('attachments'):
                        response_sent_nontext = get_message()
                        send_message(recipient_id, response_sent_nontext)
    return "Message Processed"


def verify_fb_token(token_sent):
    # take token sent by facebook and verify it matches the verify token you sent
    # if they match, allow the request, else return an error
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


# chooses a random message to send to the user
def get_message():
    sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!",
                        "We're grateful to know you :)"]
    # return selected item to the user
    return random.choice(sample_responses)


# chooses an automated response to the message depending on the substance of the message
def get_automated_message(message):
    message = message.lower()
    response = "With FoodE, you have a ton of options to choose from. Visit our facebook here: https://www.facebook.com/FoodEOfficial/"
    response_2 = "You can contact us by emailing foodEofficial@gmail.com with any comments or concerns. Also, feel free to reach out to us on instagram @foodEOfficial!/"
    about = "FoodE is a fun and innovative way to connect with local restaurants in order to get the delicious meals you deserve. Eating out has never been so easy and accessible. Save the meals you want, discard the ones you don't."
    dev_message = "FoodE is still in development, but like us on FaceBook, follow us on Instagram, and sign up for our mailing list to stay up to date on the latest versions of the app."
    how_are_you_replies = ["I'm hungry, let's find a place to eat.", "I'm happy you're here.",
                           "I'm sad that millions of people struggle to decide where to eat every day. If only they had access to FoodE..."]
    celeb_replies = [
        "David Chang is a chef and restaranteur who explores the culture and evolution of staples from around the world like pizza on his Netflix show, \"Ugly Delicious\". FoodE Fun Fact: He's from Northern Virginia!",
        "Michelle Obama's \"Let's Move!\" campaign encouraged youth to eat healthier foods and exercise more. FoodE Fun Fact: She had bee hives installed on the White House South Lawn!",
        "Gordon Ramsay is a celebrity chef known for his high-end restaurants and variety of food-based TV series. FoodE Fun Fact: He was raised in the William Shakespeare's birthplace!",
        "Anthony Bourdain was a chef and food critic famous for his exploration of diverse cultures and their foods in \"Anthony Bourdain: No Reservations\". May he rest in peace"]
    if "problem" in message or "complaint" in message or "confused" in message or "help" in message:
        return response_2
    elif "what" in message and "foode" in message or "this" in message:
        return about
    elif "when" in message and "foode" in message or "app" in message or "release" in message:
        return dev_message
    elif "restaurant" in message or "food" in message or "eat" in message:
        return response
    elif "how" in message or "are you" in message or "what's up" in message:
        return random.choice(how_are_you_replies)
    elif "David Chang".lower() in message:
        return celeb_replies[0]
    elif "Michelle Obama".lower() in message:
        return celeb_replies[1]
    elif "Gordon Ramsay".lower() in message or "Chef Ramsay".lower() in message:
        return celeb_replies[2]
    elif "Anthony Bourdain".lower() in message:
        return celeb_replies[3]
    else:
        return "I'm sorry, we don't quite understand."


# uses PyMessenger to send response to user
def send_message(recipient_id, response):
    # sends user the text message provided via input response parameter
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run()
