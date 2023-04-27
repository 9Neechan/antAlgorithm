import matplotlib.pyplot as plt
import networkx as nx
import random
import math


def create_multigraph_struct(graph):
    G = nx.MultiDiGraph()
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] != 0 and i != j:
                G.add_edge(f'{i}', f'{j}', weight=graph[i][j])
    return G


def create_graph_struct(path_arr, graph):
    G = nx.DiGraph()
    data = []
    for j in range(len(path_arr)):
        if j + 1 < len(path_arr):
            data.append(path_arr[j + 1])
    data.append(path_arr[0])
    for i in range(len(path_arr)):
        G.add_edge(f'{path_arr[i]}', f'{data[i]}', weight=graph[path_arr[i]][data[i]])
    return G


def make_plt(flag, path_arr, graph, i, path_len, tao):
    """Рисует графы с помощью бибилиотеки matplotlib и сохраняет в папку pictures"""
    pos = {'0': [0, 0.25],
           '1': [-0.55, 0.25],
           '2': [-0.55, -0.4],
           '3': [0.2, -0.5],
           '4': [0.45, 0],
           '5': [-0.15, -0.0775903]}
    path = ''

    if flag == 'multi':
        G = create_multigraph_struct(graph)
        snapshot_name = "pictures/initial.png"
    else:
        G = create_graph_struct(path_arr, graph)
        snapshot_name = f"pictures/{i}.png"
        path = f'{str(path_arr[0])}-{str(path_arr[1])}-' \
               f'{str(path_arr[2])}-{str(path_arr[3])}-' \
               f'{str(path_arr[4])}-{str(path_arr[5])}'

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='green', alpha=0.6)
    # edges
    nx.draw_networkx_edges(G, pos, width=2)
    # node labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family="sans-serif")
    if flag == "basic":
        # edge weight labels
        edge_labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos, edge_labels)
        plt.title(f'Номер итерации: {i}')
        plt.text(0.7, 0, f'Путь: {path}')
        plt.text(0.7, -0.07, f'Длина пути: {path_len}')
        plt.text(0.7, -0.14, f'Прибавка к феромонам: {tao}')
    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(snapshot_name, dpi=65, bbox_inches='tight')
    plt.close()


def draw_graph(data, best_paths, graph):
    """Визуализация графов"""
    flag = 'multi'
    make_plt(flag, [], graph, 0, 0, 0)

    # рисуем стадии работы цикла
    for i in range(len(data)):
        flag = 'basic'
        make_plt(flag, data[i][1][1], graph, data[i][0], data[i][1][0], round(data[i][2], 3))


def check_edges(path, graph):
    """Проверяет является ли путь гамильтоновым циклом"""
    leng = -1
    for i in range(len(path)):
        if i == len(path)-1:
            if graph[path[i]][path[0]] == 0:
                return False, leng
            else:
                leng += graph[path[i]][path[0]]
        else:
            if graph[path[i]][path[i+1]] == 0:
                return False, leng
            else:
                leng += graph[path[i]][path[i+1]]
    return True, leng


def count_sum_v(v, graph, feromon, a, b):
    """Считает сумму длин ребер, выходящих из заданной вершины"""
    summ = 0
    for i in range(len(graph[v])):
        if graph[v][i] != 0:
            Lvk = graph[v][i]
            nvk = 1/Lvk
            summ += math.pow(nvk, b) * math.pow(feromon[v][i], a)
    return summ


def search_v(path):
    list = [0, 1, 2, 3, 4, 5]
    for el in path:
        list.remove(el)
    return list[0]


def calculate_path(graph, feromon, a, b, v):
    """Создает путь"""
    # случайно выбираем вершину
    #v = random.randint(0, len(graph)-1)
    path = [0, [v]]
    summ = count_sum_v(v, graph, feromon, a, b)

    # шаг для одной i-той вершины
    for i in range(len(graph) - 1):
        # считаем долю вероятности пойти в конкретную вершину из 100%
        sum_p = 0
        p_arr = []
        for i in range(len(graph[v])):
            if graph[v][i] != 0 and i not in path[1]:
                Lij = graph[v][i]
                nij = 1 / Lij
                p = 100 * (math.pow(nij, b) * math.pow(feromon[v][i], a) / summ)
                sum_p += p
                p_arr.append([sum_p, i])

        if len(p_arr) == 1:
            next_v = p_arr[0][1]
        elif len(path[1]) == 5:
            next_v = search_v(path[1])
        else:
            # выбираем следующую вершину
            rand_num = random.randint(0, 100)
            next_v = -1
            for i in range(len(p_arr)):
                if i + 1 >= len(p_arr):
                    next_v = p_arr[i][1]
                    break
                else:
                    next_v = sum([1, 2, 3, 4, 5]) - sum(path[1])
                    if rand_num >= p_arr[i][0]:
                        if rand_num < p_arr[i + 1][0]:
                            next_v = p_arr[i][1]
                            break
        # добавляем ее в путь
        path[0] += graph[v][next_v]
        path[1].append(next_v)

        v = next_v
        summ = count_sum_v(v, graph, feromon, a, b)

    return path


def ant_algorithm(graph, a, b, p, iters):
    data_for_pics = []
    min_l = 10000

    # заполняем матрицу феромонов
    feromon = [[1 for _ in range(len(graph))] for arr in range(len(graph))]
    for i in range(len(graph)):
        for j in range(len(graph)):
            if graph[i][j] == 0:
                feromon[i][j] = 0

    # итерации алгоритма
    for j in range(iters):
        # считаем путь
        v = random.randint(0, len(graph) - 1)
        path = calculate_path(graph, feromon, a, b, v)
        # проверяем является ли он гамильтоновым циклом
        booll, leng = check_edges(path[1], graph)

        if booll:
            # обновляем матрицу феромонов
            tao = 15 / path[0]
            for i in range(len(path[1])):
                if i+1 >= len(path[1]):
                    feromon[path[1][i]][path[1][0]] = feromon[path[1][i]][path[1][0]] * (1 - p) + tao
                else:
                    feromon[path[1][i]][path[1][i+1]] = feromon[path[1][i]][path[1][i+1]]*(1-p) + tao
            data_for_pics.append([j, path, tao])
            if path[0] < min_l:
                min_l = path[0]

    best_paths = []
    for el in data_for_pics:
        print(el)
        if el[1][0] == min_l and el[1] not in best_paths:
            best_paths.append(el)

    print()
    for el in best_paths:
        print(el)

    draw_graph(data_for_pics, best_paths, graph)
    return data_for_pics, min_l, best_paths


graph = [[0, 3, 0, 0, 1, 0],
         [3, 0, 8, 0, 0, 3],
         [0, 3, 0, 1, 0, 1],
         [0, 0, 8, 0, 1, 0],
         [3, 0, 0, 3, 0, 0],
         [3, 3, 3, 5, 4, 0]]

a = 0.5
b = 0.5
q = 15
p = 0.3

#ant_algorithm(graph, a, b, q, p)