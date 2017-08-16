import requests
from bs4 import BeautifulSoup

from django.core.management.base import BaseCommand

from registration.models import UserProfile


ROYAL_STATS_URL = 'https://statsroyale.com/profile/'


class Command(BaseCommand):
    help = 'Update profile of user'

    def handle(self, *args, **options):
        for profile in UserProfile.objects.all():
            if profile.clash_id.startswith('#'):
                url = ROYAL_STATS_URL + profile.clash_id[1:]
            else:
                url = ROYAL_STATS_URL + profile.clash_id

            response = requests.get(url, timeout=20)
            if response.status_code == requests.codes.ok:
                soup = BeautifulSoup(response.content, 'html.parser')
                result = {}
                try:
                    level = soup.find('span', class_='profileHeader__userLevel').get_text()
                    stats = soup.find('div', class_='statistics')
                    result_list = stats.get_text().split('\n')
                    for i in range(0, len(result_list), 2):
                        if result_list[i]:
                            result[result_list[i+1]] = result_list[i]
                    profile.cup_numbers = int(result['Last known trophies'])
                    profile.level = int(level)
                    print()
                    print(result)
                    print(level)
                    print()

                except Exception as e:
                    print('user: %s, with clash_id: %s, ERROR: %s' % (profile.user.id, profile.clash_id, str(e)))
                else:
                    print('user: %s, with clash_id: %s, DONE.' % (profile.user.id, profile.clash_id))
                # profile.stats = result
                profile.save()

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
