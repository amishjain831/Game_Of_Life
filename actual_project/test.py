import pygame
import sys
import numpy as np
from constants import *

def life_step(x, y, world):
    neighbours = np.sum(world[x - 1: x + 2, y - 1: y + 2])
    actual = neighbours - world[x,y] 

    if world[x, y] == 1 and not 2 <= actual <= 3:
        return 0
    elif actual == 3:
        return 1
    return world[x, y]


def game_start(option):
    if(int(option) == 0):
        choice = input("choose 0 for default user input and 1 to give input: ")
        if int(choice):
            print("Enter the entries in a single line (separated by space): ") 
            entries = list(map(int, input().split())) 
            world = np.array(entries).reshape(screenL // cellSize + 1, screenW // cellSize + 1) 
        if int(choice) == 0:
            print("for static configuration choose 0")
            print("for simple oscillation configurations (Blinker and Toad) choose 1")
            print("for 'Gasper Glister Gunr' configuration choose 2")
            print("for 'beacon' configuration choose 3")
            config = input("choose your option: ")


            if int(config) == 0:
                world  = np.zeros((screenL // cellSize + 1, screenW // cellSize + 1))
                world[2:4, 1:3] = 1
                world[1:4, 5:9] = [[0, 1, 1, 0],[1, 0, 0, 1],[0, 1, 1, 0]]
                world[1:5, 11:15] = [[0, 1, 1, 0],[1, 0, 0, 1],[0, 1, 0, 1],[0, 0, 1, 0]]
                world[1:4, 17:20] = [[1, 1, 0],[1, 0, 1],[0, 1, 0]]
            if int(config) == 1:
                blinker = [1, 1, 1]
                toad = [[1, 1, 1, 0],
                        [0, 1, 1, 1]]
                world  = np.zeros((screenL // cellSize + 1, screenW // cellSize + 1))
                world[2, 1:4] = blinker
                world[2:4, 6:10] = toad

            if int(config) == 2:
                world  = np.zeros((screenL // cellSize + 1, screenW // cellSize + 1))
                glider_gun =[[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
                world[1:37,1:10] = np.array(glider_gun).T

            if int(config) == 3:
                world  = np.zeros((screenL // cellSize + 1, screenW // cellSize + 1))

                beacon = [[1, 1, 0, 0],[1, 1, 0, 0],[0, 0, 1, 1],[0, 0, 1, 1]]
                world[1:5, 1:5] = beacon                
                



    if(int(option)):
        world  = np.zeros((screenL // cellSize + 1, screenW // cellSize + 1))
        world = np.random.choice(a=[0, 1], size=(screenL // cellSize + 1, screenW // cellSize + 1))

    pygame.init()
    screen = pygame.display.set_mode((screenL, screenW))
    fps = 10
    clock = pygame.time.Clock()



    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:  # Restart world
                    world = np.random.choice(a=[0, 1], size=(screenL // cellSize + 1, screenW // cellSize + 1))
                if event.key == pygame.K_q:
                    fps += 1
                if event.key == pygame.K_a:
                    fps -= 1
                    if fps == 0:
                        fps = 1

        pygame.display.set_caption("Convay\'s Game Of Life " + str(fps) + "fps ")
        screen.fill(backgroundColor)

        newWorld = np.copy(world)
        #iterate over the array
        for (x, y), value in np.ndenumerate(world):
            newWorld[x, y] = life_step(x, y, world)

            if newWorld[x, y] == 1:
                pygame.draw.rect(screen, cellColor, (cellSize * (x), cellSize * (y), cellSize, cellSize), 2)

        world = newWorld
        pygame.display.update()
        clock.tick(fps)

if __name__ == "__main__":
    option = input("choose 0 for initial user input and 1 for random start: ")
    game_start(int(option))        
