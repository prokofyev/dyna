from constants import * 

def get_grid_pos(x, y):
    return x // GRID_SIZE, y // GRID_SIZE

def change_color(image, old_color, new_color, threshold=30):
    """Заменяет old_color на new_color в image с учетом порога threshold."""
    surf = image.copy()
    w, h = surf.get_size()
    for x in range(w):
        for y in range(h):
            pixel = surf.get_at((x, y))
            # Проверяем, близок ли цвет к old_color (с учетом порога)
            if all(abs(pixel[i] - old_color[i]) < threshold for i in range(3)):
                new_pixel = new_color[:3]  # Берем RGB (игнорируем альфа, если есть)
                if len(pixel) == 4:  # Если есть альфа-канал
                    new_pixel = (*new_color[:3], pixel[3])
                surf.set_at((x, y), new_pixel)
    return surf

