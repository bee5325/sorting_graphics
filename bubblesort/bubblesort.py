import time, sys, pygame
import random

size = width, height = 600, 400
screen = pygame.display.set_mode(size)
numb_count = 200
rect_width = width // numb_count


class Number:

    def __init__(self, val, seq):
        self.val = int(val)
        self.sur = pygame.Surface((rect_width, int(val)))
        self.sur.fill((255,255,255))
        self.seq = seq
        self.pos = (self.seq*rect_width, height-self.sur.get_height())

    def set_val(self, val):
        self.val = int(val)
        self.sur = pygame.Surface((rect_width, int(val)))
        self.sur.fill((255,255,255))

    def set_state(self, state):
        if state == 0:
            self.sur.fill((255,255,255))
        elif state == 1:
            self.sur.fill((0,255,0))
        self.draw()

    def set_seq(self, seq):
        self.seq = seq
        self.pos = (self.seq*rect_width, height-self.sur.get_height())

    def draw(self):
        screen.blit(self.sur, self.pos)


numbers = [Number(random.random()*height, i) for i in range(numb_count)]


def swap(nlist, n1, n2):
    temp = nlist[n1]
    nlist[n1] = nlist[n2]
    nlist[n2] = temp
    nlist[n1].set_seq(n1)
    nlist[n2].set_seq(n2)


def game_setup():
    screen.fill((0,0,0))
    draw_list()


def bubble_sort(i, end_ind):

    if i == end_ind:
        return 0, end_ind-1

    if numbers[i].val > numbers[i+1].val:
        swap(numbers, i, i+1)

    return i+1, end_ind


def draw_list():
    screen.fill((0,0,0))
    for n in numbers:
        n.draw()
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()


    game_setup()
    i = 0
    end_ind = len(numbers)-1

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        for n in numbers:
            n.set_state(0)
        if end_ind != 0:
            numbers[i].set_state(1)
            i, end_ind = bubble_sort(i, end_ind)
        draw_list()
