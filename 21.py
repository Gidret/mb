phonebook = {}

while True:
    print("\n--- Телефонная книга ---")
    print("1. Добавить контакт")
    print("2. Найти контакт")
    print("3. Удалить контакт")
    print("4. Показать все контакты")
    print("5. Выход")

    choice = input("Выберите действие (1-5): ")

    if choice == "1":
        name = input("Введите имя: ")
        phone = input("Введите номер телефона: ")
        phonebook[name] = phone
        print(f"Контакт '{name}' сохранен.")

    elif choice == "2":
        name = input("Введите имя для поиска: ")
        if name in phonebook:
            print(f"Номер {name}: {phonebook[name]}")
        else:
            print("Контакт не найден.")

    elif choice == "3":
        name = input("Введите имя для удаления: ")
        if name in phonebook:
            del phonebook[name]
            print(f"Контакт '{name}' удален.")
        else:
            print("Контакт не найден.")

    elif choice == "4":
        if phonebook:
            print("\nСписок всех контактов:")
            for name, phone in phonebook.items():
                print(f"- {name}: {phone}")
        else:
            print("Телефонная книга пуста.")

    elif choice == "5":
        print("Выход из программы.")
        break

    else:
        print("Неверный ввод, выберите пункт от 1 до 5.")


# Ввод количества элементов и заполнение кортежа
n = int(input("Введите количество чисел в кортеже: "))
numbers = tuple(int(input(f"Введите число {i + 1}: ")) for i in range(n))

print("\nВаш кортеж:", numbers)

if len(numbers) > 0:
    # 1) Вывод элементов и среза
    print("Первый элемент:", numbers[0])
    print("Последний элемент:", numbers[-1])
    # Индексы в Python начинаются с 0: 2-й элемент имеет индекс 1, 3-й — индекс 2.
    # Верхняя граница среза не включается, поэтому указываем [1:3].
    print("Срез со второго по третий элемент:", numbers[1:3])

    # 2) Подсчет вхождений и поиск первого индекса
    target = int(input("\nВведите число для поиска: "))
    count = numbers.count(target)
    print(f"Количество вхождений числа {target}: {count}")

    if count > 0:
        print(f"Индекс первого вхождения: {numbers.index(target)}")
    else:
        print("Такого числа нет в кортеже.")
else:
    print("Кортеж пуст.")


import os
import random

# Создает пустое игровое поле 10 на 10, заполненное туманом войны '~'
def create_board():
    board = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append('~')  # Добавляем пустую клетку в строку
        board.append(row)   # Добавляем готовую строку в игровое поле
    return board

# Выводит игровое поле в консоль
# Параметр hide_ships=True позволяет спрятать живые корабли (чтобы соперник их не видел)
def display_board(board, hide_ships=False):
    print("   1 2 3 4 5 6 7 8 9 10") # Верхняя рамка с номерами колонок
    for y in range(10):
        row_display = []
        for x in range(10):
            cell = board[y][x]
            # Если включен режим маскировки и в клетке живой корабль -> заменяем на туман
            if hide_ships and cell == '■':
                row_display.append('~')
            else:
                row_display.append(cell)
        
        # Выравниваем числа: перед однозначными (1-9) ставим 2 пробела, перед "10" — один пробел
        if y + 1 < 10:
            space = "  "
        else:
            space = " "
        print(f"{y + 1}{space}" + " ".join(row_display))

# Проверяет, можно ли поставить корабль в эти координаты с учетом границ и зазоров в 1 клетку
def can_place_ship(board, x, y, size, direction):
    # Пробегаемся по каждой палубе будущего корабля
    for i in range(size):
        if direction == 'Г':   # Если горизонтальный — сдвигаем X координату
            nx = x + i
            ny = y
        else:                  # Если вертикальный — сдвигаем Y координату
            nx = x
            ny = y + i

        # Проверка 1: не вылетел ли корабль за границы поля (от 0 до 9)?
        if not (0 <= nx < 10 and 0 <= ny < 10):
            return False

        # Проверка 2: проверяем саму клетку палубы и все 8 клеток вокруг нее (квадрат 3х3)
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                cx = nx + dx
                cy = ny + dy
                # Если соседняя клетка существует на поле и там уже стоит корабль '■'
                if 0 <= cx < 10 and 0 <= cy < 10:
                    if board[cy][cx] == '■':
                        return False # Ставить нельзя, нарушено правило соседства
    return True # Если все проверки прошли — ставить можно

