import pygame, sys, os
from pygame.locals import *

# Khởi tạo pygame
pygame.init()

WIDTH = 800
HEIGHT = 600
Player_width = 40
Player_height = 60
fps = pygame.time.Clock()
FPS = 30

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Demo')

#Colors
WHITE = (255, 255, 255)

player = pygame.image.load('player.png')
player = pygame.transform.scale(player, (Player_width, Player_height))
player_rect = player.get_rect(center = (50, 50))

# Hàm move để di chuyển nhân vật
def move(up, down, left, right):   
    speed = 10 
    if up:
        player_rect.centery -= speed
        if player_rect.top <= 0:
            player_rect.top =0
    if down:
        player_rect.centery += speed
        if player_rect.bottom >= HEIGHT:
            player_rect.bottom = HEIGHT
    if left:    
        player_rect.centerx -= speed
        if player_rect.left <= 0:
            player_rect.left = 0
    if right:
        player_rect.centerx += speed
        if player_rect.right >= WIDTH:
            player_rect.right = WIDTH

up, down, left, right = False, False, False, False

while True:
    WIN.fill(WHITE)
    WIN.blit(player, player_rect)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.exit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_UP:
                up = True
                print('up')
            if event.key == K_DOWN:
                down = True
                print('down')
            if event.key == K_LEFT:
                left = True
                print('left')
            if event.key == K_RIGHT:
                right = True
                print('right')
                
        if event.type == KEYUP:
            if event.key == K_UP:
                up = False                
            if event.key == K_DOWN:
                down = False
            if event.key == K_LEFT:
                left = False
            if event.key == K_RIGHT:
                right = False
    
    move(up, down, left, right)           
    
    pygame.display.update()
    fps.tick(FPS)
