import requests


def adp_send_sms(phone_number, message):
    query_params = {
        'mobileno': phone_number,
        'body': message,
        'SecretValue': "x54sdSdTTf6gjDSdfj",
    }

    try:
        r = requests.get("http://91.99.103.210/api/adp/send", params=query_params, timeout=10)
    except Exception as e:
        print(e)
        return False
    else:
        if r.status_code // 100 != 2:
            return False

    return True
