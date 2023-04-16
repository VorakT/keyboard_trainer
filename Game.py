import pygame
from config import WIDTH, HEIGHT, FPS, FONT, TEST_TEXT_SIZE, DATA_TEXT_SIZE
from pygame.color import THECOLORS
from GameState import GameState
from GameSprites import TestText, WpmText
from datetime import datetime


class Game:
    def __init__(self):
        self.state = GameState()

    def run(self):
        '''
        Main function, that initializes sprites and then handles
        input using GameState
        '''
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        sprites = pygame.sprite.Group()
        text = TestText(TEST_TEXT_SIZE, FONT)
        sprites.add(text)
        self.state.add_observer(text)
        wpm_text = WpmText(DATA_TEXT_SIZE, THECOLORS['black'], FONT)
        sprites.add(wpm_text)
        running = True
        frames = 0
        self.state.start()
        while running:
            clock.tick(FPS)
            frames += 1
            if frames >= FPS / 2:
                frames = 0
                wpm_text.update(self.state.get_wpm(), self.state.get_percent())
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if not self.state.active:
                    continue
                if event.type == pygame.KEYDOWN and event.unicode != '' and event.key != pygame.K_BACKSPACE\
                        and event.key != pygame.K_ESCAPE:
                    self.state.check_correct_input(event.unicode)
                if self.state.check_text_end():
                    break
            screen.fill(THECOLORS['white'])
            sprites.draw(screen)
            pygame.display.flip()
        with open('data.txt', 'a') as f:
            f.write(datetime.today().strftime('%Y-%m-%d %H:%M:%S') + '\n')
            f.write("Words per minute: " + str(self.state.get_wpm()) + '\n')
            f.write("Percent of right presses: " + str(self.state.get_percent()) + '%\n\n')
        pygame.quit()
