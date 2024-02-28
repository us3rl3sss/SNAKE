#Импортируем необходимые библиотеки
import os
from typing import Self
import pygame as pg
from random import randrange
os.chdir(os.path.dirname(os.path.abspath(__file__)))
pg.font.init()
pg.mixer.init()

#Задаем параметры
window = 500
tile_size = 50
range = (tile_size // 2, window - tile_size // 2, tile_size)

get_random_position = lambda: [randrange(*range), randrange(*range)]
snake = pg.Rect(0, 0, tile_size - 2, tile_size - 2)
length = 1
segments = [snake.copy()]
snake_dir = (0, 0)
time, time_step = 0, 250
food = snake.copy()
food.center = get_random_position()
snake.center = get_random_position()
screen = pg.display.set_mode([window] * 2)
clock = pg.time.Clock()
dirs = {pg.K_w: 1, pg.K_s: 1, pg.K_a: 1, pg.K_d: 1}
speed = 8
scoreRecord = 0

#Вывод счета
font = pg.font.Font(None, 18)
text = font.render("Your score is: 0", True, (255, 255, 255))

#Изображения
snake_image = pg.image.load('resources/truck.png')
snake_head_image = pg.transform.scale(snake_image, (tile_size - 2, tile_size - 2))

food_image = pg.image.load('resources/box.png')
food_head_image = pg.transform.scale(food_image, (tile_size - 2, tile_size - 2))

pg.mixer.music.load ('resources/lofi.mp3')
pg.mixer.music.play(-1) 

background_image = pg.image.load('resources/background.png')
background_image = pg.transform.scale(background_image, (window, window))

#Тело игры и запуск (Данный цикл проверяет нажатия кнопок, есть словарь (массив данных с ключем и значением), проверяем направления змейки, которая не должна входить в саму себя)
while True:
  clock.tick(speed)
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
  #Создание фона
  screen.fill((0, 0, 0))
  screen.blit(background_image, (0, 0))

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
      #Обнуление змейки
      snake.center, food.center = get_random_position(), get_random_position()
      length, segments = 1, [snake.copy()]
      snake_dir = (0, 0)
      gameOverStr =  "Game over! " + "Score record: " + str(scoreRecord)
      text = font.render(gameOverStr, True, (255, 255, 255))
      gameOverSound = pg.mixer.Sound('resources/gameover.wav')
      pg.mixer.Sound.play(gameOverSound)
      speed = 8
      time_step = 250

  #Вывод текста счета:
  text_rect = text.get_rect(center=(410, 480))
  screen.blit(text, text_rect)
  
  #Проверка взаимодействия змейки с едой
  if snake.colliderect(food):
      food.center = get_random_position()
      length += 1
      if length > scoreRecord:
        scoreRecord = length-1
      speed += 1
      time_step -= 10
      PickSound = pg.mixer.Sound('resources/pick.mp3')
      pg.mixer.Sound.play(PickSound)
      
      showText = "Your score is: " + str (length-1)
      text = font.render(showText, True, (255, 255, 255))
      pg.display.flip()
  
  #Рисуем еду
  screen.blit(food_head_image, food)
  #Рисуем змейку
  screen.blit(snake_head_image, snake)
  for segment in segments[:-1]:
      screen.blit(food_head_image, segment)
  #Двигаем змейку (каждый тик змейка изменяет свое значение.Меняем значение, когда время превышает определенное кол-во тиков)
  time_now = pg.time.get_ticks()
  if time_now - time > time_step:
      time = time_now
      snake.move_ip(snake_dir)
      segments.append(snake.copy())
      segments = segments[-length:]
  pg.display.flip()
  clock.tick(60)