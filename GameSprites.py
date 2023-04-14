import pygame
from config import WIDTH, HEIGHT
from pygame.color import THECOLORS


class Observer:
    def correct_invoke(self, keyboard_input, index):
        pass

    def incorrect_invoke(self, keyboard_input, index):
        pass


def join_text_surfaces_in_one_line(list_of_surfaces):
    width = 0
    for surf in list_of_surfaces:
        width += surf.get_width()
    result_surf = pygame.Surface((width, list_of_surfaces[0].get_height()))
    result_surf.fill(THECOLORS['green'])
    width_pos = 0
    for surf in list_of_surfaces:
        result_surf.blit(surf, (width_pos, 0))
        width_pos += surf.get_width()
    result_surf.set_colorkey(THECOLORS['green'])
    return result_surf


def make_text_surf(text):
    width = 0
    height = 0
    lines = []
    for line in text:
        words = []
        width_sum = 0
        for word in line:
            if word.get_width() + width_sum > WIDTH * 9 / 10:
                line_surf = join_text_surfaces_in_one_line(words)
                lines.append(line_surf)
                height += line_surf.get_height()
                words = []
                width = max(width, width_sum)
                width_sum = 0
            words.append(word)
            width_sum += word.get_width()
        line_surf = join_text_surfaces_in_one_line(words)
        lines.append(line_surf)
        height += line_surf.get_height()
        width = max(width, width_sum)
    result_surf = pygame.Surface((width, height))
    result_surf.fill(THECOLORS['green'])
    height = 0
    for line in lines:
        result_surf.blit(line, ((width - line.get_width()) / 2, height))
        height += line.get_height()
    result_surf.set_colorkey(THECOLORS['green'])
    return result_surf


def get_word_surf(word, pyfont, color):
    return pyfont.render(word, False, color)


def color_incorrect_letter(word, index, pyfont):
    black_surf = pyfont.render(word[:index], False, THECOLORS['black'])
    red_surf = pyfont.render(word[index:index + 1], False, THECOLORS['red'])
    gray_surf = pyfont.render(word[index + 1:], False, THECOLORS['gray'])
    height = black_surf.get_height()
    width = black_surf.get_width() + red_surf.get_width() + gray_surf.get_width()
    result_surf = pygame.Surface((width, height))
    result_surf.fill(THECOLORS['green'])
    result_surf.blit(black_surf, (0, 0))
    result_surf.blit(red_surf, (black_surf.get_width(), 0))
    result_surf.blit(gray_surf, (black_surf.get_width() + red_surf.get_width(), 0))
    result_surf.set_colorkey(THECOLORS['green'])
    return result_surf


def color_correct_letter(word, index, pyfont):
    black_surf = pyfont.render(word[:index + 1], False, THECOLORS['black'])
    gray_surf = pyfont.render(word[index + 1:], False, THECOLORS['gray'])
    height = black_surf.get_height()
    width = black_surf.get_width() + gray_surf.get_width()
    result_surf = pygame.Surface((width, height))
    result_surf.fill(THECOLORS['green'])
    result_surf.blit(black_surf, (0, 0))
    result_surf.blit(gray_surf, (black_surf.get_width(), 0))
    result_surf.set_colorkey(THECOLORS['green'])
    return result_surf


class TestText(pygame.sprite.Sprite, Observer):
    def __init__(self, size, font):
        super().__init__()
        self.text = []
        self.text_surf = []
        self.font = pygame.font.SysFont(font, size)
        with open('text.txt') as text:
            self.text = [line.split() for line in text.read().split('\n')]
        for line in self.text:
            for i in range(1, len(line)):
                line.insert(i * 2 - 1, '_')
        self.text_surf = [[get_word_surf(word, self.font, THECOLORS['gray']) for word in line] for line in self.text]
        self.update_image()

    def update_image(self):
        self.image = make_text_surf(self.text_surf)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def correct_invoke(self, keyboard_input, pos):
        self.text_surf[pos.line][pos.word] = color_correct_letter(self.text[pos.line][pos.word], pos.index, self.font)
        self.update_image()

    def incorrect_invoke(self, keyboard_input, pos):
        self.text_surf[pos.line][pos.word] = color_incorrect_letter(self.text[pos.line][pos.word], pos.index, self.font)
        self.update_image()


class WpmText(pygame.sprite.Sprite):
    def __init__(self, size, color, font):
        super().__init__()
        self.font = pygame.font.SysFont(font, size)
        self.color = color
        self.text = [['Wpm: ', '0'], ['100', '%']]
        self.text_surf = [[get_word_surf(word, self.font, color) for word in line] for line in self.text]
        self.image = make_text_surf(self.text_surf)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 4)
        
    def update(self, wpm, percent):
        super().update()
        self.text[0][1] = str(wpm)
        self.text[1][0] = str(percent)
        self.text_surf[0][1] = get_word_surf(str(wpm), self.font, self.color)
        self.text_surf[1][0] = get_word_surf(str(percent), self.font, self.color)
        self.image = make_text_surf(self.text_surf)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 4)
