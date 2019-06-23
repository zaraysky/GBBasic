import random


def random_generator(start, stop, count):
    lst = list(range(start, stop))
    i = 0
    while i < count:
        yield lst.pop(random.randrange(len(lst)))
        i += 1


class Card:
    def __init__(self, name):
        self.name = name
        self.numbers = []
        self.closed = [False] * 15
        self.numbers = [ x for x in random_generator(1, 91, 15)]

    def __str__(self):
        s = dict()
        s[0] = f' {self.name} '.center(35, '-')
        s[1] = ''
        s[2] = ''
        s[3] = ''
        cntr = 0
        for i in range(1, 91):
            if i in self.numbers:
                c = str(i) if not self.closed[self.numbers.index(i)] else 'XX'
                s[cntr % 3 + 1] = s[cntr % 3 + 1] + f'|  {c:2}  '
                cntr += 1
            # else:
            #     s[i % 3 + 1] = s[i % 3 + 1] + ' '
        s[1] += '|'
        s[2] += '|'
        s[3] += '|'

        s[4] = '-' * 34
        return '\n'.join([v for v in s.values()])

    def is_number_on_card(self, n):
        return n in self.numbers

    def close_number(self, n):
        if n in self.numbers:
            self.closed[self.numbers.index(n)] = True

    def is_card_closed(self):
        return all(self.closed)


player = Card('Ваша карточка')
computer = Card('Карточка компьютера')
n = list(range(1, 91))

while not (player.is_card_closed() or computer.is_card_closed()):
    i = n.pop(random.randrange(len(n)))
    print('Новый бочонок: {} (осталось {})'.format(i, len(n)))
    print(player)
    print(computer)
    answer = input('Зачеркнуть цифру? (y/n)')
    if answer == 'y':
        if player.is_number_on_card(i):
            player.close_number(i)
        else:
            print('Вы проиграли')
            break
    else:  # считаем, что ответил нет при любом вариантре кроме 'y'
        if player.is_number_on_card(i):
            print('Вы проиграли')
            break

    computer.close_number(i)

print('Вы {}'.format('выиграли' if player.is_card_closed() else 'проиграли'))