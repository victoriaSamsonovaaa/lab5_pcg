import matplotlib.pyplot as plt
import numpy as np

def draw_line(x1, y1, x2, y2, color='b'):
    plt.plot([x1, x2], [y1, y2], color)

def draw_polygon(vertices, color='r'):
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    plt.fill(x, y, color)

def compute_code(x, y, vertices):
    INSIDE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 4
    TOP = 8

    code = INSIDE
    if x < min(v[0] for v in vertices):
        code |= LEFT
    elif x > max(v[0] for v in vertices):
        code |= RIGHT
    if y < min(v[1] for v in vertices):
        code |= BOTTOM
    elif y > max(v[1] for v in vertices):
        code |= TOP
    return code

def draw_clipped_line(x1, y1, x2, y2):
    plt.plot([x1, x2], [y1, y2], 'r')

def find_intersection(x1, y1, x2, y2, code, vertices):
    slope = (y2 - y1) / (x2 - x1)
    if code & TOP:
        x = x1 + (1 / slope) * (max(v[1] for v in vertices) - y1)
        y = max(v[1] for v in vertices)
    elif code & BOTTOM:
        x = x1 + (1 / slope) * (min(v[1] for v in vertices) - y1)
        y = min(v[1] for v in vertices)
    elif code & RIGHT:
        y = y1 + slope * (max(v[0] for v in vertices) - x1)
        x = max(v[0] for v in vertices)
    elif code & LEFT:
        y = y1 + slope * (min(v[0] for v in vertices) - x1)
        x = min(v[0] for v in vertices)
    return x, y

def clip_by_polygon(x1, y1, x2, y2, vertices):
    # Инициализация кодов для обоих концов отрезка
    code1 = compute_code(x1, y1, vertices)
    code2 = compute_code(x2, y2, vertices)

    if (code1 & code2) != 0:
        return

    while (code1 | code2) != 0:
        # Выбор конца, который находится вне многоугольника
        if code1 != 0:
            code_out = code1
        else:
            code_out = code2

        # Нахождение пересечения линии с границей многоугольника
        intersection_point = find_intersection(x1, y1, x2, y2, code_out, vertices)
        if code_out == code1:
            x1, y1 = intersection_point
            code1 = compute_code(x1, y1, vertices)
        else:
            x2, y2 = intersection_point
            code2 = compute_code(x2, y2, vertices)

    # Визуализация исходного отрезка и его видимой части
    draw_line(x1, y1, x2, y2, 'g')  # Зеленый цвет для отрезков, отсеченных многоугольником

# Исходные данные
TOP = 1
BOTTOM = 2
LEFT = 4
RIGHT = 8
n = int(input("Введите количество отрезков: "))
lines = []
for i in range(n):
    line = list(map(int, input(f"Введите координаты отрезка {i + 1} (x1 y1 x2 y2): ").split()))
    lines.append(line)

polygon_vertices = list(map(int, input("Введите координаты многоугольника (x y): ").split()))

# Окно отсечения
xmin, ymin, xmax, ymax = map(int, input("Введите координаты окна отсечения (xmin ymin xmax ymax): ").split())

# Визуализация системы координат
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(0, color='black', linewidth=0.5)

# Визуализация многоугольника
draw_polygon([(polygon_vertices[i], polygon_vertices[i + 1]) for i in range(0, len(polygon_vertices), 2)])

# Визуализация отрезков
for line in lines:
    draw_line(line[0], line[1], line[2], line[3])

# Визуализация окна отсечения
plt.gca().add_patch(plt.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, linewidth=1, edgecolor='c', facecolor='none'))

# Отсечение отрезков выпуклым многоугольником
for line in lines:
    clip_by_polygon(line[0], line[1], line[2], line[3], [(polygon_vertices[i], polygon_vertices[i + 1]) for i in range(0, len(polygon_vertices), 2)])

plt.gca().set_aspect('equal', adjustable='box')
plt.show()
