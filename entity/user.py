import hashlib

class User:

    def __init__(self, db, ip):
        self.db = db

        self.ip = ip
        self.is_playing = False
        self.session_name = None
        self.images = None
        self.good = 0
        self.bad = 0
        self.pointer = 0

        # load user data
        c = db.cursor()
        c.execute("SELECT * FROM game_sessions WHERE user_ip = :uip AND session_status = 0", {"uip": self.ip})
        user_data = c.fetchone()
        c.close()
        if user_data is None:
            self.is_playing = False
        else:
            self.is_playing = True
            self.session_name = user_data[1]
            self.images = user_data[4].split(',')
            self.pointer = int(user_data[5])
            self.good = int(user_data[6])
            self.bad = int(user_data[7])

    def make_decision(self, user_choice):
        right_index = self.images[self.pointer]
        if right_index == user_choice:
            self.good += 1
        else:
            self.bad += 1

        self.pointer += 1

        c = self.db.cursor()
        c.execute('UPDATE game_sessions SET pointer = :p, good = :g, bad = :b WHERE session_name = :sn', {
            'p': self.pointer,
            'g': self.good,
            'b': self.bad,
            'sn': self.session_name
        })
        c.close()

    def close_game(self):
        c = self.db.cursor()
        c.execute('UPDATE game_sessions SET session_status = 1 WHERE session_name = :sn', {'sn': self.session_name})
        self.is_playing = False
        c.close()

    def get_last_games(self):
        c = self.db.cursor()
        c.execute("SELECT * FROM game_sessions WHERE user_ip = :uip AND session_status = 1", {"uip": self.ip})
        last_games = c.fetchall()
        c.close()
        return last_games

    def start_game(self, game, difficult):
        difficult_counts = [10, 50, 100]
        images = game.get_random_images(difficult_counts[int(difficult)])
        session_name = hashlib.md5((self.ip + images).encode('utf-8')).hexdigest()

        c = self.db.cursor()
        c.execute('INSERT INTO game_sessions VALUES (:uip, :sname, 0, :diff, :ims, 0, 0, 0)', {
            'uip': self.ip,
            'sname': session_name,
            'diff': difficult,
            'ims': images
        })

        return session_name

    def is_playing(self):
        return self.is_playing