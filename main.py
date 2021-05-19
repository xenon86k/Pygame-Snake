import pygame
import sys
import random
from pygame.math import Vector2


class SNAKE:

    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.add_block = False

        self.head = None
        self.tail = None

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.add_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.add_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)


class FRUIT:
    def __init__(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.is_start_phase = True
        self.is_start_phase2 = True
        self.score = 0
        with open("high_score.txt", "r") as file:
            self.high_score = int(file.readline())
        self.is_game_over = False
        self.game_over_sound = pygame.mixer.Sound("Sound/sfx_hit.wav")

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        if self.is_start_phase:
            self.draw_grass()
            self.game_start()
        elif self.is_game_over:
            self.game_over_screen()
        elif not self.is_start_phase:
            self.draw_grass()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block = True
            self.snake.crunch_sound.play()

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
            if not self.is_start_phase2:
                self.is_game_over = True
                self.game_over_sound.play()
                self.is_start_phase2 = True

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
                if not self.is_start_phase2:
                    self.is_game_over = True
                    self.game_over_sound.play()
                    self.is_start_phase2 = True

    def game_over(self):
        self.snake.reset()

    @staticmethod
    def draw_grass():
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        self.score = len(self.snake.body) - 3
        self.update_high_score()
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def game_start(self):
        welcome_text_surface = game_font_welcome.render("WELCOME TO PYGAME - SNAKE!", True, (0, 0, 0))
        welcome_text_rect = welcome_text_surface.get_rect(center=(10 * cell_size, 2 * cell_size))

        # Icon made by "https://www.freepik.com" from "https://www.flaticon.com/"
        snake_surface = pygame.transform.scale(pygame.image.load("Graphics/snake.png").convert_alpha(), (128, 128))
        snake_rect = snake_surface.get_rect(center=(8 * cell_size, 6 * cell_size))

        # Icon made by "https://www.freepik.com" from "https://www.flaticon.com/"
        python_surface = pygame.transform.scale(pygame.image.load("Graphics/python.png").convert_alpha(), (128, 128))
        python_rect = python_surface.get_rect(center=(12 * cell_size, 6 * cell_size))

        high_score_text_surface = game_font_start.render(f"High Score: {self.high_score}", True, (0, 0, 0))
        high_score_rect = high_score_text_surface.get_rect(center=(10 * cell_size, 10 * cell_size))

        start_text_surface = game_font_start.render("PRESS 'SPACE' TO START", True, (0, 0, 0))
        start_text_rect = start_text_surface.get_rect(center=(10 * cell_size, 12 * cell_size))

        # Icon made by "https://www.freepik.com" from "https://www.flaticon.com/"
        start_surface = pygame.transform.scale(pygame.image.load("Graphics/start.png").convert_alpha(), (128, 128))
        start_rect = start_surface.get_rect(center=(10 * cell_size, 14 * cell_size))

        play_text_surface = game_font_play.render("Use ARROW/WASD To Play", True, (0, 0, 0))
        play_text_rect = play_text_surface.get_rect(center=(10 * cell_size, 18 * cell_size))

        screen.blit(welcome_text_surface, welcome_text_rect)
        screen.blit(snake_surface, snake_rect)
        screen.blit(python_surface, python_rect)
        screen.blit(high_score_text_surface, high_score_rect)
        screen.blit(start_text_surface, start_text_rect)
        screen.blit(start_surface, start_rect)
        screen.blit(play_text_surface, play_text_rect)

    def game_over_screen(self):
        # Icon made by "https://www.flaticon.com/authors/good-ware" from "https://www.flaticon.com/"
        game_over_surface = pygame.transform.scale(pygame.image.load("Graphics/game-over.png").convert_alpha(),
                                                   (384, 384))
        game_over_rect = game_over_surface.get_rect(center=(10 * cell_size, 6 * cell_size))

        score_text = game_font_play.render(f"Your Score: {str(self.score)}", True, (0, 0, 0))
        score_text_rect = score_text.get_rect(center=(10 * cell_size, 12 * cell_size))

        high_score_text = game_font_play.render(f"High Score: {str(self.high_score)}", True, (0, 0, 0))
        high_score_text_rect = high_score_text.get_rect(center=(10 * cell_size, 13 * cell_size))

        play_again_text = game_font_start.render("PRESS 'P' TO PLAY AGAIN", True, (0, 0, 0))
        play_again_text_rect = play_again_text.get_rect(center=(10 * cell_size, 15 * cell_size))

        screen.blit(game_over_surface, game_over_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(high_score_text, high_score_text_rect)
        screen.blit(play_again_text, play_again_text_rect)

    def update_high_score(self):
        if self.high_score < self.score:
            self.high_score = self.score
            with open("high_score.txt", "w") as file:
                file.write(str(self.score))


pygame.mixer.pre_init()
pygame.init()
pygame.display.set_caption("PYGAME - SNAKE")

cell_size = 40
cell_number = 20

screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

# Decrease speed move snake faster or increase to move snake slower
speed = 150
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, speed)

apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
game_font_start = pygame.font.Font('Font/SF Atarian System Bold.ttf', 45)
game_font_play = pygame.font.Font('Font/SF Atarian System Bold.ttf', 35)
game_font_welcome = pygame.font.Font('Font/SF Atarian System Bold.ttf', 60)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                main_game.is_start_phase = False
            if not main_game.is_start_phase and not main_game.is_game_over:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    main_game.is_start_phase2 = False
                    if main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    main_game.is_start_phase2 = False
                    if main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    main_game.is_start_phase2 = False
                    if main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    # main_game.is_start_phase2 = False
                    if main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
            if not main_game.is_start_phase and main_game.is_game_over:
                if event.key == pygame.K_p:
                    main_game.is_game_over = False

    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(120)

# Reference - https://youtu.be/QFvqStqPCRU
# Changes made:
# 1. Added game starting, over page
# 2. Added game over sound
# 3. Added highs core saving and showing functionality
# 4. Added WASD key support