# Пытается поставить корабль на поле
def place_ship(board, x, y, size, direction):
    # Сначала проверяем, разрешено ли ставить
    if not can_place_ship(board, x, y, size, direction):
        return False # Если нельзя, возвращаем False
    
    # Если можно, фактически меняем символы на поле на '■'
    for i in range(size):
        if direction == 'Г':
            board[y][x + i] = '■'
        else:
            board[y + i][x] = '■'
    return True # Корабль успешно выставлен

# Автоматически расставляет флот случайным образом
def auto_place_ships(board, fleet):
    for size in fleet:
        placed = False
        while not placed:
            x = random.randint(0, 9)       # Случайный X от 0 до 9
            y = random.randint(0, 9)       # Случайный Y от 0 до 9
            direction = random.choice(['Г', 'В']) # Случайное направление
            placed = place_ship(board, x, y, size, direction) # Пытаемся поставить

# Функция «сканирует» поле вокруг подбитой палубы, чтобы понять, утонул ли корабль полностью
def check_if_ship_sunk(board, start_x, start_y):
    ship_cells = [] # Сюда соберем координаты всего корабля целиком
    
    # Шагаем влево от места попадания, пока натыкаемся на палубы (раненые или живые)
    x = start_x
    while x >= 0 and board[start_y][x] in ('X', '■'):
        ship_cells.append((x, start_y))
        x -= 1
    # Шагаем вправо
    x = start_x + 1
    while x < 10 and board[start_y][x] in ('X', '■'):
        ship_cells.append((x, start_y))
        x += 1
        
    # Шагаем вверх
    y = start_y
    while y >= 0 and board[y][start_x] in ('X', '■'):
        ship_cells.append((start_x, y))
        y -= 1
    # Шагаем вниз
    y = start_y + 1
    while y < 10 and board[y][start_x] in ('X', '■'):
        ship_cells.append((start_x, y))
        y += 1

    # Убираем дубликаты координат с помощью множества и превращаем обратно в список
    ship_cells = list(set(ship_cells))

    # Если среди найденных клеток корабля осталась хотя бы одна живая '■', корабль еще жив
    for sx, sy in ship_cells:
        if board[sy][sx] == '■':
            return False, [] # Корабль ранен, но не убит
            
    return True, ship_cells # Корабль полностью уничтожен!

# Автоматически обводит уничтоженный корабль точками '*', так как там точно нет других кораблей
def mark_surrounding(board, ship_cells):
    for sx, sy in ship_cells:
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                cx = sx + dx
                cy = sy + dy
                # Если соседняя клетка — это пустая вода '~', ставим туда '*' (промах/занято)
                if 0 <= cx < 10 and 0 <= cy < 10:
                    if board[cy][cx] == '~':
                        board[cy][cx] = '*'

# Принимает выстрел игрока и обрабатывает его результат
def receive_shot(board, x, y):
    cell = board[y][x]
    if cell == 'X' or cell == '*':
        return 'repeat' # Игрок выстрелил туда, куда уже стрелял ранее
    elif cell == '~':
        board[y][x] = '*' # Ставим промах
        return 'miss'
    elif cell == '■':
        board[y][x] = 'X' # Ставим попадание (ранен)
        # Сразу проверяем, не был ли это последний вздох корабля
        is_sunk, ship_cells = check_if_ship_sunk(board, x, y)
        if is_sunk:
            mark_surrounding(board, ship_cells) # Обводим точками
            return 'killed' # Корабль убит
        return 'injured' # Корабль просто ранен

# Проверяет, остались ли на поле вообще живые палубы
def all_ships_sunk(board):
    for y in range(10):
        for x in range(10):
            if board[y][x] == '■':
                return False # Нашли хоть одну живую палубу — игра продолжается
    return True # Живых кораблей нет — поражение

# Очищает экран консоли, перенося текст, чтобы игроки не подглядывали друг за другом
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("" * 30)

