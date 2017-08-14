import logging

import zeep
from zeep.cache import InMemoryCache
from zeep.transports import Transport

"""
set of function all related to shahparak bank payment gateway
"""

errors = logging.getLogger('errors')
transport = Transport(cache=InMemoryCache())


def login(username, password, wsdl):
    """
    bank needs to confirm payment after each pay.
    server must login first to start confirmation
    this operation work with soap communication api

    :return: a True or false plus a session to use for verify transaction
    """
    try:
        client = zeep.Client(wsdl=wsdl, transport=transport)
        zeep.Client()
        return (True, client.service.login({"username": username, "password": password}))
    except Exception as e:
        errors.error(str(e))
        return False, None


def verify(session, ref, wsdl):
    """
    get a ref id and verify a transaction. if this not happen all the money cash back
    to bank and user acount automatically after a while.
    :param session: a session that received from login process
    :param ref: reference id that bank send to server after payment
    :param wsdl: bank soap wsdl address
    :return: True or False for result and amount of confirmed transaction
    """
    try:
        client = zeep.Client(wsdl=wsdl, transport=transport)
        data = {'context': {'data': {'entry': {'key': 'SESSION_ID', 'value': session}}},
                'verifyRequest': {'refNumList': [str(ref)]}}
        res = client.service.verifyTransaction(**data)
        amount = res.verifyResponseResults[0].amount
        if amount:
            return True, int(amount)
        return False, None
    except Exception as e:
        errors.error(str(e))
        return False, None


def check_payment(username, password, url, amount, ref_id):
    """
    login and confirm a transaction use above functions
    :return: Tru or False in diffrent situations
    """
    login_res, login_data = login(username, password, url)
    if login_res:
        verify_res, verify_amount = verify(login_data, ref_id, url)
        if verify_res and verify_amount == amount:
            return True

    return False


def verify_shaparak(gateway, ref_id, amount):
    """
    the only public function of shahparak pay that get all
    needed parameters and return a true or false in result
    """
    return check_payment(gateway.merchant_id, gateway.merchant_pass, gateway.check_url, amount, ref_id)
