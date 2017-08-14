# import os
# import time
# import json
# import requests
# import logging
# errors = logging.getLogger('errors')
#
# # from Crypto.PublicKey import RSA
# # from Crypto.Cipher import PKCS1_v1_5
#
# from base64 import b64encode
#
# from django.conf import settings

#
# f = open(os.path.join(settings.BASE_DIR, 'payments/_assets/raad_key.pem'), 'rb')
# pubkey = RSA.importKey(f.read())
# f.close()


def verify_raad(pay_auth, user_token, amount):
    pass
    # result = False
    #
    # try:
    #     ddd = '%s,%s' % (user_token, int(round(time.time() * 1000)))
    #     cipher = PKCS1_v1_5.new(pubkey)
    #     raad_sign = b64encode(cipher.encrypt(ddd.encode('utf-8')))
    #
    #     url = "https://rad.pec.ir/radapi/v2/payment/verifyPayment"
    #     payload = {'post': {'PayAuth': pay_auth}}
    #     headers = {
    #         'apikey': settings.RAAD_API_KEY,
    #         'sign': raad_sign,
    #         'content-type': "application/json",
    #         'cache-control': "no-cache",
    #     }
    #
    #     # {
    #     #   "Result": {
    #     #     "statusCode": 0,
    #     #     "message": "Verified",
    #     #     "data": {
    #     #       "PayAuth": "44e69a90-8192-4d98-bd4b-96b7d900d6d8",
    #     #       "Amount": 1000,
    #     #       "status": 0,
    #     #       "TraceNumber": 208452,
    #     #       "InvoiceNumber": 704219010595
    #     #     }
    #     #   }
    #     # }
    #
    #     # {
    #     #   "Result": {
    #     #     "statusCode": -1,
    #     #     "message": "Access Denied: 4"
    #     #   }
    #     # }
    #
    #     response = requests.request("POST", url, data=json.dumps(payload), headers=headers)
    #     r_json = response.json()
    #     print('r_json', r_json)
    #     result = (r_json['Result']['statusCode'] == 0 and r_json['Result']['data']['Amount'] == amount * 10)
    # except Exception as e:
    #     print('r_json_except', e)
    #     errors.error(str(e))
    #
    # return result
