# mb


import os
import random

class Ship:
    def __init__(self, size):
        self.size = size
        self.coords = []  # Список кортежей (x, y)
        self.hits = set() # Попадания по кораблю

    def is_sunk(self):
        return len(self.hits) == self.size


class Board:
    def __init__(self):
        self.size = 10
        # '~' - пусто, '■' - корабль, 'X' - попадание, '•' - промах
        self.grid = [['~' for _ in range(self.size)] for _ in range(self.size)]
        self.ships = []

    def display(self, hide_ships=False):
        """Отрисовка поля в консоли."""
        print("   " + " ".join(str(i) for i in range(1, 11)))
        for y in range(self.size):
            row_display = []
            for x in range(self.size):
                cell = self.grid[y][x]
                if hide_ships and cell == '■':
                    row_display.append('~')
                else:
                    row_display.append(cell)
            print(f"{y + 1:2} " + " ".join(row_display))

    def can_place_ship(self, x, y, size, direction):
        """Проверка, можно ли поставить корабль (включая зазор в 1 клетку)."""
        coords = []
        for i in range(size):
            nx = x + (i if direction == 'Г' else 0)
            ny = y + (i if direction == 'В' else 0)

            # Проверка выхода за границы поля
            if not (0 <= nx < self.size and 0 <= ny < self.size):
                return False

            # Проверка соседних клеток (корабли не должны касаться)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    cx, cy = nx + dx, ny + dy
                    if 0 <= cx < self.size and 0 <= cy < self.size:
                        if self.grid[cy][cx] == '■':
                            return False
            coords.append((nx, ny))
        return coords

    def place_ship(self, size, x, y, direction):
        """Размещение корабля на поле."""
        coords = self.can_place_ship(x, y, size, direction)
        if not coords:
            return False

        ship = Ship(size)
        ship.coords = coords
        for cx, cy in coords:
            self.grid[cy][cx] = '■'
        self.ships.append(ship)
        return True

    def auto_place_ships(self, fleet):
        """Случайная расстановка всех кораблей (для быстрой проверки)."""
        for size in fleet:
            placed = False
            while not placed:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                direction = random.choice(['Г', 'В'])
                placed = self.place_ship(size, x, y, direction)

    def receive_shot(self, x, y):
        """Обработка выстрела по координатам (x, y)."""
        cell = self.grid[y][x]
        if cell in ('X', '•'):
            return 'repeat'
        elif cell == '~':
            self.grid[y][x] = '•'
            return 'miss'
        elif cell == '■':
            self.grid[y][x] = 'X'
            for ship in self.ships:
                if (x, y) in ship.coords:
                    ship.hits.add((x, y))
                    if ship.is_sunk():
                        self.mark_surrounding(ship)
                        return 'killed'
                    return 'injured'

    def mark_surrounding(self, ship):
        """Обводит потопленный корабль точками автоматически."""
        for sx, sy in ship.coords:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    cx, cy = sx + dx, sy + dy
                    if 0 <= cx < self.size and 0 <= cy < self.size:
                        if self.grid[cy][cx] == '~':
                            self.grid[cy][cx] = '•'

    def all_ships_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)


