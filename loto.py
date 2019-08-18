#!/usr/bin/python3

"""
== Лото ==

Правила игры в лото.

Игра ведется с помощью специальных карточек, на которых отмечены числа, 
и фишек (бочонков) с цифрами.

Количество бочонков — 90 штук (с цифрами от 1 до 90).

Каждая карточка содержит 3 строки по 9 клеток. В каждой строке по 5 случайных цифр, 
расположенных по возрастанию. Все цифры в карточке уникальны. Пример карточки:

--------------------------
    9 43 62          74 90
 2    27    75 78    82
   41 56 63     76      86 
--------------------------

В игре 2 игрока: пользователь и компьютер. Каждому в начале выдается 
случайная карточка. 

Каждый ход выбирается один случайный бочонок и выводится на экран.
Также выводятся карточка игрока и карточка компьютера.

Пользователю предлагается зачеркнуть цифру на карточке или продолжить.
Если игрок выбрал "зачеркнуть":
	Если цифра есть на карточке - она зачеркивается и игра продолжается.
	Если цифры на карточке нет - игрок проигрывает и игра завершается.
Если игрок выбрал "продолжить":
	Если цифра есть на карточке - игрок проигрывает и игра завершается.
	Если цифры на карточке нет - игра продолжается.
	
Побеждает тот, кто первый закроет все числа на своей карточке.

Пример одного хода:

Новый бочонок: 70 (осталось 76)
------ Ваша карточка -----
 6  7          49    57 58
   14 26     -    78    85
23 33    38    48    71   
--------------------------
-- Карточка компьютера ---
 7 11     - 14    87      
      16 49    55 77    88    
   15 20     -       76  -
--------------------------
Зачеркнуть цифру? (y/n)

Подсказка: каждый следующий случайный бочонок из мешка удобно получать 
с помощью функции-генератора.

Подсказка: для работы с псевдослучайными числами удобно использовать 
модуль random: http://docs.python.org/3/library/random.html

"""

import os
import random


class Card():
    def __init__(self, player):
        self.player = player
        self.numbers = RandomNumbers()
        self.line1 = self.numbers.fill_line()
        self.line2 = self.numbers.fill_line()
        self.line3 = self.numbers.fill_line()
        self.whole_card = [self.line1, self.line2, self.line3]
        self.remains = 15

    def __sub__(self, other):
        for line in self.whole_card:
            if other in line:
                i = self.whole_card.index(line)
                j = line.index(other)
                self.whole_card[i][j] = '--'
                self.remains -= 1
                return True
        return False

    def __str__(self):
        print_line = '-------- {} Card ---------\n'.format(self.player)
        for line in self.whole_card:
            for elem in line:
                if str(elem).isdigit() and len(str(elem)) is 1:
                    print_line += '{}{}{}'.format(' ', str(elem), ' ')
                else:
                    print_line += '{}{}'.format(str(elem), ' ')
            print_line += '\n'
        print_line += '--------------------------'
        return print_line

    def __len__(self):
        return self.remains

    def check(self, number):
        for line in self.whole_card:
            if number in line:
                return True
        return False


class RandomNumbers(list):
    def __init__(self):
        self._numbers = [i for i in range(1, 91)]
        random.shuffle(self._numbers)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self._numbers) > 0:
            return self._numbers.pop()
        else:
            raise StopIteration

    def __repr__(self):
        return super(list, self._numbers).__str__()

    def __len__(self):
        return len(self._numbers)

    def fill_line(self):  # Функция для создания строки карточки.
        x = [next(self) for i in range(5)]
        x.sort(key=lambda z: z, reverse=True)
        y = ['  '] * 5
        seq = [1, 1, 1, 1, 1, 2, 2, 2, 2]
        random.shuffle(seq)
        req = []

        for i in seq:
            if i == 1:
                req.append(x.pop())
            else:
                req.append(y.pop())

        return req


def main():

    def new_screen(end='no'):
        os.system("cls")
        # os.system("clear")    #Clear screen in Linux
        global x
        print()
        print("======= 'Loto' game =======")
        print()
        if end == 'no':
            x = int(next(bag))
            print('Новый бочонок: {} (осталось {})'.format(x, len(bag)))
        elif end == 'yes':
            print('Игра кончена. Осталось {} бочонков.'.format(len(bag)))
        print(my_card)
        print()
        print(pc_card)


    def choice():
        answers = ['y', 'n', 'q', 'iddqd']
        answer = ''
        while answer not in answers:
            answer = input('Зачеркнуть цифру? (y/n/q) ').lower()
            if answer == 'y':
                if my_card - x is False:
                    new_screen(end='yes')
                    print('You lose! Game Over')
                    return False
                if len(my_card) == 0:
                    new_screen(end='yes')
                    print('You win!')
                    return False
            elif answer == 'n':
                if my_card.check(x) is True:
                    new_screen(end='yes')
                    print('You lose! Game Over')
                    return False
            elif answer == 'q':
                new_screen(end='yes')
                print('Игрок {} вышел из игры. Побеждает игрок {}.'.format(my_card.player, pc_card.player))
                return False
            elif answer == 'iddqd':
                for i in my_card.whole_card:
                    for j in i:
                        if type(j) is int:
                            my_card - j
                new_screen(end='yes')
                print("You win, but hey, you're a CHEATER!!!")
                return False
            else:
                print('Я Вас не понял, повторите еще раз.')


    my_card = Card('My')
    pc_card = Card('PC')

    bag = RandomNumbers()

    while len(bag) > 0:
        new_screen()
        result = choice()
        if result == False:
            break
        if pc_card.check(x) is True:
            pc_card - x
            if len(pc_card) == 0:
                new_screen(end='yes')
                print('PC win! You lose! Game Over')
                break
    if len(bag) == 0:
        print("No more barrels in the bag. It's a draw!")


if __name__ == '__main__':
    main()


input("Press Enter")