import time, sys, pygame
import random
import copy

size = width, height = 600, 400
screen = pygame.display.set_mode(size)
numb_count = 20 
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
        elif state == 2:
            self.sur.fill((0,0,255))
        elif state == 3:
            self.sur.fill((255,0,0))
        else:
            self.sur.fill((50,50,50))
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


def merge_sort(nlist, templist, start, merge_size, left, right):

    # both left and right exhausted
    if left >= start+merge_size and right >= start+2*merge_size:
        for i in range(len(templist)):
            nlist[start+i] = copy.copy(templist[i])
        templist.clear()
        start = start + 2*merge_size
        if start > len(nlist):
            start = 0
            merge_size *= 2
        return start, merge_size, left, right

    # one side is exhausted
    if left >= start+merge_size or right >= start+2*merge_size:
        if left >= start+merge_size:
            templist.append(copy.copy(nlist[right]))
            right += 1
        elif right >= start+2*merge_size:
            templist.append(copy.copy(nlist[left]))
            left += 1
        return start, merge_size, left, right

    # both sides haven't exhausted
    if nlist[left].val > nlist[right].val:
        templist.append(copy.copy(nlist[left]))
        left += 1
    elif nlist[left].val <= nlist[right].val:
        templist.append(copy.copy(nlist[right]))
        right += 1
    return start, merge_size, left, right


def draw_list():
    screen.fill((0,0,0))
    for n in numbers:
        n.draw()
    pygame.display.flip()
    time.sleep(1)

def draw_templist(templist):
    for n in templist:
        n.draw()

if __name__ == '__main__':
    pygame.init()


    game_setup()
    templist = list()
    start, merge_size, left, right = 0, 1, 0, 1

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        for i, n in enumerate(numbers):
            n.set_state(4) # inactive

        print(start, left, right, [n.seq for n in templist])
        start, merge_size, left, right = merge_sort(numbers, templist, start, merge_size, left, right)

        draw_templist(templist)
        draw_list()
