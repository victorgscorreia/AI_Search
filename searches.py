
import numpy as np
import draw as dw
import time
import queue
import random


COLOR_RIGHT_PATH = [0,255,127]
COLOR_VISITED = [255, 203, 219]
COLOR_IN_QUEUE = [128,128,128]
TIME_WAIT = 0


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


def print_caminho(i,j, anterior_i, anterior_j, display,ini,end):
    i = int(i)
    j = int(j)
    
    ret = []
    if anterior_i[i][j] != -1:
        ret = print_caminho( anterior_i[i][j], anterior_j[i][j], anterior_i,anterior_j,display,ini,end ) 

    if display is not None and ( i != ini[0] or j != ini[1]) and (i != end[0] or j != end[1]):
        display.drawStep(i,j,COLOR_RIGHT_PATH)
    time.sleep(TIME_WAIT)  
    ret.append( (i,j) )
    return ret

class Cell:

    def __init__(self, i, j, depth, heuristica):
        self.i = i
        self.j = j
        self.depth = depth
        self.h = heuristica
    
    #as funcoes abaixo deixam a classe comparavel
    def __lt__(self,other):
        return self.h + self.depth < other.h + other.depth

    def __eq__(self,other):
        return self.h + self.depth == other.h + other.depth

    def __ne__(self,other):
        return self.h + self.depth != other.h + other.depth

    def __le__(self,other):
        return self.h + self.depth <= other.h + other.depth

    def __gt__(self,other):
        return self.h + self.depth > other.h + other.depth

    def __ge__(self,other):
        return self.h + self.depth >= other.h + other.depth

def heuristica_manhattan(i,j, i_target, j_target):
    return abs(i - i_target) + abs(j - j_target)

def heu_equal(i,j,i_target,j_target):
    heu = 0
    if i != i_target:
        heu += 1
    if j != j_target:
        heu += 1
    return heu

def heuristica_euclidiana(i,j, i_target, j_target):
    a = i - i_target
    b = j - j_target
    return np.sqrt(a*a + b*b)

def A_Star(maze_matrix,ini,end, size, heuristica,display):

    visitado = np.zeros((size[0],size[1]))
    anterior_i = -1*np.ones((size[0],size[1]))
    anterior_j = -1*np.ones((size[0],size[1]))

    q = queue.PriorityQueue()

    heu = heuristica(ini[0],ini[1],end[0],end[1])
    ini_cell = Cell(ini[0],ini[1],0,heu)
    q.put(ini_cell)
    
    count_visited = 0
    count_in_queue = 0

    max_tam_queue = 1

    while not q.empty():

        if max_tam_queue < q.qsize():
            max_tam_queue = q.qsize()

        ele_cell = q.get()
        ele = np.zeros((2,)).astype(int)

        ele[0] = ele_cell.i
        ele[1] = ele_cell.j

        visitado[ele[0],ele[1]] = 2
        
        count_visited += 1

        if ele[0] == end[0] and ele[1] == end[1]:
            return anterior_i,anterior_j, count_visited, count_in_queue, max_tam_queue
        
        nexts = next_steps(ele,size,visitado,maze_matrix)

        for n in nexts:
            if display is not None and (n[0] != end[0] or n[1] != end[1]):
                display.drawStep(n[0],n[1],COLOR_IN_QUEUE)

            anterior_i[n[0]][n[1]] = ele[0]

            anterior_j[n[0]][n[1]] = ele[1]

            visitado[n[0]][n[1]] = 1
            
            count_in_queue += 1
            n_heu = heuristica(n[0],n[1],end[0],end[1])
            n_cell = Cell(n[0],n[1],ele_cell.depth+1, n_heu)
            q.put(n_cell)
        
        #nao pintar o ultimo nem o primeiro
        if display is not None and (ele[0] != ini[0] or ele[1] != ini[1]):
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, max_tam_queue

def largura(maze_matrix,ini,end, size,display):

    visitado = np.zeros((size[0],size[1]))
    anterior_i = -1*np.ones((size[0],size[1]))
    anterior_j = -1*np.ones((size[0],size[1]))
    q = queue.Queue()

    q.put(ini)
    
    count_visited = 0
    count_in_queue = 0

    max_tam_queue = 1

    while not q.empty():

        if max_tam_queue < q.qsize():
            max_tam_queue = q.qsize()

        ele = q.get()
        visitado[ele[0],ele[1]] = 2
        
        count_visited += 1

        if ele[0] == end[0] and ele[1] == end[1]:
            return anterior_i,anterior_j, count_visited, count_in_queue, max_tam_queue
        
        nexts = next_steps(ele,size,visitado,maze_matrix)

        for n in nexts:
            if display is not None and (n[0] != end[0] or n[1] != end[1]):
                display.drawStep(n[0],n[1],COLOR_IN_QUEUE)

            anterior_i[n[0]][n[1]] = ele[0]

            anterior_j[n[0]][n[1]] = ele[1]

            visitado[n[0]][n[1]] = 1
            
            count_in_queue += 1

            q.put(n)
        
        #nao pintar o ultimo nem o primeiro
        if display is not None and (ele[0] != ini[0] or ele[1] != ini[1]):
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, max_tam_queue

