import pygame
import random
import os


pygame.font.init()
pygame.init()

# инициализация звука

line_sound = pygame.mixer.Sound('data/line.wav')
game_over = pygame.mixer.Sound('data/gameover.wav')
draw = pygame.mixer.Sound('data/success.wav')

game_over.set_volume(0.1)
line_sound.set_volume(0.1)
draw.set_volume(0.1)

# Глобальные переменные
s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30

top_left_x = (s_width - 2 * play_width - 60) // 2  # верхняя левая координата X
top_left_y = s_height - play_height       # верхняя левая координата Y


# Формы фигур

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    return image


def create_grid(locked_pos={}):
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j, i)]
                grid[i][j] = c

    return grid


def convert_shape_format(shape):
    positions = []

    formatted = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(formatted):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False

    return True


def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size)
    label = font.render(text, 1, color)

    surface.blit(label, (160, 325))


def draw_grid(surface, grid, num, score):
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    sx = top_left_x + num * (play_width + 100)
    sy = top_left_y
    dy = play_height
    pygame.draw.rect(surface, (255, 0, 0), (sx, top_left_y, play_width, play_height), 5)
    label = font.render('Счёт: ' + str(score), 1, (255, 255, 255))
    surface.blit(label, (sx + 70, 30))
    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (sx, sy + i * block_size), (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx + j * block_size, sy), (sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                    pygame.mixer.Sound.play(line_sound)
                except Exception:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(shape, shape2, surface):
    font = pygame.font.SysFont('comicsans', 30)
    # отрисовка следующей фигуры для первого игрока
    label = font.render('Next 1:', 1, (255, 255, 255))
    sx = top_left_x + play_width - 23
    sy = top_left_y
    formatted = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(formatted):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size,
                                  sy + 75 + i * block_size,
                                  block_size, block_size), 0)
    surface.blit(label, (sx + 40, sy + 50))
    # отрисовка следующей фигуры для второго игрока
    label = font.render('Next 2:', 1, (255, 255, 255))
    sx = top_left_x + play_width - 23
    sy = top_left_y + play_height // 2 - 100
    formatted = shape2.shape[shape.rotation % len(shape2.shape)]
    for i, line in enumerate(formatted):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape2.color,
                                 (sx + j * block_size,
                                  sy + 75 + i * block_size,
                                  block_size, block_size), 0)
    surface.blit(label, (sx + 40, sy + 50))


def draw_window(surface, grid, grid2, score, score2):
    fon = pygame.transform.scale(load_image('back.jpg'), (s_width, s_height))
    surface.blit(fon, (0, 0))
    # фигура второго игрока
    for i in range(len(grid2)):
        for j in range(len(grid2[i])):
            pygame.draw.rect(surface, grid2[i][j], (top_left_x + play_width + 100 + j * block_size,
                                                   top_left_y + i * block_size,
                                                   block_size, block_size), 0)
    # фигура первого игрока
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size,
                                                   top_left_y + i * block_size,
                                                   block_size, block_size), 0)

    draw_grid(surface, grid, 0, score)
    draw_grid(surface, grid2, 1, score2)
    #  pygame.display.update()


