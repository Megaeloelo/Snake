from time import time
import pygame
import pygame_menu
from enum import Enum
import random
import time

class Direction(Enum):
    NONE=0
    UP=1
    DOWN=2
    LEFT=3
    RIGHT=4

class Color(Enum):
    RED = pygame.Color(255, 0, 0)
    GREEN = pygame.Color(0, 255, 0)
    BLUE = pygame.Color(0, 0, 255)
    BLACK = pygame.Color(0, 0, 0)
    WHITE = pygame.Color(255, 255, 255)
    YELLOW = pygame.Color(255, 255, 0)
    CYAN = pygame.Color(0, 255, 255)
    MAGENTA = pygame.Color(255, 0, 255)

AVAILABLE_COLORS = [
    ("Red", Color.RED),
    ("Green", Color.GREEN),
    ("Blue", Color.BLUE),
    ("Black", Color.BLACK),
    ("White", Color.WHITE),
    ("Yellow", Color.YELLOW),
    ("Cyan", Color.CYAN),
    ("Magenta", Color.MAGENTA)
]

SNAKE_HEAD_COLOR = Color.GREEN
SNAKE_TAIL_COLOR = Color.GREEN
FRUIT_COLOR = Color.RED

class Entity:
    def __init__(self, game_window:pygame.Surface, color:Color, position:list[int]) -> None:
        self.game_window = game_window
        self.color = color
        self.position = position
    
    def collides(self, position) -> bool:
        if self.position[0] == position[0] and self.position[1] == position[1]:
            return True
        return False

    def draw(self) -> None:
        rect = pygame.Rect(self.position[0], self.position[1], 20, 20)
        pygame.draw.rect(self.game_window, self.color.value, rect)

class Snake(Entity):
    def __init__(self, game_window:pygame.Surface) -> None:
        window_size = game_window.get_size()
        super().__init__(game_window, SNAKE_HEAD_COLOR, [window_size[0]//2, window_size[1]//2])

        self.current_direction = Direction.NONE
        self.tail_color = SNAKE_TAIL_COLOR
        self.tail = []
        self.tail_length = 0

    def change_direction(self, direction:Direction) -> None:
        self.current_direction = direction

    def get_direction(self) -> Direction:
        return self.current_direction
    
    def get_tail_positions(self) -> list[list[int]]:
        return self.tail

    def move(self) -> None:
        self.tail.insert(0, self.position.copy())
        if self.current_direction == Direction.UP:
            self.position[1] -= 20
        elif self.current_direction == Direction.DOWN:
            self.position[1] += 20
        elif self.current_direction == Direction.LEFT:
            self.position[0] -= 20
        elif self.current_direction == Direction.RIGHT:
            self.position[0] += 20
        
        if len(self.tail) > self.tail_length:
            self.tail.pop()

    def grow(self) -> None:
        self.tail.append(self.position.copy())
        self.tail_length+=1
        pass

    def draw(self) -> None:
        super().draw()
        for pos in self.tail:
            rect = pygame.Rect(pos[0], pos[1], 20, 20)
            pygame.draw.rect(self.game_window, self.tail_color.value, rect)

class Fruit(Entity):
    def __init__(self, game_window:pygame.Surface) -> None:
        window_size = game_window.get_size()
        position = [random.randrange(1, window_size[0]//20) * 20,
                    random.randrange(1, window_size[1]//20) * 20]
        
        super().__init__(game_window, FRUIT_COLOR, position)

def show_score(game_window:pygame.Surface, score:int):
    score_font = pygame.font.SysFont("times new roman", 20)
    score_surface = score_font.render(f"Score: {score}", True, Color.WHITE.value)

    game_window.blit(score_surface, score_surface.get_rect())
 

def game_over(game_window:pygame.Surface, score:int):
    my_font = pygame.font.SysFont("times new roman", 50)
    game_over_surface = my_font.render(f"Final score: {score}", True, Color.RED.value)
    game_over_rect = game_over_surface.get_rect()
    window_size = game_window.get_size()
    game_over_rect.midtop = (window_size[0]/2, window_size[1]/4)
     
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    
    time.sleep(5)
    pygame.quit()
    quit()

def start_the_game(game_window:pygame.Surface):
    window_size = game_window.get_size()
    fps = pygame.time.Clock()
    snake = Snake(game_window)
    fruit = Fruit(game_window)
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.get_direction() != Direction.DOWN:
                    snake.change_direction(Direction.UP)
                elif event.key == pygame.K_DOWN and snake.get_direction() != Direction.UP:
                    snake.change_direction(Direction.DOWN)
                elif event.key == pygame.K_LEFT and snake.get_direction() != Direction.RIGHT:
                    snake.change_direction(Direction.LEFT)
                elif event.key == pygame.K_RIGHT and snake.get_direction() != Direction.LEFT:
                    snake.change_direction(Direction.RIGHT)
        
        snake.move()

        for pos in snake.get_tail_positions():
            if snake.collides(pos):
                game_over(game_window, score)

        if snake.collides(fruit.position):
            score+=10
            fruit = Fruit(game_window)
            snake.grow()

        if snake.position[0] < 0 or snake.position[0] > window_size[0]-20:
            game_over(game_window, score)

        if snake.position[1] < 0 or snake.position[1] > window_size[1]-20:
            game_over(game_window, score)
        
        game_window.fill(Color.BLACK.value)
        snake.draw()
        fruit.draw()
        show_score(game_window, score)

        pygame.display.update()

        fps.tick(6)

def change_snake_head_color(value, color:Color):
    global SNAKE_HEAD_COLOR
    SNAKE_HEAD_COLOR = color

def change_snake_tail_color(value, color:Color):
    global SNAKE_TAIL_COLOR
    SNAKE_TAIL_COLOR = color

def change_fruit_color(value, color:Color):
    global FRUIT_COLOR
    FRUIT_COLOR = color

def main():
    pygame.init()
    pygame.display.set_caption("Snake")
    game_window = pygame.display.set_mode((400, 400))

    options = pygame_menu.Menu("Options", 400, 400, theme=pygame_menu.themes.THEME_BLUE)
    options.add.selector("Snake head color", AVAILABLE_COLORS, 1, onchange=change_snake_head_color)
    options.add.selector("Snake tail color", AVAILABLE_COLORS, 1, onchange=change_snake_tail_color)
    options.add.selector("Fruit color", AVAILABLE_COLORS, 0, onchange=change_fruit_color)

    menu = pygame_menu.Menu("Snake", 400, 400, theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button("Play", start_the_game, (game_window))
    menu.add.button(options.get_title(), options)
    menu.add.button("Quit", pygame_menu.events.EXIT)

    menu.mainloop(game_window)

if __name__ == "__main__":
    main()