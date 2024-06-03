import os

import pygame

BASE_IMG_PATH = 'data/images/'

def load_image(path):
    print("Loading Image:", path)
    try:
        img = pygame.image.load(BASE_IMG_PATH + path).convert()
        img.set_colorkey((0, 0, 0))
        return img
    except pygame.error as e: 
        print(f"loading error: {path}")
        raise SystemExit(e)


def load_images(path):
    images = []
    full_path = os.path.join(BASE_IMG_PATH, path)  # Construct absolute path
    print("Full path:", full_path)
    for img_name in sorted(os.listdir(full_path)):
        if img_name.endswith('.png') or img_name.endswith('.jpg') or img_name.endswith('.bmp'):
            images.append(load_image(os.path.join(path, img_name)))  # Use absolute path for loading image
    return images


class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0
    
    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]