import sqlite3
from vendor.bottle import *
from entity.user import User
from entity.game import Game
import sys


class GuessWhoApplication:

    def __init__(self, argv):
        self.db = None
        self.game = Game(argv[1])

    def init_db(self):
        self.db = sqlite3.connect(':memory:')
        c = self.db.cursor()
        with open('migration.sql', 'r+') as migration_file:
            c.execute(migration_file.read().replace('\n', ''))
        c.close()

    def run(self):
        self.init_db()
        run(host='localhost', port=8080)


# web endpoint
@route('/')
def index():
    user = User(app.db, request.environ.get('REMOTE_ADDR'))
    if user.is_playing:
        redirect('/play/' + user.session_name)
    else:
        redirect('/new')


@route('/new')
@post('/new')
def new_game():
    user = User(app.db, request.environ.get('REMOTE_ADDR'))
    if user.is_playing:
        redirect('/play/' + user.session_name)

    difficult = request.forms.get('difficult')
    if difficult is None:
        last_games = user.get_last_games()
        return template('views/new_game.html', {'last_games': last_games})
    else:
        # create new game
        session = user.start_game(app.game, difficult)
        redirect('/play/' + session)


@route('/play/<hash>')
@post('/play/<hash>')
def play(hash):
    user = User(app.db, request.environ.get('REMOTE_ADDR'))
    if user.session_name == hash:
        user_choice = request.forms.get('person')
        if user_choice is None:
            current_img = app.game.get_image(int(user.images[user.pointer]))['thumbnail']
            persons = app.game.get_game_persons(user.images)
            return template('views/game.html', {'user': user, 'img': current_img, 'persons': persons})
        else:
            user.make_decision(user_choice)
            if user.pointer == len(user.images):
                user.close_game()
                redirect('/new')
            else:
                redirect('/play/' + hash)
    else:
        redirect('/new')



@route('/static/<path:path>')
def static_request(path):
    return static_file(path, root='static')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('USAGE: ./run.py <file_with_persons_list>')
    app = GuessWhoApplication(sys.argv)
    app.run()
