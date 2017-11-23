import re
import requests
import time


class Image:

    @staticmethod
    def get(person_name):
        try:
            html = requests.get('https://www.google.ru/search', {'q': person_name, 'tbm': 'isch'}).text
        except Exception:
            print('We have google ban, sleeping 1 minute')
            time.sleep(60)
            return Image.get(person_name)

        m = re.findall('(https://encrypted-tbn0.gstatic.com.*?)"', html)
        return m[0]