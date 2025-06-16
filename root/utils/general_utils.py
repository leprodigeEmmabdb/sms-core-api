import string
import random
from twilio.rest import Client


def get_user(request):
    user = None
    user_id = None
    if request and hasattr(request, "user"):
        user = request.user
        user_id = user.id
    return user, user_id

def generate_opt_code(length=6):
    digits = string.digits.replace('0', '')
    result_str = ''.join(random.choice(digits) for i in range(length))
    return result_str  # f"{result_str[:3]}-{result_str[-3:]}"

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str


def generate_temp_pwd(length=6):
    digits = string.digits.replace('0', '')
    result_str = ''.join(random.choice(digits) for i in range(length))
    return result_str  # f"{result_str[:3]}-{result_str[-3:]}"


def send_sms(phone, message):
    # pass
    account_sid = "ACc5f2bfcce4e30319b30ab1e4e095bf30"
    auth_token = "50f09222db33b21c5cdbe83896f8ba7d"
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=message,
        from_='CRU',
        to=phone
    )

    return message.sid


def convertSecondsToHoursMinSec(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


def convertSecondsToMinSec(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    if minutes > 0:
        return "%02d min %02d sec" % (minutes, seconds)
    return "%02d sec" % seconds
