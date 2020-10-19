
import numpy as np
import draw as dw
import time
import queue
import random


COLOR_RIGHT_PATH = [0,255,127]
COLOR_VISITED = [255, 203, 219]
COLOR_IN_QUEUE = [128,128,128]
TIME_WAIT = 0.01

'''
NEXTS_STEPS
    Calcula os elementos adjacentes a um elemento que ainda nao foram colocados
    na estrutura de dados e os retorna
    
    @PARAMETROS
        element - vetor de 2 valores - elemento ao qual queremos saber seus 
                adjacentes
        size - vetor de 2 valores - tamanho do maze
        visitado - matriz de mesma dimensao do maze - representa os elementos
                    ja colocados na estrutura de dados
        maze_matrix - matriz que representa nosso maze
    @RETORNO
        lista de elementos adjacentes ainda nao colocados na ED, pode retornar
        uma lsita vazia.
'''
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

'''
PRINT_CAMINHO
    Esta funcao faz o bakctracking de uma busca qualquer para encontrar o caminho
    achado por ela.
    @PARAMETROS
        i - linha do elemento atual, ao chamar a funcao passar a linha do 
            elemento destino
        j - coluna do elemento atual, ao chamar a funcao passar a coluna do 
            elemento destino
        ini - vetor de dimensao 2 -  posicao inicial da busca
        end - vetor de dimensao 2 - posicao destino da busca
        display - o display onde se passara a visualizacao da busca, 
            None significa sem visualizacao

        anterior_i: retornado da busca - uma matriz da mesma dimensao do maze, o valor 
            anterior_i[i][j] guarda a linha do elemento anterior a i,j na 
            busca, ou -1 caso seja o ponto de partida da busca ou a busca nao 
            tenha passado pela posicao i,j 

        anterior_j: retornado da busca - uma matriz da mesma dimensao do maze, o valor 
            anterior_i[i][j] guarda a coluna do elemento anterior a i,j na 
            busca, ou -1 caso seja o ponto de partida da busca ou a busca nao 
            tenha passado pela posicao i,j 
    @RETORNO
        lista de elementos do caminho encontrado, pronto para ser printado na
        saida padrao como pedido na especificacao do trabalho
'''
def print_caminho(i,j, anterior_i, anterior_j, display,ini,end):
    i = int(i)
    j = int(j)
    
    ret = []
    #se ainda tem um anterior ao elemento i,j, chama-se a recursao para o ele
    #anterior
    if anterior_i[i][j] != -1:
        ret = print_caminho( anterior_i[i][j], anterior_j[i][j], anterior_i,anterior_j,display,ini,end ) 
    
    #se a visualizacao estiver ativa, pinta o elemento cor a cor COLOR_RIGHT_PATH
    #nao pinta o elemento inicial nem o elemento destino
    if display is not None and ( i != ini[0] or j != ini[1]) and (i != end[0] or j != end[1]):
        display.status()
        display.drawStep(i,j,COLOR_RIGHT_PATH)
        time.sleep(TIME_WAIT)  
    ret.append( (i,j) )
    return ret

'''
Cell
    Esta classe eh utilizada pelas busca A* e BFS
    para facilitar achar o elemento a ser proximo a ser
    processado, que eh o elemetno que tem o menor f(x)=g(x)+h(x)
    no caso de A*, e o menor h(x) no caso da bfs.

    A classe tem 4 atributos:
        i - a linha que o elemento esta no maze
        j - a coluna que o elemento esta no maze
        depth - g(x) - profundidade na busca.
        heuristica - h(x) - calculada fora da classe utilizando uma
        funcao heuristica
        
    todos estes elementos devem ser passados ao criar um objeto da
    classe.
    Para facilitar a implementacao, no caso da bfs, coloca-se sempre
    depth = g(x) = 0.
    O metodos da classe sao os metodos necessarios para tornar a 
    classe comparavel e poder colocala numa PriorityQueue.
'''
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

'''
Manhattan
    Heuristica calculada a partir da distancia de manhattan
    Formula eh: d = |x1-x2|+|y1-y2|
    @PARAMETROS
        i - linha do elemento atual
        j - coluna do elemento atual
        i_target - linha do elemento destino
        j_target - coluna do elemento destino
    @RETORNO
        d - distancia de manhattan entre um elemento e o elemento
            destino
'''
def heuristica_manhattan(i,j, i_target, j_target):
    return abs(i - i_target) + abs(j - j_target)

