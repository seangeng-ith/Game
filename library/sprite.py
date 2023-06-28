from random import randint
from .constant import WINDOW_HEIGHT, WINDOW_WIDTH


class Generate_sprite:

    def __init__(self, dictionary, img):
        self._dict = dictionary
        self._img  = img


class MakeEnemy(Generate_sprite):
    
    def __init__(self, emtpy_dictionary=None, enemy_img=None):
        super().__init__(emtpy_dictionary, enemy_img)
        self._dict = emtpy_dictionary
        self._img  = enemy_img
    
    def create_enemy_data(self, count):
        for i in range(count):
            key = f"enemy_{i+1}"
            rand_y = randint(100, WINDOW_HEIGHT-150)
            rand_x = randint(100, WINDOW_WIDTH-150)

            vol_x = randint(1,5)
            vol_y = randint(1,5)

            self._dict[key] = {
                "position": [rand_x, rand_y],
                "volocity": [vol_x, vol_y],
                "img": self._img
            }