def profundidade(maze_matrix,ini,end, size,display):

    visitado = np.zeros((size[0],size[1]))
    anterior_i = -1*np.ones((size[0],size[1]))
    anterior_j = -1*np.ones((size[0],size[1]))
    q = queue.LifoQueue()

    q.put(ini)
    
    count_visited = 0
    count_in_queue = 0

    max_tam_queue = 1

    while not q.empty():

        if max_tam_queue < q.qsize():
            max_tam_queue = q.qsize()
            
        ele = q.get()
        visitado[ele[0],ele[1]] = 2
        
        count_visited += 1

        if ele[0] == end[0] and ele[1] == end[1]:
            return anterior_i,anterior_j, count_visited, count_in_queue, max_tam_queue
        
        nexts = next_steps(ele,size,visitado,maze_matrix)

        for n in nexts:
            if display is not None and (n[0] != end[0] or n[1] != end[1]):
                display.drawStep(n[0],n[1],COLOR_IN_QUEUE)

            anterior_i[n[0]][n[1]] = ele[0]

            anterior_j[n[0]][n[1]] = ele[1]

            visitado[n[0]][n[1]] = 1
            
            count_in_queue += 1

            q.put(n)
        
        #nao pintar o ultimo nem o primeiro
        if display is not None and (ele[0] != ini[0] or ele[1] != ini[1]):
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, max_tam_queue

def bfs(maze_matrix,ini,end, size, heuristica,display):
    visitado = np.zeros((size[0],size[1]))
    anterior_i = -1*np.ones((size[0],size[1]))
    anterior_j = -1*np.ones((size[0],size[1]))

    q = queue.PriorityQueue()
    heu = heuristica(ini[0],ini[1],end[0],end[1])
    ini_cell = Cell(ini[0],ini[1],0,heu)
    q.put(ini_cell)
    
    count_visited = 0
    count_in_queue = 0

    max_tam_queue = 1

    while not q.empty():

        if max_tam_queue < q.qsize():
            max_tam_queue = q.qsize()

        ele_cell = q.get()
        ele = np.zeros((2,)).astype(int)

        ele[0] = ele_cell.i
        ele[1] = ele_cell.j

        visitado[ele[0],ele[1]] = 2
        
        count_visited += 1

        if ele[0] == end[0] and ele[1] == end[1]:
            return anterior_i,anterior_j, count_visited, count_in_queue,max_tam_queue
        
        nexts = next_steps(ele,size,visitado,maze_matrix)

        for n in nexts:
            if display is not None and (n[0] != end[0] or n[1] != end[1]):
                display.drawStep(n[0],n[1],COLOR_IN_QUEUE)

            anterior_i[n[0]][n[1]] = ele[0]

            anterior_j[n[0]][n[1]] = ele[1]

            visitado[n[0]][n[1]] = 1
            
            count_in_queue += 1
            heu = heuristica(n[0],n[1],end[0],end[1])
            n_cell = Cell(n[0],n[1],0, heu)
            q.put(n_cell)
        
        #nao pintar o ultimo nem o primeiro
        if display is not None and (ele[0] != ini[0] or ele[1] != ini[1]):
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, max_tam_queue

def hill_climbing(maze_matrix,ini,end, size, heuristica,display):

    visitado = np.zeros((size[0],size[1]))
    anterior_i = -1*np.ones((size[0],size[1]))
    anterior_j = -1*np.ones((size[0],size[1]))

    q = queue.PriorityQueue()

    heu = heuristica(ini[0],ini[1],end[0],end[1])
    ini_cell = Cell(ini[0],ini[1],0,heu)
    q.put(ini_cell)
    
    count_visited = 0
    count_in_queue = 0

    while not q.empty():
        count_in_queue += 1
        ele_cell = q.get()
        ele = np.zeros((2,)).astype(int)

        ele[0] = ele_cell.i
        ele[1] = ele_cell.j

        visitado[ele[0],ele[1]] = 2
        
        count_visited += 1

        if ele[0] == end[0] and ele[1] == end[1]:
            return anterior_i,anterior_j, count_visited, count_in_queue,1
        
        nexts = next_steps(ele,size,visitado,maze_matrix)

        min_cell = ele_cell

        random.shuffle(nexts)
        for n in nexts:
            
            anterior_i[n[0]][n[1]] = ele[0]

            anterior_j[n[0]][n[1]] = ele[1]

            visitado[n[0]][n[1]] = 1
            
            
            n_heu = heuristica(n[0],n[1],end[0],end[1])
            n_cell = Cell(n[0],n[1],0, n_heu)
            if n_cell <= min_cell:
                min_cell = n_cell
        
        if min_cell.i != ele[0] or min_cell.j != ele[1]:
            q.put(min_cell)
        #nao pintar o ultimo nem o primeiro
        if display is not None and (ele[0] != ini[0] or ele[1] != ini[1]):
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, 1