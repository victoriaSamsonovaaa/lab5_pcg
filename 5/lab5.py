from os import name
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

def cohen_sutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    # Реализация алгоритма Сазерленда-Коэна
    INSIDE, LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 4, 8
    
    def compute_code(x, y):
        code = INSIDE
        if x < xmin:
            code |= LEFT
        elif x > xmax:
            code |= RIGHT
        if y < ymin:
            code |= BOTTOM
        elif y > ymax:
            code |= TOP
        return code
    
    code1 = compute_code(x1, y1)
    code2 = compute_code(x2, y2)

    while (code1 | code2) != 0:
        if (code1 & code2) != 0:
            return None, None  # отрезок полностью за пределами окна

        code = code1 if code1 != 0 else code2

        x, y = 0, 0
        if code & TOP:
            x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
            y = ymax
        elif code & BOTTOM:
            x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
            y = ymin
        elif code & RIGHT:
            y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
            x = xmax
        elif code & LEFT:
            y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
            x = xmin

        if code == code1:
            x1, y1 = x, y
            code1 = compute_code(x1, y1)
        else:
            x2, y2 = x, y
            code2 = compute_code(x2, y2)

    return (x1, y1), (x2, y2)

def cyrus_beck(x1, y1, x2, y2, vertices):
    def dot_product(v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    def clip_t(num, denom, t0, t1):
        if denom == 0:
            if num < 0:
                return None, None  # Line is inside the clip window
            else:
                return t0, t1  # Line is parallel to the clipping edge, keep as is

        t = num / denom

        if denom > 0:
            if t > t1:
                return None, None  # Line is outside the clip window
            elif t > t0:
                t0 = t
        elif denom < 0:
            if t < t0:
                return None, None  # Line is outside the clip window
            elif t < t1:
                t1 = t

        return t0, t1

    n = len(vertices)
    normals = [((vertices[(i + 1) % n][1] - vertices[i][1]),
                (vertices[i][0] - vertices[(i + 1) % n][0]))
               for i in range(n)]

    t0, t1 = 0, 1

    for i in range(n):
        p = normals[i]
        q = (vertices[i][0] - x1, vertices[i][1] - y1)

        numerator = dot_product(q, p)
        denominator = dot_product((x2 - x1, y2 - y1), p)

        t0, t1 = clip_t(numerator, denominator, t0, t1)
        if t0 is None or t1 is None:
            return None, None  # Line is outside the clip window

    x_start = x1 + t0 * (x2 - x1)
    y_start = y1 + t0 * (y2 - y1)
    x_end = x1 + t1 * (x2 - x1)
    y_end = y1 + t1 * (y2 - y1)

    return (x_start, y_start), (x_end, y_end)

def draw_polygon(ax, vertices, color):
    # Визуализация многоугольника
    polygon = Polygon(vertices, closed=True, fill=None, edgecolor=color)
    ax.add_patch(polygon)

def draw_line(ax, x1, y1, x2, y2, color):
    ax.plot([x1, x2], [y1, y2], color=color)

def main():
    filename = "input.txt"
    
    with open(filename, "r") as file:
        # Чтение числа отрезков
        n = int(file.readline().strip())

        segments = []
        for _ in range(n):
            # Чтение координат отрезков
            x1, y1, x2, y2 = map(float, file.readline().split())
            segments.append((x1, y1, x2, y2))

        # Чтение координат отсекающего прямоугольного окна
        clip_window = map(float, file.readline().split())

        # Чтение числа вершин многоугольника
        m = int(file.readline().strip())

        # Чтение координат вершин многоугольника
        polygon_vertices = [tuple(map(float, file.readline().split())) for _ in range(m)]

    # Создаем два отдельных графика с разными размерами
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    ax1.axhline(0, color='black', lw=2)
    ax1.axvline(0, color='black', lw=2)
    clip_window_list = list(clip_window)
    clip_rectangle = Rectangle((clip_window_list[0], clip_window_list[1]),
                           clip_window_list[2] - clip_window_list[0],
                           clip_window_list[3] - clip_window_list[1],
                           fill=None, edgecolor='magenta')

    ax1.add_patch(clip_rectangle)

    for segment in segments:
        x1, y1, x2, y2 = segment
        draw_line(ax1, x1, y1, x2, y2, color='red')

        clipped_start, clipped_end = cohen_sutherland(x1, y1, x2, y2, clip_window_list[0], clip_window_list[1], clip_window_list[2], clip_window_list[3])
        if clipped_start is not None and clipped_end is not None:
            draw_line(ax1, clipped_start[0], clipped_start[1], clipped_end[0], clipped_end[1], color='blue')

    ax2.axhline(0, color='black', lw=2)
    ax2.axvline(0, color='black', lw=2)

    for segment in segments:
        x1, y1, x2, y2 = segment
        draw_line(ax2, x1, y1, x2, y2, color='red')

        clipped_start, clipped_end = cyrus_beck(x1, y1, x2, y2, polygon_vertices)
        if clipped_start is not None and clipped_end is not None:
            draw_line(ax2, clipped_start[0], clipped_start[1], clipped_end[0], clipped_end[1], color='blue')

    draw_polygon(ax2, polygon_vertices, color='magenta')

    plt.show()

if __name__ == "__main__":
    main()