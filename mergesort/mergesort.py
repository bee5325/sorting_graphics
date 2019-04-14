import time, sys, pygame
import random
import copy

size = width, height = 600, 400
screen = pygame.display.set_mode(size)
numb_count = 600 
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
        self.pos = (self.seq*rect_width, height-self.sur.get_height())
        self.sur.fill((255,255,255))

    def set_state(self, state):
        self.sur.set_alpha(255)
        if state == 0: # checking
            self.sur.fill((255,255,255))
        elif state == 1: # temporary placeholder
            self.sur.fill((0,255,0))
            self.sur.set_alpha(125)
        elif state == 2: # left and right
            self.sur.fill((0,0,255))
        elif state == 3: # chosen
            self.sur.fill((255,0,0))
        else: # inactive
            self.sur.fill((80,80,80))
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

    curr_idx = start + len(templist)
    left_done = (left >= start+merge_size or left >= len(nlist))
    right_done = (right >= start+2*merge_size or right >= len(nlist))
    
    # both left and right exhausted
    if left_done and right_done:
        for i in range(len(templist)):
            nlist[start+i] = copy.copy(templist[i])
        templist.clear()
        start = start + 2*merge_size
        left = start
        right = start + merge_size
        if left >= len(nlist) or right >= len(nlist):
            start = 0
            merge_size *= 2
            left = start
            right = start + merge_size
        if merge_size >= len(nlist):
            return -1, -1, -1, -1, -1 
        return start, merge_size, left, right, -1

    # one side is exhausted
    if left_done or right_done:
        if left_done:
            templist.append(Number(nlist[right].val, curr_idx))
            chosen = right
            right += 1
        elif right_done:
            templist.append(Number(nlist[left].val, curr_idx))
            chosen = left 
            left += 1
        return start, merge_size, left, right, chosen

    # both sides haven't exhausted
    if nlist[left].val > nlist[right].val:
        templist.append(Number(nlist[right].val, curr_idx))
        chosen = right 
        right += 1
    else:
        templist.append(Number(nlist[left].val, curr_idx))
        chosen = left
        left += 1
    return start, merge_size, left, right, chosen


def draw_list():
    screen.fill((0,0,0))
    for n in numbers:
        n.draw()

def draw_templist(templist):
    for n in templist:
        n.set_state(1)
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

        if start != -1:
            left_done = (left >= start+merge_size or left >= len(numbers))
            right_done = (right >= start+2*merge_size or right >= len(numbers))
            for i, n in enumerate(numbers):
                if i == left or i == right:
                    if i == left and not left_done:
                        n.set_state(2)
                    if i == right and not right_done:
                        n.set_state(2)
                elif i >= start and i < start+2*merge_size:
                    n.set_state(0)
                else:
                    n.set_state(4) # inactive

            start, merge_size, left, right, chosen = merge_sort(numbers, templist, start, merge_size, left, right)

            if chosen != -1:
                numbers[chosen].set_state(3)
        else:
            for n in numbers:
                n.set_state(0)

        draw_list()
        draw_templist(templist)
        pygame.display.flip()
