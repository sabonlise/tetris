import pygame
import os
import subprocess


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

        button_solo.draw(window)
        button_duo.draw(window)
        button_duo_time.draw(window)

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
                    subprocess.Popen(['solo.py'], shell=True, creationflags=subprocess.SW_HIDE)

                elif button_duo.is_clicked(pos):
                    subprocess.Popen(['duo_classic.py'], shell=True, creationflags=subprocess.SW_HIDE)

                elif button_duo_time.is_clicked(pos):
                    subprocess.Popen(['duo_time.py'], shell=True, creationflags=subprocess.SW_HIDE)

            if event.type == pygame.MOUSEMOTION:
                if button_solo.is_clicked(pos):
                    button_solo.color = (170, 255, 0)
                else:
                    button_solo.color = (0, 255, 0)
                    if button_duo.is_clicked(pos):
                        button_duo.color = (0, 229, 238)
                    else:
                        button_duo.color = (0, 0, 255)
                        if button_duo_time.is_clicked(pos):
                            button_duo_time.color = (0, 229, 238)
                        else:
                            button_duo_time.color = (0, 0, 255)

    pygame.display.quit()


button_solo = Button((0, 255, 0), 290, 315, 200, 50, 'Solo')
button_duo = Button((0, 0, 255), 425, 400, 200, 50, 'Duo classic')
button_duo_time = Button((0, 0, 255), 170, 400, 200, 50, 'Duo time')
pygame.font.init()

s_width, s_height = 800, 700
play_width, play_height = 300, 600

top_left_x = (s_width - play_width) // 2  # верхняя левая координата X
top_left_y = s_height - play_height       # верхняя левая координата Y

window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Тетрис')
main_menu(window)
