import requests
from datetime import datetime
from django.conf import settings
from django.core.cache import cache


def verify_bazaar(package_name, product_id, purchase_token, item_type):
    if item_type == 2:
        item_type_text = "applications", "subscriptions"
    else:
        item_type_text = "validate", "inapp"

    access_token = cache.get('bazaar_token', None)
    # if access_token:
    #     access_token = access_token.access_token
    # generate url refer to type and passed parameters
    url_to_check = settings.BAZAAR_URLPATTERN % (
        item_type_text[0], package_name, item_type_text[1], product_id,
        purchase_token)
    try:
        result = requests.get(url_to_check, verify=False,
                              headers={"Authorization": access_token})
        if result.status_code == 404:
            return False
        if result.status_code in [403, 401]:
            data_to_refresh_token = {
                "grant_type": "refresh_token",
                "client_id": settings.BAZAAR_CLIENT_ID,
                "client_secret": settings.BAZAAR_CLIENT_SECRET,
                "refresh_token": settings.BAZAAR_REFRESH_TOKEN
            }
            get_refresh = requests.post(settings.BAZAAR_REFRESH_URL,
                                        data=data_to_refresh_token)
            if get_refresh.status_code == 200:
                access_token = get_refresh.json()["access_token"]
                cache.set('access_token', access_token)
                result = requests.get(url_to_check, verify=False,
                                      headers={"Authorization": access_token})
            else:

                return False

        if result.status_code == 200:
            result_json = result.json()

            if item_type == 1 and (
                            'consumptionState' in result_json and 'purchaseState' in result_json) and \
                            result_json[
                                'consumptionState'] == 1 and \
                            result_json['purchaseState'] == 0:
                return True
            elif "validUntilTimestampMsec" in result_json and datetime.fromtimestamp(
                            float(result_json[
                                      "validUntilTimestampMsec"]) / 1000) > datetime.now():
                return True
        return False

    except Exception as e:
        return False
