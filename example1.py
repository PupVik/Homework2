class BoardException(Exception):
    pass

class BoardOutException(BoardException):
    def __str__(self):
        return 'Вы стреляете за пределы поле!'

class BoardUsedException(BoardException):
    def __str__(self):
        return 'Вы уже стреляли в эту клетку'

class BoardWrongShipException(BoardException):
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

class Ship:
    def __init__(self, nose, lenght, direction, life):
        self.nose = nose
        self.lenght = lenght
        self.direction = direction
        self.life = life


    @property
    def dots(self):
        ship_dots = []
        for i in range(self.lenght):
            cur_x = self.nose.x
            cur_y = self.nose.y

            if self.direction == 0:
                cur_x += i

            elif self.direction == 1:
                cur_y += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hid=False, size=6):
        self.size = size
        self.hid = hid

        self.count = 0

        self.field = [["."] * size for _ in range(size)]

        self.busy = []
        self.ships = []

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardWrongShipException()

        for d in ship.dots:
            self.field[d.x][d.y] = "°"
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, sp=False):
        n = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        for d in ship.dots:
            for dx, dy in n:
                cur = Dot(d.x + dx, d.y + dy)
                if not (self.out(cur)) and cur not in self.busy:
                    if sp:
                        self.field[cur.x][cur.y] = "/"
                    self.busy.append(cur)

    def __str__(self):
        res = ""
        res += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid:
            res = res.replace("°", "/")
        return res

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardUsedException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lifes -= 1

                self.field[d.x][d.y] = "x"
                if ship.lives == 0:
                    self.count += 1
                    self.contour(ship, sp=True)
                    self.field[d.x][d.y] = "X"
                    print('Убил')
                    return True
                else:
                    print('Ранил')
                    return True

        self.field[d.x][d.y] = "~"
        print('Мимо')
        return False

    def begin(self):
        self.busy = []


class Player:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход компьютера: {d.x + 1} {d.y + 1}')
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input('Ваш ход: ').split()

            if len(cords) != 2:
                print(' Введите 2 координаты!')
                continue

            x, y = cords
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)

class Game:
    def __init__(self, size=6):
        self.size = size
        pl = self.random_board()
        co = self.random_board()
        co.hid = True

        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board

    def greet(self):
        print('Приветствуем в игре Морской бой!')
        print('Правила:')
        print('Пользователь играет с компьютером и ходит первый')
        print('Необходимо ввести 2 координаты - номер строки и столбца')
        print('Поехали!')

    def game(self):
        num = 0
        while True:
            print('-' * 27)
            print('Доска Пользователя:')
            print(self.us.board)
            print('-' * 27)
            print('Доска Компьютера:')
            print(self.ai.board)
            time.sleep(3)
            if num % 2 == 0:
                print('-' * 27)
                time.sleep(1)
                print('Ход Пользователя: введите строку и столбец через пробел')
                repeat = self.us.move()
            else:
                print('-' * 27)
                print('Ход Компьютера: ')
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print('-' * 27)
                print('Пользователь победил!')
                break

            if self.us.board.count == 7:
                print('-' * 27)
                print('Компьютер победил!')
                break
            num += 1

    def loop(self):
        self.mode

    def start(self):
        self.greet("")
        self.loop("")

    Game = Game()
    Game.start

    def start(self):
        self.game()