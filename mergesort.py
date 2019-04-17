import time, sys, pygame
import random
import copy
import sequence

S_SIZE = S_WID, S_HGT = 600, 400
screen = pygame.display.set_mode(S_SIZE)
NUMB_COUNT = 200 

nlist = [random.random()*S_HGT for _ in range(NUMB_COUNT)]
num = sequence.NumGroup(nlist, S_WID, S_HGT)


def draw_all():
    screen.fill((0,0,0))
    num.draw(screen)
    pygame.display.flip()


def draw_templist(templist):
    for n in templist:
        n.set_state(1)
        n.draw()


# TODO: Think of ways to implement templist for the new data structure
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
            templist[right] = nlist[right].val)
            chosen = right
            right += 1
        elif right_done:
            templist.append(nlist[left].val)
            chosen = left 
            left += 1
        return start, merge_size, left, right, chosen

    # both sides haven't exhausted
    if nlist[left].val > nlist[right].val:
        templist.append(nlist[right].val)
        chosen = right 
        right += 1
    else:
        templist.append(nlist[left].val)
        chosen = left
        left += 1
    return start, merge_size, left, right, chosen



if __name__ == '__main__':
    pygame.init()

    templist = sequence.NumGroup([0 for _ in range(NUMB_COUNT), S_WID, S_HGT)

    start, merge_size, left, right = 0, 1, 0, 1

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # if not finish
        if start != -1:

            # display part 1
            left_done = (left >= start+merge_size or left >= len(num))
            right_done = (right >= start+2*merge_size or right >= len(num))
            for i, n in enumerate(num):
                if i == left or i == right:
                    if i == left and not left_done:
                        n.set_color((0,0,255))
                    if i == right and not right_done:
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

        num.update()
        num.draw(screen)
        templist.draw(screen)
        pygame.display.flip()
