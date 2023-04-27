import PySimpleGUI as psg
from random import randint
import algorithm

MAX_ROWS, MAX_COLS, COL_HEADINGS = 6, 6, ('    ', '0', '1', '2', '3', '4', '5')

layout = [[psg.Text('Введите коэффициент a (0, 1)', font='Default 12'), psg.InputText(key='a', justification='r')]] + \
         [[psg.Text('Введите коэффициент b (0, 1)', font='Default 12'), psg.InputText(key='b', justification='r')]] + \
         [[psg.Text('Введите коэффициент p (0, 1)', font='Default 12'), psg.InputText(key='p', justification='r')]] + \
         [[psg.Text('Введите количество итераций', font='Default 12'), psg.InputText(key='iters', justification='r')]] + \
         [[psg.Text('Введите веса в матрицу смежности', font='Default 12')]] + \
         [[psg.Text(s, key=s, enable_events=True, font='Courier 14', size=(5, 1)) for i, s in enumerate(COL_HEADINGS)]] + \
         [[psg.T(r, size=(4, 1))] + [psg.Input(randint(0, 10), justification='r', key=(r, c), disabled=False) for c in range(MAX_COLS)] for r in range(MAX_ROWS)] + \
         [[psg.Button('Рассчитать')]] + \
         [[psg.Text('Исходный граф', font='Default 12', visible=False, key='t1')]] + \
         [[psg.Image('pictures/initial.png', key='init_img', visible=False, size=(10, 10))] +
          [psg.Image('pictures/0.png', key='i_img', visible=False, size=(10, 10))]] + \
         [[psg.Button('Назад', visible=False, key='back_but'), psg.Button('Далее', visible=False, key='next_but')]] + \
         [[psg.Text('Кратчайший гамильтонов цикл', font='Default 12', visible=False, key='t2')]]

n = 0
data = []
max_n = len(data) - 1
a = -1.0
b = -1.0
p = -1.0
pics = []

window = psg.Window('Муравьиный алгоритм', layout, size=(900, 750), default_element_size=(8, 1), element_padding=(1, 1), return_keyboard_events=True)
while True:
    event, values = window.read()
    print(event, values)
    if event in (None, 'Exit'):
        break

    if event == 'Рассчитать':
        best_iters = []
        pics = []
        # по диагонали ставим нули и запрещаем пользователю ввод
        for i in range(MAX_ROWS):
            for j in range(MAX_COLS):
                if i == j:
                    window[(i, j)].update(0, disabled=True)

        # считываем таблицу смежности с GUI
        graph = [[int(values[(row, col)]) for col in range(MAX_COLS)] for row in range(MAX_ROWS)]
        a = float(values['a'])
        b = float(values['b'])
        p = float(values['p'])
        iters = int(values['iters'])

        # запускаем алгоритм
        data, min_l, best_paths = algorithm.ant_algorithm(graph, a, b, p, iters)

        for el in data:
            pics.append(el[0])

        for el in best_paths:
            best_iters.append(el[0])

        max_n = len(pics) - 1

        # отображаем результаты
        window['t1'].update(f'Исходный граф                                                                             Текущий гамильтонов цикл',
                            visible=True)
        window['init_img'].update('pictures/initial.png', visible=True)
        window['i_img'].update('pictures/0.png', visible=True)
        window['t2'].update(f'Длина кратчайшего гамильтонового цикла: {min_l}. Найдены на итерациях {best_iters}', visible=True)
        if max_n > 0:
            window['back_but'].update(visible=True, disabled=True)
            window['next_but'].update(visible=True, disabled=False)

    # логика кнопки "Назад"
    if event == 'back_but':
        n -= 1
        window['i_img'].update(f'pictures/{pics[n]}.png')
        window['next_but'].update(disabled=False)
        if n == 0:
            window['back_but'].update(disabled=True)

    # логика кнопки "Далее"
    if event == 'next_but':
        n += 1
        window['i_img'].update(f'pictures/{pics[n]}.png')
        window['back_but'].update(disabled=False)
        if n == max_n:
            window['next_but'].update(disabled=True)

window.close()