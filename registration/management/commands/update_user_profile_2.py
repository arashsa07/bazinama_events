from time import sleep
import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand
from django.utils import timezone

from registration.models import UserProfile


BASE_URL = 'https://statsroyale.com/profile/%s'
REFRESH_URL = 'https://statsroyale.com/profile/%s/refresh'

SUCCESS_MESSAGE = 'Refresh Started!'
FAILED_MESSAGE_1 = 'Profile was refreshed recently. Please try again later.'
FAILED_MESSAGE_2 = 'Invalid Hashtag'


class Command(BaseCommand):
    help = 'Update profile of user (version 2)'

    def handle(self, *args, **options):
        for profile in UserProfile.objects.all():
            if profile.user.payment_set.filter(paid_status=True).count() == 0:
                continue
            if profile.clash_info_updated_time and profile.clash_info_updated_time > timezone.now() - timezone.timedelta(hours=1):
                continue

            print(profile.user.phone_number, profile.clash_id, profile.nick_name, profile.user.id)

            refresh_url = REFRESH_URL % profile.clash_id
            url = BASE_URL % profile.clash_id

            try:
                refresh_response = requests.get(url=refresh_url, timeout=20)
                refresh_result = refresh_response.json()
            except Exception as e:
                print('Refresh Error: %s' % str(e))
                sleep(10)
            else:
                if refresh_result['success']:
                    sleep(refresh_result['secondsToUpdate'] + 10)

            try:
                response = requests.get(url=url, timeout=20)
                soup = BeautifulSoup(response.content, 'html.parser')
                level = soup.find('span', class_='profileHeader__userLevel').get_text()
                stats = soup.find('div', class_='statistics')
                result_list = stats.get_text().split('\n')

                result = {}

                for i in range(0, len(result_list), 2):
                    if result_list[i]:
                        result[result_list[i+1]] = result_list[i]

                cup_numbers = int(result['Highest trophies'])
                level = int(level)
                profile.cup_numbers = cup_numbers
                profile.level = level
                profile.clash_info = result
                profile.clash_info_updated_time = timezone.now()

                print('level: %s ---> %s' % (profile.level, level))
                print('cups: %s ---> %s' % (profile.cup_numbers, cup_numbers))

            except Exception as e:
                print('Profile ERROR: %s' % str(e))
                profile.clash_info = 'ERROR: %s' % str(e)

            profile.save()
            print('-' * 80)


sample_result = {
    '3 crown wins': ' 10 ',
    'Challenge cards won': '0',
    'Highest trophies': '312',
    'Last known trophies': '312',
    'League': 'None',
    'Loses': '8',
    'Prev season highest': '0',
    'Prev season rank': '0',
    'Prev season trophies': '0',
    'Total donations': '3',
    'Tourney cards won': '0',
    'Wins': '11'
}

# http://statsroyale.com/profile/2098L999
# http://statsroyale.com/profile/2098L999/refresh
# {
# "success": true,
# "message": "Refresh Started!",
# "count": 17,
# "secondsToUpdate": 3
# }
# {
# "success": false,
# "message": "Profile was refreshed recently. Please try again later."
# }
# {
# "success": false,
# "message": "Invalid Hashtag"
# }
