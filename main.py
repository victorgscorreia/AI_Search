import numpy as np
import draw as dw
import time
import queue

COLOR_RIGHT_PATH = [0,255,127]
COLOR_VISITED = [255, 203, 219]
COLOR_IN_QUEUE = [128,128,128]
TIME_WAIT = 0.05


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


def next_steps(element,size,visitado,maze_matrix):
    moves = [[-1,0],[1,0],[0,-1],[0,1]]
    
    nexts = []

    for move in moves:
        n = np.zeros((2,)).astype(int)
        n[0] = move[0] + element[0]
        n[1] = move[1] + element[1]

        if n[0] < 0 or n[0] >= size[0]:
            continue
        if n[1] < 0 or n[1] >= size[1]:
            continue
        if visitado[n[0],n[1]] != 0:
            continue
        if maze_matrix[n[0]][n[1]] == 0:
            continue
        nexts.append(n)
    
    return nexts


def largura(maze_matrix,ini,end, size,display):
    visitado = np.zeros((size[0],size[1]))
    anterior_i = -1*np.ones((size[0],size[1]))
    anterior_j = -1*np.ones((size[0],size[1]))
    q = queue.Queue()

    q.put(ini)

    while not q.empty():
        ele = q.get()
        visitado[ele[0],ele[1]] = 2
        

        if ele[0] == end[0] and ele[1] == end[1]:
            return anterior_i,anterior_j
        
        nexts = next_steps(ele,size,visitado,maze_matrix)

        for n in nexts:
            if n[0] != end[0] or n[1] != end[1]:
                display.drawStep(n[0],n[1],COLOR_IN_QUEUE)

            anterior_i[n[0]][n[1]] = ele[0]

            anterior_j[n[0]][n[1]] = ele[1]

            visitado[n[0]][n[1]] = 1

            q.put(n)
        
        #nao pintar o ultimo nem o primeiro
        if ele[0] != ini[0] or ele[1] != ini[1]:
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
        time.sleep(TIME_WAIT)
            
    return None,None

def print_caminho(i,j, anterior_i, anterior_j, display,ini,end):
    i = int(i)
    j = int(j)
    if anterior_i[i][j] != -1:
        print_caminho( anterior_i[i][j], anterior_j[i][j], anterior_i,anterior_j,display,ini,end ) 
        
    if (i != ini[0] or j != ini[1]) and (i != end[0] or j != end[1]):
        display.drawStep(i,j,COLOR_RIGHT_PATH)
    time.sleep(TIME_WAIT)   


def main():

    maze_string, size = read_maze()
    maze_matrix,ini,end = creat_matrix_np(maze_string, size)


    display = dw.DisplayMaze(800, 800, maze_string)
    

    ant_i,ant_j = largura(maze_matrix,ini,end,size,display)
    
    if ant_i is not None:
        print_caminho(end[0], end[1],ant_i, ant_j,display,ini,end)

    while display.status():
        i = 1+1
    display.quit()
if __name__ == '__main__':
    main()