import pygame
import os


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width // 2 - (label.get_width() // 2),
                         top_left_y + play_height // 2 - label.get_height() // 2))


def main_menu(window):
    run = True
    while run:
        window.fill((0, 0, 0))
        draw_text_middle(window, '1 - one player; 2 - two players'
                         , 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN\
                and (event.key == pygame.K_1 or event.key == pygame.K_KP1):
                os.startfile(r'solo.py')
                run = False
            if event.type == pygame.KEYDOWN\
                and (event.key == pygame.K_2 or event.key == pygame.K_KP2):
                os.startfile(r'duo.py')
                run = False
    pygame.display.quit()



pygame.font.init()
s_width, s_height = 800, 700
play_width = 300
play_height = 600
top_left_x = (s_width - play_width) // 2  # верхняя левая координата X
top_left_y = s_height - play_height       # верхняя левая координата Y
window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Тетрис')
main_menu(window)