'''
Euclidiana
    Heuristica calculada a partir da distancia euclidiana
    Formula eh: d = sqrt( (x1-x2)^2 + (y1-y2)^2 )
    @PARAMETROS 
        i - linha do elemento atual
        j - coluna do elemento atual
        i_target - linha do elemento destino
        j_target - coluna do elemento destino
    @RETORNO
        d - distancia euclidiana entre um elemento e o elemento
            destino
'''
def heuristica_euclidiana(i,j, i_target, j_target):
    a = i - i_target
    b = j - j_target
    return np.sqrt(a*a + b*b)

'''
A* - A Estrela
    Esta funcao faz a busca heuristica A* em um maze, a partir de um estado
    inicial ini e tenta chegar ao estado end, utilizando uma heuristica 
    passada.

    @PARAMETROS
    maze_matrix - matriz que representa o maze
    ini - vetor de dimensao 2 -  posicao inicial da busca
    end - vetor de dimensao 2 - posicao destino da busca
    size - vetor de dimensao 2 - representa o tamanho da matriz maze_matrix
    heuristica - heuristica a ser utilizada na busca
    display - o display onde se passara a visualizacao da busca, 
              None significa sem visualizacao

    @RETORNO
    em caso de a busca ser bem sucedida retornara a quintupla:
        anterior_i,anterior_j, count_visited, count_in_queue, max_tam_queue
    onde cada uma dessa quintupla significa:

        anterior_i: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a linha do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 

        anterior_j: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a coluna do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 
        
        count_visited: numero de elementos que a busca processou, processar 
                        significa verificar se é o elemento destino e colocar os
                        elementos adjacentes na estrutura de dados.
        
        count_in_queue: numero de elemento que foram colocados na estrutura de 
                        dados para serem processados
        
        max_tam_queue: numero maximo de elementos que a estrutura de dados guardou
                        em determinado momento, representa a memoria utlilizada
                        pela busca.

    em caso de falha, retorna a quintupla:
        None,None, count_visited, count_in_queue,max_tam_queue
'''
def A_Star(maze_matrix,ini,end, size, heuristica,display=None):

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
                display.status()
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
            display.status()
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, max_tam_queue

'''
LARGURA
    Esta funcao faz a busca em largura em um maze, a partir de um estado
    inicial ini e tenta chegar ao estado end

    @PARAMETROS
    maze_matrix - matriz que representa o maze
    ini - vetor de dimensao 2 -  posicao inicial da busca
    end - vetor de dimensao 2 - posicao destino da busca
    size - vetor de dimensao 2 - representa o tamanho da matriz maze_matrix
    display - o display onde se passara a visualizacao da busca, 
              None significa sem visualizacao

    @RETORNO
    em caso de a busca ser bem sucedida retornara a quintupla:
        anterior_i,anterior_j, count_visited, count_in_queue, max_tam_queue
    onde cada uma dessa quintupla significa:

        anterior_i: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a linha do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 

        anterior_j: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a coluna do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 
        
        count_visited: numero de elementos que a busca processou, processar 
                        significa verificar se é o elemento destino e colocar os
                        elementos adjacentes na estrutura de dados.
        
        count_in_queue: numero de elemento que foram colocados na estrutura de 
                        dados para serem processados
        
        max_tam_queue: numero maximo de elementos que a estrutura de dados guardou
                        em determinado momento, representa a memoria utlilizada
                        pela busca.

    em caso de falha, retorna a quintupla:
        None,None, count_visited, count_in_queue,max_tam_queue
'''
def largura(maze_matrix,ini,end, size,display=None):

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
                display.status()
                display.drawStep(n[0],n[1],COLOR_IN_QUEUE)

            anterior_i[n[0]][n[1]] = ele[0]

            anterior_j[n[0]][n[1]] = ele[1]

            visitado[n[0]][n[1]] = 1
            
            count_in_queue += 1

            q.put(n)
        
        #nao pintar o ultimo nem o primeiro
        if display is not None and (ele[0] != ini[0] or ele[1] != ini[1]):
            display.status()
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, max_tam_queue