# Организует этап расстановки флота для конкретного игрока
def setup_player_board(player_name):
    board = create_board()
    fleet = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] # Наш стандартный набор кораблей

    clear_screen()
    print(f"=== {player_name}: Расстановка кораблей ===")
    mode = input("Выберите режим расстановки (1 - Вручную, 2 - Автоматически): ").strip()

    if mode == '2':
        auto_place_ships(board, fleet)
        display_board(board, hide_ships=False)
        input("Корабли расставлены! Передайте управление другу и НАЖМИТЕ ENTER...")
        clear_screen()
        return board

    # Ручная расстановка
    for size in fleet:
        while True:
            clear_screen()
            print(f"=== {player_name}: Расстановка кораблей ===")
            display_board(board, hide_ships=False)
            print(f"Ставим корабль размером в {size} палуб(ы).")

            try:
                coords_input = input("Введите координаты (X и Y через пробел, от 1 до 10): ").split()
                if len(coords_input) != 2:
                    print("Ошибка: нужно ввести два числа через пробел!")
                    input("Нажмите Enter...")
                    continue

                # Вычитаем 1, так как пользователи вводят от 1 до 10, а индексы в Python от 0 до 9
                x = int(coords_input[0]) - 1
                y = int(coords_input[1]) - 1

                # Направление нужно запрашивать только для кораблей длиннее 1 клетки
                if size > 1:
                    direction = input("Направление (Г - горизонтально, В - вертикально): ").strip().upper()
                    if direction in ('G', 'H'): direction = 'Г'
                    if direction == 'V': direction = 'В'
                    if direction not in ('Г', 'В'):
                        print("Ошибка: введите 'Г' или 'В'!")
                        input("Нажмите Enter...")
                        continue
                else:
                    direction = 'Г' # Для одиночной клетки направление не важно

                # Пытаемся поставить корабль
                if place_ship(board, x, y, size, direction):
                    break # Успех! Переходим к следующему кораблю
                else:
                    print("Ошибка: сюда нельзя поставить корабль!")
                    input("Нажмите Enter...")
            except ValueError:
                print("Ошибка: вводите только целые числа!")
                input("Нажмите Enter...")

    clear_screen()
    print(f"=== {player_name}: Все корабли расставлены! ===")
    display_board(board, hide_ships=False)
    input("Передайте управление другу и НАЖМИТЕ ENTER, чтобы очистить экран...")
    clear_screen()
    return board

# Главная функция управления игрой
def play_game():
    print("Добро пожаловать в консольный «Морской Бой»!")
    input("Нажмите Enter, чтобы начать игру...")

    # Создаем и заполняем поля для обоих игроков
    board1 = setup_player_board("Игрок 1")
    board2 = setup_player_board("Игрок 2")

    current_player = 1 # Начинает первый игрок

    while True:
        clear_screen()
        # Определяем, кто стреляет, а кто защищается на текущем ходу
        if current_player == 1:
            player_name = "Игрок 1"
            my_board = board1
            enemy_board = board2
        else:
            player_name = "Игрок 2"
            my_board = board2
            enemy_board = board1

        input(f"Ходит {player_name}. Убедитесь, что соперник не смотрит, и нажмите Enter...")

        # Внутренний цикл хода (пока игрок попадает, он продолжает стрелять)
        while True:
            clear_screen()
            print(f"=== Ход: {player_name} ===")
        
            print("Ваше поле (видны только попадания по вам):")
            display_board(my_board, hide_ships=True) 
            
            print("Поле противника:")
            display_board(enemy_board, hide_ships=True)

            try:
                shot_input = input("Введите координаты выстрела (X и Y через пробел): ").split()
                if len(shot_input) != 2:
                    print("Введите ровно две координаты от 1 до 10 через пробел!")
                    input("Нажмите Enter...")
                    continue

                x = int(shot_input[0]) - 1
                y = int(shot_input[1]) - 1
                
                if not (0 <= x < 10 and 0 <= y < 10):
                    print("Координаты должны быть в диапазоне от 1 до 10!")
                    input("Нажмите Enter...")
                    continue

                # Передаем выстрел на доску врага
                result = receive_shot(enemy_board, x, y)

                if result == 'repeat':
                    print("Вы уже стреляли в эту клетку! Попробуйте снова.")
                    input("Нажмите Enter...")
                elif result == 'miss':
                    print("Мимо! Ход переходит к следующему игроку.")
                    input("Нажмите Enter для передачи хода...")
                    # Меняем игрока: если был 1, станет 2, и наоборот
                    current_player = 2 if current_player == 1 else 1
                    break # Прерываем цикл текущего хода, ход передан
                elif result == 'injured':
                    print("Ранен! Вы получаете дополнительный ход.")
                    input("Нажмите Enter...")
                elif result == 'killed':
                    print("Убит! Корабль полностью потоплен. Вы получаете дополнительный ход.")
                    # Проверяем, не выиграл ли игрок этим убийством
                    if all_ships_sunk(enemy_board):
                        clear_screen()
                        print(f"Победа! {player_name} полностью уничтожил флот противника!")
                        return # Выход из игры
                    input("Нажмите Enter...")
            except ValueError:
                print("Ошибка: вводите только целые числа!")
                input("Нажмите Enter...")

# Точка входа: запускает игру, только если файл запущен напрямую, а не импортирован
if __name__ == "__main__":
    play_game()
