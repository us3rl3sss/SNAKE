#Импортируем необходимые библиотеки
import pygame as pg
from random import randrange

#Задаем параметры
window = 500
tile_size = 25
range = (tile_size // 2, window - tile_size // 2, tile_size)

get_random_position = lambda: [randrange(*range), randrange(*range)]
snake = pg.Rect(0, 0, tile_size - 2, tile_size - 2)
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 110
food = snake.copy()
food.center = get_random_position()
snake.center = get_random_position()
screen = pg.display.set_mode([window] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}

snake_image = pg.image.load('resources/truck.jpg')
snake_head_image = pg.transform.scale(snake_image, (tile_size - 2, tile_size - 2))

food_image = pg.image.load('resources/box.jpg')
food_head_image = pg.transform.scale(food_image, (tile_size - 2, tile_size - 2))

#Тело игры и запуск
while True:
  for event in pg.event.get():
      if event.type == pg.QUIT:
          exit()
      if event.type == pg.KEYDOWN:
          if event.key == pg.K_w and dirs[pg.K_w]:
              snake_dir = (0, -tile_size)
              dirs = {pg.K_w: 1, pg.K_s: 0, pg.K_a: 1, pg.K_d: 1}
          if event.key == pg.K_s and dirs[pg.K_s]:
              snake_dir = (0, tile_size)
              dirs = {pg.K_w: 0, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
          if event.key == pg.K_a and dirs[pg.K_a]:
              snake_dir = (-tile_size, 0)
              dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 0}
          if event.key == pg.K_d and dirs[pg.K_d]:
              snake_dir = (tile_size, 0)
              dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 0, pg.K_d: 1}
  screen.fill((0, 0, 0))  # Change 'black' to (0, 0, 0)
  #Проверка столкновений
  food_in_tail = any(food.colliderect(segment) for segment in segments[:-1])
  if food_in_tail:
      food.center = get_random_position()
  self_eating = snake.collidelist(segments[:-1]) != -1
  if (
      snake.left < 0
      or snake.right > window
      or snake.top < 0
      or snake.bottom > window
      or self_eating
  ):
      snake.center, food.center = get_random_position(), get_random_position()
      length, segments = 1, [snake.copy()]
      snake_dir = (0, 0)
  #Проверка взаимодействия змейки с едой
  if snake.colliderect(food):
      food.center = get_random_position()
      length += 1
  #Рисуем еду
  screen.blit(food_head_image, food)
  #Рисуем змейку
  for segment in segments:
      screen.blit(snake_head_image, segment)
  #Двигаем змейку
  time_now = pg.time.get_ticks()
  if time_now - time > time_step:
      time = time_now
      snake.move_ip(snake_dir)
      segments.append(snake.copy())
      segments = segments[-length:]
  pg.display.flip()
  clock.tick(10)