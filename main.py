import numpy as np
import draw as dw
import time
import queue
import random
from searches import *

def read_maze():
    size = input()
    size = size.split(' ')
    size = [int(i) for i in size]

    maze_string = input()

    for i in range(size[0]-1):
        maze_string = maze_string + "\n" + input()

    return maze_string, size

def creat_matrix_np(maze_string, size):
    
    maze_matrix = np.zeros([size[0],size[1]])

    lines = maze_string.split('\n')
    lines_num = len(lines)
    colum_num = len(lines[0])

    ini  = np.zeros((2,)).astype(int)
    end  = np.zeros((2,)).astype(int)

    for i in range(lines_num):
        for j in range(colum_num):

            if lines[i][j] == '*':
                maze_matrix[i][j] = 1

            elif lines[i][j] == '-':
                maze_matrix[i][j] = 0
            
            elif lines[i][j] == '#':
                maze_matrix[i][j] = 2
                ini[0] = i
                ini[1] = j

            elif lines[i][j] == '$':
                maze_matrix[i][j] = 3
                end[0] = i
                end[1] = j

            else:
                maze_matrix[i][j] = -1

    return maze_matrix,ini,end


def main():

    maze_string, size = read_maze()
    maze_matrix,ini,end = creat_matrix_np(maze_string, size)


    display = dw.DisplayMaze(800, 800, maze_string)
    
    
    ant_i,ant_j,c_v,c_q,max_tam_queue = profundidade(maze_matrix,ini,end,size,display)
    tam_caminho = 0
    if ant_i is not None:
        tam_caminho = print_caminho(end[0], end[1],ant_i, ant_j,display,ini,end)

    print("numero visitados = " + str(c_v))
    print("numero colocados na fila = " + str(c_q))
    print("tamanho maximo da estrutura de dados = " + str(max_tam_queue))
    print("tamanho do caminho achado = " + str(tam_caminho))

    while display.status():
        i = 1+1
    display.quit()
if __name__ == '__main__':
    main()