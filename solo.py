import pygame
import random
import os


pygame.font.init()
pygame.init()

# инициализация звука

line_sound = pygame.mixer.Sound('data/line.wav')
game_over = pygame.mixer.Sound('data/gameover.wav')

game_over.set_volume(0.1)
line_sound.set_volume(0.1)

# Глобальные переменные
s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30

top_left_x = (s_width - play_width) // 2  # верхняя левая координата X
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

    surface.blit(label, (160, 300))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128),
                         (sx, sy + i * block_size),
                         (sx + play_width, sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface, (128, 128, 128),
                             (sx + j * block_size, sy),
                             (sx + j * block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid) - 1, -1, -1):
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
                new_key = (x, y + inc)
                locked[new_key] = locked.pop(key)

    return inc


def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Следующая фигура', 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height // 2 - 100
    formatted = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(formatted):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color,
                                 (sx + j * block_size,
                                  sy + i * block_size,
                                  block_size, block_size), 0)

    surface.blit(label, (sx - 20, sy - 30))


def update_score(new_score):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > new_score:
            f.write(str(score))
        else:
            f.write(str(new_score))


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score=0, last_score=0):

    try:
        fon = pygame.transform.scale(load_image('back.jpg'), (s_width, s_height))
        surface.blit(fon, (0, 0))

        pygame.font.init()
        font = pygame.font.SysFont('comicsans', 60)
        label = font.render('Тетрис', 1, (255, 255, 255))

        surface.blit(label, (top_left_x + play_width // 2 - (label.get_width() // 2), 30))
        # текущий счёт
        font = pygame.font.SysFont('comicsans', 30)
        label = font.render('Текущий счёт: ' + str(score), 1, (255, 255, 255))

        surface.blit(label, (20, 100))
        # последний наивысший счёт
        label = font.render('Рекорд: ' + str(last_score), 1, (255, 255, 255))
    except pygame.error:
        pass

    surface.blit(label, (20, 150))
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j * block_size,
                                                   top_left_y + i * block_size,
                                                   block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)


def main(window):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    fall_time = 0
    level_time = 0
    score = 0
    fall_speed = 0.27
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time // 1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        if fall_time // 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            else:
                keys = pygame.key.get_pressed()
                if current_piece.y > 1:
                    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                        current_piece.x -= 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.x += 1
                    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                        current_piece.x += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.x -= 1
                    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                        current_piece.y += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.y -= 1
                    elif keys[pygame.K_UP] or keys[pygame.K_w]:
                        current_piece.rotation += 1
                        if not (valid_space(current_piece, grid)):
                            current_piece.rotation -= 1

        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(window, grid, score, int(last_score))
        draw_next_shape(next_piece, window)
        pygame.display.update()
        # проверка поражения
        if check_lost(locked_positions):
            gameover = pygame.transform.scale(load_image('game_over.jpg'), (s_width, s_height))
            window.blit(gameover, (0, 0))
            pygame.mixer.Sound.play(game_over)
            pygame.mixer.music.stop()
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


def main_menu(window):
    run = True
    pygame.mixer.music.load('data/tetris_theme.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
    fon = pygame.transform.scale(load_image('fon.jpg'), (s_width, s_height))
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