'''
PROFUNDIDADE
    Esta funcao faz a busca em profundidade em um maze, a partir de um estado
    inicial ini e tenta chegar ao estado end

    @PARAMETROS
    maze_matrix - matriz que representa o maze
    ini - vetor de dimensao 2 -  posicao inicial da busca
    end - vetor de dimensao 2 - posicao destino da busca
    size - vetor de dimensao 2 - representa o tamanho da matriz maze_matrix
    display - o display onde se passara a visualizacao da busca, 
              None significa sem visualizacao

    @RETORNO
    em caso de a busca ser bem sucedida retornara a quintupla:
        anterior_i,anterior_j, count_visited, count_in_queue, max_tam_queue
    onde cada uma dessa quintupla significa:

        anterior_i: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a linha do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 

        anterior_j: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a coluna do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 
        
        count_visited: numero de elementos que a busca processou, processar 
                        significa verificar se é o elemento destino e colocar os
                        elementos adjacentes na estrutura de dados.
        
        count_in_queue: numero de elemento que foram colocados na estrutura de 
                        dados para serem processados
        
        max_tam_queue: numero maximo de elementos que a estrutura de dados guardou
                        em determinado momento, representa a memoria utlilizada
                        pela busca.

    em caso de falha, retorna a quintupla:
        None,None, count_visited, count_in_queue,max_tam_queue
'''
def profundidade(maze_matrix,ini,end, size,display=None):

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
                display.status()
                display.drawStep(n[0],n[1],COLOR_IN_QUEUE)

            anterior_i[n[0]][n[1]] = ele[0]

            anterior_j[n[0]][n[1]] = ele[1]

            visitado[n[0]][n[1]] = 1
            
            count_in_queue += 1

            q.put(n)
        
        #nao pintar o ultimo nem o primeiro
        if display is not None and (ele[0] != ini[0] or ele[1] != ini[1]):
            display.status()
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, max_tam_queue

'''
BFS
    Esta funcao faz a busca heuristica BFS em um maze, a partir de um estado
    inicial ini e tenta chegar ao estado end, utilizando uma heuristica 
    passada.

    @PARAMETROS
    maze_matrix - matriz que representa o maze
    ini - vetor de dimensao 2 -  posicao inicial da busca
    end - vetor de dimensao 2 - posicao destino da busca
    size - vetor de dimensao 2 - representa o tamanho da matriz maze_matrix
    heuristica - heuristica a ser utilizada na busca
    display - o display onde se passara a visualizacao da busca, 
              None significa sem visualizacao

    @RETORNO
    em caso de a busca ser bem sucedida retornara a quintupla:
        anterior_i,anterior_j, count_visited, count_in_queue, max_tam_queue
    onde cada uma dessa quintupla significa:

        anterior_i: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a linha do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 

        anterior_j: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a coluna do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 
        
        count_visited: numero de elementos que a busca processou, processar 
                        significa verificar se é o elemento destino e colocar os
                        elementos adjacentes na estrutura de dados.
        
        count_in_queue: numero de elemento que foram colocados na estrutura de 
                        dados para serem processados
        
        max_tam_queue: numero maximo de elementos que a estrutura de dados guardou
                        em determinado momento, representa a memoria utlilizada
                        pela busca.

    em caso de falha, retorna a quintupla:
        None,None, count_visited, count_in_queue,max_tam_queue
'''
def bfs(maze_matrix,ini,end, size, heuristica,display=None):
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
                display.status()
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
            display.status()
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, max_tam_queue

'''
Hill Climbing
    Esta funcao faz a busca heuristica Hill Climbing em um maze, a partir de um 
    estado inicial ini e tenta chegar ao estado end, utilizando uma heuristica
    passada.

    @PARAMETROS
    maze_matrix - matriz que representa o maze
    ini - vetor de dimensao 2 -  posicao inicial da busca
    end - vetor de dimensao 2 - posicao destino da busca
    size - vetor de dimensao 2 - representa o tamanho da matriz maze_matrix
    heuristica - heuristica a ser utilizada na busca
    display - o display onde se passara a visualizacao da busca, 
              None significa sem visualizacao

    @RETORNO
    em caso de a busca ser bem sucedida retornara a quintupla:
        anterior_i,anterior_j, count_visited, count_in_queue, max_tam_queue
    onde cada uma dessa quintupla significa:

        anterior_i: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a linha do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 

        anterior_j: uma matriz da mesma dimensao do maze, o valor anterior_i[i][j] 
                    guarda a coluna do elemento anterior a i,j na busca, ou -1 caso
                    seja o ponto de partida da busca ou a busca nao tenha passado 
                    pela posicao i,j 
        
        count_visited: numero de elementos que a busca processou, processar 
                        significa verificar se é o elemento destino e colocar os
                        elementos adjacentes na estrutura de dados.
        
        count_in_queue: numero de elemento que foram colocados na estrutura de 
                        dados para serem processados
        
        max_tam_queue: numero maximo de elementos que a estrutura de dados guardou
                        em determinado momento, representa a memoria utlilizada
                        pela busca.

    em caso de falha, retorna a quintupla:
        None,None, count_visited, count_in_queue,max_tam_queue
'''
def hill_climbing(maze_matrix,ini,end, size, heuristica,display=None):

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
            display.status()
            display.drawStep(ele[0],ele[1],COLOR_VISITED)
            time.sleep(TIME_WAIT)
            
    return None,None, count_visited, count_in_queue, 1