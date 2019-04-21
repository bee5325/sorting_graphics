import time, sys, pygame
import random
import copy
import sequence

S_SIZE = S_WID, S_HGT = 1080, 400
screen = pygame.display.set_mode(S_SIZE)
NUMB_COUNT = 1080 

nlist = [random.random()*S_HGT for _ in range(NUMB_COUNT)]
num = sequence.NumGroup(nlist, S_WID, S_HGT)


class TempNumGroup(sequence.NumGroup):

    def __init__(self, base_num_group):
        nlist = [0 for _ in range(base_num_group.length)]
        screen_w = base_num_group.screen_w
        screen_h = base_num_group.screen_h
        super().__init__(nlist, screen_w, screen_h)

        for n in self.nlist:
            n.set_color((255,0,0))
            n.set_alpha(125)
        self.curr_idx = 0

    def append(self, num):
        self[self.curr_idx].set_val(num.val)
        self.curr_idx += 1

    def clear(self):
        for i in range(self.curr_idx):
            self[i].set_val(0)
        self.curr_idx = 0

    def set_start_pos(self, idx):
        self.bottomleft = (idx*self.sprite_w, self.screen_h)

    def __iter__(self):
        return iter(self.nlist[:self.curr_idx])


def draw_all():
    screen.fill(0)
    num.update()
    num.draw(screen)
    templist.update()
    templist.draw(screen)
    pygame.display.flip()


def merge_sort(nlist, templist, start, merge_size, left, right):

    left_done = (left >= start+merge_size or left >= len(nlist))
    right_done = (right >= start+2*merge_size or right >= len(nlist))
    
    # both left and right exhausted
    if left_done and right_done:
        for i, t in enumerate(templist):
            nlist[start+i].set_val(t.val)
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
            templist.append(nlist[right])
            chosen = right
            right += 1
        elif right_done:
            templist.append(nlist[left])
            chosen = left 
            left += 1
        return start, merge_size, left, right, chosen

    # both sides haven't exhausted
    if nlist[left].val > nlist[right].val:
        templist.append(nlist[right])
        chosen = right 
        right += 1
    else:
        templist.append(nlist[left])
        chosen = left
        left += 1
    return start, merge_size, left, right, chosen



if __name__ == '__main__':
    pygame.init()

    templist = TempNumGroup(num)

    start, merge_size, left, right = 0, 1, 0, 1

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # if not finish
        if start != -1:

            # display part 1
            templist.set_start_pos(start)
            left_done = (left >= start+merge_size or left >= len(num))
            right_done = (right >= start+2*merge_size or right >= len(num))
            for i, n in enumerate(num):
                if i == left and not left_done:
                    n.set_color((0,0,255))
                elif i == right and not right_done:
                    n.set_color((0,0,255))
                elif i >= start and i < start+2*merge_size:
                    n.set_color((255,255,255))
                else:
                    n.set_color((100,100,100)) # inactive

            # merge logic
            start, merge_size, left, right, chosen = merge_sort(num, templist, start, merge_size, left, right)

            # display part 2
            if chosen != -1:
                num[chosen].set_color((0,255,0))
        else:
            for n in num:
                n.set_color((255,255,255))

        draw_all()