def main(window):
    first_lost = False
    second_lost = False
    change_piece = False
    change_piece2 = False
    run = True

    locked_positions = {}
    locked_positions2 = {}

    grid = create_grid(locked_positions)
    grid2 = create_grid(locked_positions2)

    current_piece = get_shape()
    current_piece2 = get_shape()
    next_piece = get_shape()
    next_piece2 = get_shape()
    clock = pygame.time.Clock()

    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    fall_time2 = 0
    fall_speed2 = 0.27
    level_time2 = 0
    score = 0
    score2 = 0

    while run:
        grid = create_grid(locked_positions)
        grid2 = create_grid(locked_positions2)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        fall_time2 += clock.get_rawtime()
        level_time2 += clock.get_rawtime()
        clock.tick()
        # 1 player checking for fall shape
        if level_time // 1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time // 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True
        # 2 player checking for fall shape
        if fall_time2 // 1000 > fall_speed2:
            fall_time2 = 0
            current_piece2.y += 1
            if not(valid_space(current_piece2, grid2)) and current_piece2.y > 0:
                print('qq')
                current_piece2.y -= 1
                change_piece2 = True

        if level_time2 // 1000 > 5:
            level_time2 = 0
            if level_time2 > 0.12:
                level_time2 -= 0.005
        # control and exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            else:
                keys = pygame.key.get_pressed()
                if current_piece.y > 1 and current_piece2.y > 1:
                    # управление первого игрока
                    if keys[pygame.K_a]:
                        current_piece.x -= 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.x += 1
                    elif keys[pygame.K_d]:
                        current_piece.x += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.x -= 1
                    elif keys[pygame.K_s]:
                        current_piece.y += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.y -= 1
                    elif keys[pygame.K_w]:
                        current_piece.rotation += 1
                        if not(valid_space(current_piece, grid)):
                            current_piece.rotation -= 1
                    # управление второго игрока
                    elif keys[pygame.K_UP]:
                        current_piece2.rotation += 1
                        if not (valid_space(current_piece2, grid2)):
                            current_piece2.rotation -= 1
                    elif keys[pygame.K_LEFT]:
                        current_piece2.x -= 1
                        if not(valid_space(current_piece2, grid2)):
                            current_piece2.x += 1
                    elif keys[pygame.K_DOWN]:
                        current_piece2.y += 1
                        if not(valid_space(current_piece2, grid2)):
                            current_piece2.y -= 1
                    elif keys[pygame.K_RIGHT]:
                        current_piece2.x += 1
                        if not(valid_space(current_piece2, grid2)):
                            current_piece2.x -= 1
        # 1 shape
        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece and not first_lost:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10
        # 2 shape
        shape_pos2 = convert_shape_format(current_piece2)
        for i in range(len(shape_pos2)):
            x, y = shape_pos2[i]
            if y > -1:
                grid2[y][x] = current_piece2.color

        if change_piece2 and not second_lost:
            for pos in shape_pos2:
                p2 = (pos[0], pos[1])
                locked_positions2[p2] = current_piece2.color
            current_piece2 = next_piece2
            next_piece2 = get_shape()
            change_piece2 = False
            score2 += clear_rows(grid2, locked_positions2) * 10
        # drawing
        draw_window(window, grid, grid2, score, score2)
        draw_next_shape(next_piece, next_piece2, window)
        pygame.display.update()
        # проверка поражения
        if check_lost(locked_positions):
            if second_lost:
                if score > score2:
                    window.fill((0, 0, 0))
                    draw_text_middle(window, "Первый игрок выиграл!", 80, (255, 255, 255))
                    pygame.mixer.Sound.play(game_over)
                    pygame.mixer.music.stop()
                elif score2 > score:
                    window.fill((0, 0, 0))
                    draw_text_middle(window, "Второй игрок выиграл!", 80, (255, 255, 255))
                    pygame.mixer.Sound.play(game_over)
                    pygame.mixer.music.stop()
                else:
                    window.fill((0, 0, 0))
                    draw_text_middle(window, "Ничья!", 80, (255, 255, 255))
                    pygame.mixer.Sound.play(draw)
                    pygame.mixer.music.stop()
                pygame.display.update()
                pygame.time.delay(1500)
                run = False
            else:
                first_lost = True

        '''if check_lost(locked_positions2):
            if first_lost:
                if score > score2:
                    draw_text_middle(window, "2 проиграл!", 80, (255, 255, 255))
                elif score2 > score:
                    draw_text_middle(window, "1 проиграл!", 80, (255, 255, 255))
                else:
                    draw_text_middle(window, "Ничья!", 80, (255, 255, 255))
                pygame.display.update()
                pygame.time.delay(1500)
                run = False
            else:
                second_lost = True'''


def main_menu(window):
    run = True
    fon = pygame.transform.scale(load_image('fon.jpg'), (s_width, s_height))
    pygame.mixer.music.load('data/tetris_theme.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    while run:
        window.blit(fon, (0, 0))
        draw_text_middle(window, 'Нажмите любую кнопку', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                main(window)

    pygame.display.quit()


window = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Тетрис')
main_menu(window)
