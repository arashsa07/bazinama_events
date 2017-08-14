import requests
from django.conf import settings




if hasattr(settings, "PAYMENT") and 'vas_url' in settings.PAYMENT and 'vas_service_id' in settings.PAYMENT:
    VAS_URL = settings.PAYMENT['vas_url']
    VAS_SERVICE_ID = settings.PAYMENT['vas_service_id']
elif hasattr(settings, 'VAS_URL') and hasattr(settings, 'VAS_SERVICE_ID'):
    VAS_URL = settings.VAS_URL
    VAS_SERVICE_ID = settings.VAS_SERVICE_ID
else:
    VAS_URL = None
    VAS_SERVICE_ID = None




def aware_settle(token, vas_url=None, vas_service_id=None):
    if not vas_url or not vas_service_id:
        vas_url = VAS_URL
        vas_service_id = VAS_SERVICE_ID

    try:
        data = {

            "is_settled": True
        }
        response = requests.put(url='%s/%s/payments/%s/' % (vas_url, vas_service_id, str(token)),
                                json=data)
        if response.status_code in [200, 201, 202]:
            return True
        return False
    except:
        return False


def do_settle(token, amount, vas_url=None, vas_service_id=None):
    if not vas_url or not vas_service_id:
        vas_url = VAS_URL
        vas_service_id = VAS_SERVICE_ID

    try:
        data = {
            "settle_price": amount * 10
        }
        response = requests.put(
            url='%s/%s/payments/%s/settle/' % (vas_url, vas_service_id, str(token)),
            json=data)
        if response.status_code in [200, 201, 202]:
            response = response.json()
            if response['status'] == 10:
                return True

        return False
    except:
        return False
