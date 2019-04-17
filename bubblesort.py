import time, sys, pygame
import random
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


def bubble_sort(nlist, i, end_ind):

    if i == end_ind:
        return 0, end_ind-1

    if nlist[i].val > nlist[i+1].val:
        nlist.swap(i, i+1)

    return i+1, end_ind


if __name__ == '__main__':
    pygame.init()

    i = 0
    end_ind = len(num)-1

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # display
        for n in num:
            n.set_color((255,255,255))
        if end_ind != 0:
            num[i].set_color((0,255,0))

        # if not finish, continue sort
        if end_ind != 0:
            i, end_ind = bubble_sort(num, i, end_ind)

        num.update()
        draw_all()
