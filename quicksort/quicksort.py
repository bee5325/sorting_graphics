import time, sys, pygame
import random

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


def quick_sort(nlist, partitions, check_idx, swap_idx, pivot):

    start, end = partitions[0]

    # if nothing to check
    if end-start < 1:
        partitions.pop(0)
        # for the case when sorting is done
        if len(partitions) == 0:
            return None, None, -1
        next_start, next_end = partitions[0]
        return next_end, next_start, -1

    # randomly take 11 values, use the median one as pivot
    if pivot == -1:
        randoms = [random.randrange(start, end) for _ in range(11)]
        randoms.sort(key=lambda x: nlist[x].val)
        median = randoms[5]
        if pivot != start:
            swap(nlist, median, start)
        pivot = start

    # if all items checked for this partition
    if pivot == check_idx:
        swap(nlist, pivot, swap_idx)
        left = (start, swap_idx-1)
        right = (swap_idx+1, end)
        partitions.append(left)
        partitions.append(right)
        partitions.pop(0)
        # for the case when sorting is done
        if len(partitions) == 0:
            return None, None
        next_start, next_end = partitions[0]
        return next_end, next_start, -1

    # swap_index have to be inititalize the first time encountering smaller value
    if nlist[check_idx].val < nlist[pivot].val and swap_idx == start:
        swap_idx = check_idx
    # swap larger value to the swap_index item (only if smaller value is encountered before)
    elif nlist[check_idx].val >= nlist[pivot].val and swap_idx != start:
        swap(nlist, check_idx, swap_idx)
        swap_idx -= 1
    check_idx -= 1

    return check_idx, swap_idx, pivot


def draw_list():
    screen.fill((0,0,0))
    for n in numbers:
        n.draw()
    pygame.display.flip()

if __name__ == '__main__':
    pygame.init()


    game_setup()
    partitions = [(0, len(numbers)-1)]
    start, end = partitions[0]
    check_idx, swap_idx, pivot = end, start, -1

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if len(partitions) != 0:
            start, end = partitions[0]
            for i, n in enumerate(numbers):
                if i >= start and i <= end:
                    n.set_state(0)
                else:
                    n.set_state(4) # inactive
            if start < len(numbers):
                numbers[start].set_state(1)
                numbers[check_idx].set_state(2)
            if swap_idx != start:
                numbers[swap_idx].set_state(3)
        else:
            for n in numbers:
                n.set_state(0)

        if check_idx is not None and swap_idx is not None:
            check_idx, swap_idx, pivot = quick_sort(numbers, partitions, check_idx, swap_idx, pivot)

        draw_list()
