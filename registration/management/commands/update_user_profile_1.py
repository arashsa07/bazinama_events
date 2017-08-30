import requests

from django.core.management.base import BaseCommand
from django.utils import timezone

from registration.models import UserProfile


HEADERS = {'host': 'itzunami.net'}
BASE_URL = 'http://104.24.109.200:80/chestroyale/view.php?t=%s&v=26&r=a'


class Command(BaseCommand):
    help = 'Update profile of user (version 1)'

    def handle(self, *args, **options):
        for profile in UserProfile.objects.all():
            if profile.user.payment_set.filter(paid_status=True).count() == 0:
                continue
            if profile.clash_info_updated_time and profile.clash_info_updated_time > timezone.now() - timezone.timedelta(hours=1):
                continue

            print(profile.user.phone_number, profile.clash_id, profile.nick_name, profile.user.id)

            url = BASE_URL % profile.clash_id

            try:
                response = requests.get(url=url, headers=HEADERS, timeout=20)
                result = response.json()
            except Exception as e:
                print('Error: %s' % str(e))
                profile.clash_info = 'ERROR: %s' % str(e)
            else:
                if result['userinfo']['s1'] and result['userinfo']['livello']:
                    profile.cup_numbers = int(result['userinfo']['s1'])
                    profile.level = int(result['userinfo']['livello'])
                    profile.clash_info = result
                    profile.clash_info_updated_time = timezone.now()

                    cup_numbers = int(result['userinfo']['s1']) if result['userinfo']['s1'] else 0
                    level = int(result['userinfo']['livello']) if result['userinfo']['livello'] else 0
                    print('level: %s ---> %s' % (profile.level, level))
                    print('cups: %s ---> %s' % (profile.cup_numbers, cup_numbers))

            profile.save()

            print('-' * 80)


sample_result = {
    "s": "cr",
    "userinfo": {
        "stato": "1",
        "tag": "2098L999",  # clash id
        "username": "bardia",  # name
        "livello": "10",  # level
        "clan": "nowshahr",  # clan
        "clantag": "2GQJL829",
        "s1": "2801",  # Highest trophies
        "s2": "2657",  # Last known trophies
        "s3": "781",  # Challenge cards won
        "s4": "38",  # Tourney cards won
        "s5": "8736",  # Total donation
        "s6": "0",  # Prev season rank
        "s7": "0",  # Prev season trophies
        "s8": "0",  # Prev season highest
        "s9": "1002",  # Wins
        "s10": "1033",  # Loses
        "s11": "735"  # 3 crown wins
    },
    "l": "2017-08-21 07:00:23",
    "c": "0:1|1:0|2:0|3:0|4:0|5:1|6:0|7:0|8:1|24:3|45:4|295:5|349:2|531:6",
    "clanlist": [
        {"username": "bardia", "livello": "10", "tag": "2098L999"}
    ]
}