def clear_screen():
    """Очистка консоли, чтобы игроки не видели поля друг друга."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" * 30)  # Доп. отступ на случай запуска в IDE (PyCharm / VS Code)


def setup_player_board(player_name):
    """Этап расстановки кораблей для одного игрока."""
    board = Board()
    # 1 четырёхпалубный, 2 трёхпалубных, 3 двухпалубных, 4 однопалубных
    fleet = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]

    clear_screen()
    print(f"=== {player_name}: Расстановка кораблей ===")
    mode = input("Выберите режим расстановки (1 - Вручную, 2 - Автоматически): ").strip()

    if mode == '2':
        board.auto_place_ships(fleet)
        board.display(hide_ships=False)
        input("\nКорабли расставлены! Нажмите Enter, чтобы продолжить...")
        return board

    for size in fleet:
        while True:
            clear_screen()
            print(f"=== {player_name}: Расстановка кораблей ===")
            board.display(hide_ships=False)
            print(f"\nСтавим корабль размером в {size} палуб(ы).")

            try:
                coords_input = input("Введите координаты (X и Y через пробел, от 1 до 10): ").split()
                if len(coords_input) != 2:
                    print("Ошибка: нужно ввести два числа через пробел!")
                    input("Нажмите Enter...")
                    continue

                x, y = int(coords_input[0]) - 1, int(coords_input[1]) - 1

                if size > 1:
                    direction = input("Направление (Г - горизонтально, В - вертикально): ").strip().upper()
                    # Поддержка латинской раскладки на случай опечатки
                    if direction == 'G' or direction == 'H': direction = 'Г'
                    if direction == 'V': direction = 'В'
                    if direction not in ('Г', 'В'):
                        print("Ошибка: введите 'Г' или 'В'!")
                        input("Нажмите Enter...")
                        continue
                else:
                    direction = 'Г'

                if board.place_ship(size, x, y, direction):
                    break
                else:
                    print("Ошибка: здесь нельзя поставить корабль (выход за границы или касание другого корабля)!")
                    input("Нажмите Enter...")
            except ValueError:
                print("Ошибка: вводите только целые числа!")
                input("Нажмите Enter...")

    clear_screen()
    print(f"=== {player_name}: Все корабли расставлены! ===")
    board.display(hide_ships=False)
    input("\nНажмите Enter, чтобы передать ход...")
    return board


def play_game():
    print("Добро пожаловать в консольный «Морской Бой»!")
    input("Нажмите Enter, чтобы начать игру...")

    board1 = setup_player_board("Игрок 1")
    board2 = setup_player_board("Игрок 2")

    current_player = 1

    while True:
        clear_screen()
        if current_player == 1:
            player_name = "Игрок 1"
            my_board, enemy_board = board1, board2
        else:
            player_name = "Игрок 2"
            my_board, enemy_board = board2, board1

        input(f"Ходит {player_name}. Нажмите Enter, когда будете готовы...")

        while True:
            clear_screen()
            print(f"=== Ход: {player_name} ===")
            print("\nВаше поле:")
            my_board.display(hide_ships=False)
            print("\nПоле противника:")
            enemy_board.display(hide_ships=True)

            try:
                shot_input = input("\nВведите координаты выстрела (X по горизонтали, Y по вертикали через пробел): ").split()
                if len(shot_input) != 2:
                    print("Введите ровно две координаты от 1 до 10 через пробел!")
                    input("Нажмите Enter...")
                    continue

                x, y = int(shot_input[0]) - 1, int(shot_input[1]) - 1
                if not (0 <= x < 10 and 0 <= y < 10):
                    print("Координаты должны быть в диапазоне от 1 до 10!")
                    input("Нажмите Enter...")
                    continue

                result = enemy_board.receive_shot(x, y)

                if result == 'repeat':
                    print("Вы уже стреляли в эту клетку! Попробуйте другие координаты.")
                    input("Нажмите Enter...")
                elif result == 'miss':
                    print("\nМимо! Ход переходит к следующему игроку.")
                    input("Нажмите Enter для передачи хода...")
                    current_player = 2 if current_player == 1 else 1
                    break
                elif result == 'injured':
                    print("\nПопадание! Корабль противника ранен. Вы стреляете ещё раз!")
                    input("Нажмите Enter для следующего выстрела...")
                elif result == 'killed':
                    print("\nУбил! Вражеский корабль полностью уничтожен!")
                    if enemy_board.all_ships_sunk():
                        clear_screen()
                        print("==========================================")
                        print(f" ПОЗДРАВЛЯЕМ! {player_name} ПОБЕДИЛ В ИГРЕ!")
                        print(" Вся вражеская флотилия уничтожена!")
                        print("==========================================")
                        return
                    print("Вы получаете право на дополнительный ход!")
                    input("Нажмите Enter для следующего выстрела...")

            except ValueError:
                print("Ошибка ввода! Введите два числа через пробел.")
                input("Нажмите Enter...")


if __name__ == "__main__":
    play_game()
