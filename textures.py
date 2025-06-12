import pygame
import os

from constants import *

class TextureManager:
    def __init__(self):
        self.textures = {}
        self.load_all_textures("images")
        
    def load_all_textures(self, folder_path):
        """Автоматически загружает все изображения из указанной папки"""
        if not os.path.exists(folder_path):
            raise FileNotFoundError(f"Папка с текстурами '{folder_path}' не найдена")

        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
                texture_name = os.path.splitext(filename)[0]  # Имя файла без расширения
                texture_path = os.path.join(folder_path, filename)
                self.load_texture(texture_name, texture_path)

    def load_texture(self, name, path):
        """Загружает текстуру и сохраняет её в словаре"""
        try:
            texture = pygame.image.load(path).convert_alpha()
            # Масштабируем под размер клетки, если нужно
            texture = pygame.transform.scale(texture, (GRID_SIZE, GRID_SIZE))
            self.textures[name] = texture
            return True
        except pygame.error as e:
            print(f"Не удалось загрузить текстуру {path}: {e}")
            return False

