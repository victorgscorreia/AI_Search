import pygame
import io
import time

class DisplayMaze:
    
    def __init__(self, width, height, maze):
        
        self.width = width
        self.height = height
        self.maze = maze
        self.screen = pygame.display.set_mode([width,height])
        self.screen.fill([75, 160, 255])

        lines = maze.split('\n')
        
        lines_num = len(lines)
        colum_num = len(lines[0])

        if(lines_num/3 > colum_num/4):
            self.size_block = int((self.height-lines_num+1)/lines_num)
        else:
            self.size_block = int((self.width-colum_num+1)/colum_num)
        
        for i in range(lines_num):
            for j in range(colum_num):
                if(lines[i][j] == '*'):
                    colorR = 255
                    colorG = 255
                    colorB = 255

                elif (lines[i][j] == '-'):
                    colorR = 0
                    colorG = 0
                    colorB = 0
                
                elif (lines[i][j] == '#'):
                    colorR = 0
                    colorG = 0
                    colorB = 255
                
                elif (lines[i][j] == '$'):
                    colorR = 255
                    colorG = 0
                    colorB = 0
                
                else:
                    colorR = 0
                    colorG = 255
                    colorB = 0

                pygame.draw.rect(self.screen, [colorR, colorG, colorB], [j*(self.size_block+1), i*(self.size_block+1), self.size_block, self.size_block], 0)

        pygame.display.flip()



    def drawStep(self, x_maze, y_maze,color):
        pygame.draw.rect(self.screen, color, [y_maze*(self.size_block+1), x_maze*(self.size_block+1), self.size_block, self.size_block], 0)
        pygame.display.flip()

    def status(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        return True

    def quit(self):
        pygame.quit()