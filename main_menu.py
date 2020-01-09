import pygame
import os
import solo
import duo


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.x = x
        self.y = y
        self.color = color
        self.height = height
        self.width = width
        self.text = text

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.SysFont('comicsans', 40, bold=True)
        text = font.render(self.text, 1, (0, 0, 0))
        win.blit(text,
                 (self.x + (self.width // 2 - text.get_width() // 2),
                  self.y + (self.height // 2 - text.get_height() // 2)))

    def is_clicked(self, mouse_pos):
        if mouse_pos[0] > self.x and mouse_pos[0] < self.x + self.width and \
                mouse_pos[1] > self.y and mouse_pos[1] < self.y + self.height:
            return True
        return False


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    return image


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width // 2 - (label.get_width() // 2),
                         top_left_y + play_height // 2 - label.get_height() // 2 - 150))


def main_menu(window):
    run = True
    fon = pygame.transform.scale(load_image('fon.jpg'), (s_width, s_height))
    window.blit(fon, (0, 0))
    while run:
       # window.fill((0, 0, 0))
        button_solo.draw(window)
        button_duo.draw(window)
        draw_text_middle(window, 'Выберите режим игры',
                         60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_solo.is_clicked(pos):
                    # os.startfile(r'solo.py')
                    solo.main_menu(solo.window)
                elif button_duo.is_clicked(pos):
                    # os.startfile(r'duo.py')
                    duo.main_menu(duo.window)

            if event.type == pygame.MOUSEMOTION:
                if button_solo.is_clicked(pos):
                    button_solo.color = (170, 255, 0)
                elif button_duo.is_clicked(pos):
                    button_duo.color = (0, 229, 238)

    pygame.display.quit()


button_solo = Button((0, 255, 0), 150, 380, 200, 50, 'Соло игра')
button_duo = Button((0, 0, 255), 450, 380, 200, 50, 'Дуо игра')
pygame.font.init()
s_width, s_height = 800, 700
play_width, play_height = 300, 600
top_left_x = (s_width - play_width) // 2  # верхняя левая координата X
top_left_y = s_height - play_height       # верхняя левая координата Y
window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Тетрис')
main_menu(window)
