import numpy as np
import draw as dw
import time

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

    for i in range(lines_num):
        for j in range(colum_num):

            if lines[i][j] == '*':
                maze_matrix[i][j] = 1

            elif lines[i][j] == '-':
                maze_matrix[i][j] = 0
            
            elif lines[i][j] == '#':
                maze_matrix[i][j] = 2

            elif lines[i][j] == '$':
                maze_matrix[i][j] = 3

            else:
                maze_matrix[i][j] = -1

    return maze_matrix

def main():

    maze_string, size = read_maze()
    maze_matrix = creat_matrix_np(maze_string, size)

    print(maze_matrix)

    display = dw.DisplayMaze(1280, 960, maze_string)
    display.drawStep(5,5)
    time.sleep(10)
    display.quit()


if __name__ == '__main__':
    main()