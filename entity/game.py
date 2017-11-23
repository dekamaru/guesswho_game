import requests
import random
from entity.image import Image


class Game:

    def __init__(self, person_file):
        self.person_list = []
        self.load_persons(person_file)

    def load_persons(self, person_file):
        print('Loading persons')
        with open(person_file, 'r+') as f:
            persons = f.readlines()

        for person in persons:
            thumbnail = Image.get(person.rstrip())
            self.person_list.append({'name': person.rstrip(), 'thumbnail': thumbnail})
            print('Person "%s" loaded' % person.rstrip())

    def get_persons(self):
        return self.person_list

    def get_game_persons(self, images):
        persons_list = []
        images.sort()
        for index in images:
            persons_list.append({'id': int(index), 'name': self.person_list[int(index)]['name']})
        return persons_list

    def get_image(self, pointer):
        return self.person_list[pointer]

    def get_random_images(self, count):
        numbers = []
        while len(numbers) != count:
            rand_num = random.randint(0, len(self.person_list) - 1)
            if rand_num not in numbers:
                numbers.append(rand_num)
        return ','.join(str(x) for x in numbers)




