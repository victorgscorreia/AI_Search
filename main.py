import numpy as np
import draw as dw
import time
import queue
import random
from tqdm import tqdm
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

def teste_busca(busca,maze_matrix,size,ini,end,tam_caminho_otimo,num_testes=100, heuristica=None):
    tempo_medio = 0
    achou = 0
    c_v_media = 0
    c_q_media = 0
    memoria_media = 0
    achou_caminho_otimo = 0
    for j in range(num_testes):
        #fazendo a busca
        inicio = 0
        fim = 0
        if heuristica is None:
            inicio = time.time()
            ant_i,ant_j,c_v,c_q,max_tam_queue = busca(maze_matrix,ini,end,size,display=None)
            fim = time.time()
        else:
            inicio = time.time()
            ant_i,ant_j,c_v,c_q,max_tam_queue = busca(maze_matrix,ini,end,size,heuristica,display=None)
            fim = time.time()

        #guardando as metricas da busca em seus respectivos valores
        tempo_medio += fim - inicio
        if ant_i is not None:
            achou += 1
            caminho = print_caminho(end[0], end[1],ant_i, ant_j,None,ini,end)
            tam_caminho = len(caminho)
            if tam_caminho == tam_caminho_otimo:
                achou_caminho_otimo += 1
        c_v_media += c_v
        c_q_media += c_q
        memoria_media += max_tam_queue
        

    tempo_medio = tempo_medio/num_testes
    por_achou = achou*100/num_testes
    por_cam_otimo = achou_caminho_otimo*100/num_testes
    memoria_media = memoria_media/num_testes

    return tempo_medio, memoria_media,  por_achou, por_cam_otimo

def analise():
    num_mazes = 8
    maze_files = []
    buscas_cega = [largura,profundidade]
    buscas_heuristica = [bfs,A_Star,hill_climbing]
    heuristicas = [heuristica_manhattan]
    num_testes = 50

    for i in range(num_mazes):
        maze_files.append( "mazes_created/maze" + str(i+1)+".txt" )
    
    for i in range(num_mazes):

        file = open(maze_files[i],'r')
        size = file.readline()
        size = size.split(' ')
        size = [int(i) for i in size]
        maze_string = file.readline().strip()
        for j in range(size[0]-1):
            s = file.readline().strip()
            maze_string = maze_string + "\n" + s
        maze_matrix,ini,end = creat_matrix_np(maze_string, size)

        #achando o tamanho do caminho otimo para fazermos comparacao
        ant_i,ant_j,_,_,_ = A_Star(maze_matrix,ini,end,size,heuristica_manhattan,display=None)
        caminho = print_caminho(end[0], end[1],ant_i, ant_j,None,ini,end)
        tam_caminho_otimo = len(caminho)

        for cega in buscas_cega:
            tempo_medio, memoria_media,  por_achou, por_cam_otimo = teste_busca(cega,maze_matrix,size,ini,end,tam_caminho_otimo,num_testes)
            
            print("Resultados de " + cega.__name__ + " em " + maze_files[i])
            print("TM:  " + str(tempo_medio))
            print("ME:  " + str(memoria_media))
            print("PA:  " + str(por_achou))
            print("PAO: " + str(por_cam_otimo))
        
        for busca_h in buscas_heuristica:
            for heuristica in heuristicas:
                tempo_medio, memoria_media,  por_achou, por_cam_otimo = teste_busca(busca_h,maze_matrix,size,ini,end,tam_caminho_otimo,num_testes,heuristica=heuristica)
            
                print("Resultados de " + busca_h.__name__ + " em " + maze_files[i] + " com " + heuristica.__name__)
                print("TM:  " + str(tempo_medio))
                print("ME:  " + str(memoria_media))
                print("PA:  " + str(por_achou))
                print("PAO: " + str(por_cam_otimo))
            
def visualizacao():
    maze_string, size = read_maze()
    maze_matrix,ini,end = creat_matrix_np(maze_string, size)


    display = dw.DisplayMaze(800, 800, maze_string)
    
    
    ant_i,ant_j,c_v,c_q,max_tam_queue = bfs(maze_matrix,ini,end,size,display=display)
    tam_caminho = 0
    if ant_i is not None:
        caminho = print_caminho(end[0], end[1],ant_i, ant_j,display,ini,end)
        print(caminho)
    else:
        print("Nao foi encontrado caminho algum")

    while display.status():
        i = 1+1
    display.quit()

def main():
    analise()
    
if __name__ == '__main__':
    main()