import logging

import zeep
from zeep.cache import InMemoryCache
from zeep.transports import Transport

"""
set of function all related to shahparak bank payment gateway
"""

errors = logging.getLogger('errors')
transport = Transport(cache=InMemoryCache())


def verify_saman(wsdl, ref_number, mid, real_amount):
    result = False
    try:
        client = zeep.Client(wsdl=wsdl, transport=transport)

        res = client.service.verifyTransaction(str(ref_number), str(mid))
        if int(res) == real_amount:
            result = True
    except Exception as e:
        errors.error(str(e))

    return result