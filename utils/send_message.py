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

    if r.status_code // 100 == 2:
        return True

    return False


# def adp_send(phone_number, msg):
#     """
#     API to send sms by adp
#     :param phone_number:
#     :param msg:
#     :return: status and returned message by server
#     """
#     query_params = {
#         'mobileno': phone_number,
#         'body': msg,
#         'SecretValue': "x54sdSdTTf6gjDSdfj",
#     }
#
#     try:
#         r = requests.get(
#             "http://91.99.103.210/api/adp/send",
#             params=query_params,
#             timeout=10
#         )
#     except Exception as e:
#         return False, str(e)
#
#     if r.status_code // 100 == 2:
#         return True, r.text
#     else:
#         return False, 'server status code: %s' % r.status_code
