import random
from random import randint, choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Центр экрана (исправлено: порядок координат (x, y) -> (ширина, высота))
CENTER_OF_SCREEN = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет листика
LEAF_COLOR = (0, 128, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self, position=None, body_color=None):
        if position is None:
            position = CENTER_OF_SCREEN
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовывает объекты на экране."""
        raise NotImplementedError(
            f"Метод draw должен быть реализован в {self.__class__.__name__}"
        )

    def draw_rect(self, position, color, border_color=BORDER_COLOR):
        """Отрисовывает прямоугольник."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, border_color, rect, 1)


class Apple(GameObject):
    """Класс для яблока в игре 'Змейка'."""

    def __init__(self, snake_positions=None):
        super().__init__()
        self.body_color = APPLE_COLOR
        if snake_positions is None:
            snake_positions = []
        self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """Определяет случайную позицию для яблока на игровом поле."""
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in snake_positions:
                self.position = new_position
                break

    def draw(self):
        """Отрисовывает яблоко и лист на экране."""
        self.draw_rect(self.position, self.body_color)
        # Отрисовка листа
        leaf_position = (self.position[0] + 10, self.position[1] + 1)
        leaf_size = (GRID_SIZE // 4, GRID_SIZE // 2)
        leaf_rect = pygame.Rect(leaf_position, leaf_size)
        pygame.draw.ellipse(screen, LEAF_COLOR, leaf_rect)


class Snake(GameObject):
    """Класс, представляющий змейку в игре."""

    def __init__(self):
        super().__init__(position=CENTER_OF_SCREEN, body_color=SNAKE_COLOR)
        self.length = 1
        self.positions = [CENTER_OF_SCREEN]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку на один сегмент в текущем направлении."""
        cur_head = self.get_head_position()
        x, y = cur_head

        # Определяем новую позицию головы в зависимости от направления
        if self.direction == UP:
            new_head = (x, (y - GRID_SIZE) % SCREEN_HEIGHT)
        elif self.direction == DOWN:
            new_head = (x, (y + GRID_SIZE) % SCREEN_HEIGHT)
        elif self.direction == LEFT:
            new_head = ((x - GRID_SIZE) % SCREEN_WIDTH, y)
        elif self.direction == RIGHT:
            new_head = ((x + GRID_SIZE) % SCREEN_WIDTH, y)

        # Вставляем новую позицию головы в начало списка
        self.positions.insert(0, new_head)

        # Удаляем последний элемент, если змейка не выросла
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [CENTER_OF_SCREEN]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        # Очищаем экран
        screen.fill(BOARD_BACKGROUND_COLOR)

    def draw(self):
        """Отрисовывает змейку на экране."""
        # Отрисовка всех сегментов кроме последнего
        for position in self.positions[:-1]:
            self.draw_rect(position, self.body_color)

        # Отрисовка головы змейки
        if self.positions:
            self.draw_rect(self.positions[0], self.body_color)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция, инициализирующая игру и управляющая игровым циклом."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)

        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка столкновения с собой
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == '__main__':
    main()
