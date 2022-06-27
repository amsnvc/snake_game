import pygame
import time
import random
from pygame.locals import *

block_size = 40
background_color = (0, 0, 0)


class Snake:
    def __init__(self, screen, length):
        self.screen = screen
        self.body = pygame.image.load("block.png").convert()
        self.length = length
        self.body_x = [block_size]*length
        self.body_y = [block_size]*length
        self.direction = ''

    def draw(self):
        self.screen.fill(background_color)
        for i in range(self.length):
            self.screen.blit(self.body, (self.body_x[i], self.body_y[i]))
        pygame.display.flip()

    def add_body(self):
        self.length += 1
        self.body_x.append(-1)
        self.body_y.append(-1)

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.body_x[i] = self.body_x[i-1]
            self.body_y[i] = self.body_y[i-1]

        if self.direction == 'up':
            self.body_y[0] -= block_size

        if self.direction == 'down':
            self.body_y[0] += block_size

        if self.direction == 'left':
            self.body_x[0] -= block_size

        if self.direction == 'right':
            self.body_x[0] += block_size
        self.draw()

    def move_left(self):
        if self.direction != 'right':
            self.direction = 'left'

    def move_right(self):
        if self.direction != 'left':
            self.direction = 'right'

    def move_up(self):
        if self.direction != 'down':
            self.direction = 'up'

    def move_down(self):
        if self.direction != 'up':
            self.direction = 'down'


class Food:
    def __init__(self, screen):
        self.image = pygame.image.load("apple.png").convert()
        self.screen = screen
        self.x = random.randint(1, 23) * block_size
        self.y = random.randint(1, 11) * block_size

    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1, 23) * block_size
        self.y = random.randint(1, 11) * block_size


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((1000, 500))
        self.snake = Snake(self.surface, 1)
        self.snake.add_body()
        self.food = Food(self.surface)
        self.food.draw()

    def collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + block_size:
            if y2 <= y1 < y2 + block_size:
                return True
        return False

    def playing(self):
        self.snake.walk()
        self.food.draw()
        self.score()
        pygame.display.flip()

        if self.collision(self.snake.body_x[0], self.snake.body_y[0], self.food.x, self.food.y):
            self.snake.add_body()
            self.food.move()

        for i in range(1, self.snake.length):
            if self.collision(self.snake.body_x[0], self.snake.body_y[0], self.snake.body_x[i], self.snake.body_y[i]):
                raise "Game Over"

    def score(self):
        font = pygame.font.SysFont('Helvetica', 30)
        score = font.render(f"Score: {self.snake.length-1}", True, (255, 255, 255))
        self.surface.blit(score, (450, 0))

    def game_over(self):
        self.surface.fill(background_color)
        font = pygame.font.SysFont('Helvetica', 30)
        end_score = font.render(f"Game Over! Your score:{self.snake.length}", True, (255, 0, 0))
        self.surface.blit(end_score, (320, 200))
        new_game = font.render(f"To play again, hit Space", True, (255, 0, 0))
        self.surface.blit(new_game, (320, 250))
        exit_game = font.render(f"To exit, press Escape ", True, (255, 0, 0))
        self.surface.blit(exit_game, (320, 300))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.food = Food(self.surface)

    def run(self):
        running = True
        game_over = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_SPACE:
                        game_over = False
                    if not game_over:
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                elif event.type == QUIT:
                    running = False

            try:
                if not game_over:
                    self.playing()
            except Exception as e:
                self.game_over()
                game_over = True
                self.reset()
            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
