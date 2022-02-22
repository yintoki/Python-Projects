import random
import sys
import pygame as pg
import pygame.time

pg.init()
clock = pg.time.Clock()

screen_size = width, height = 1280, 960
screen = pg.display.set_mode(screen_size)
pygame.display.set_caption("Pong")

#Game Rectangles
ball = pg.Rect(width/2 - 15, height/2 - 15,40,40)
player = pg.Rect(width - 20, height/2 - 70, 10, 140)
opponent = pg.Rect(20, height/2 - 70, 10, 140)

#Variables
ball_speed_y, ball_speed_x = 7 * random.choice((1, -1)), 7 * random.choice((1, -1))
player_speed = 0
opponent_speed = 7

#Text Variable
player_score = 0
opponent_score = 0
game_font = pg.font.Font("freesansbold.ttf", 32)

#Score Timer
score_time = True

#colors
cyan = (0, 102, 102)
bg_color = pg.Color("grey12")
light_grey = (96, 96, 96)
turqoise = (0, 153, 153)


#Functions
def ball_anim():
    global ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1

    if ball.right >= width:
        opponent_score += 1
        score_time = pg.time.get_ticks()

    if ball.left <= 0:
        player_score += 1
        score_time = pg.time.get_ticks()

    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1
def player_anim():
    player.y += player_speed
    if player.top <= 0:
        player.top = 0
    if player.bottom >= height:
        player.bottom = height
def opponent_ai():
    if opponent.top < ball.y:
        opponent.top += opponent_speed
    if opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= height:
        opponent.bottom = height
def ball_rest():
    global ball_speed_x, ball_speed_y, score_time

    current_time = pg.time.get_ticks()
    ball.center = (width/2, height/2)

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, light_grey)
        screen.blit(number_three, (width/2 - 10, height / 2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, light_grey)
        screen.blit(number_two, (width / 2 - 10, height / 2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, light_grey)
        screen.blit(number_one, (width/2 - 10, height / 2 + 20))

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_x = 7 * random.choice((1, -1))
        ball_speed_y = 7 * random.choice((1, -1))
        score_time = None



while True:
    #input Handling
    for event in pg.event.get():
        if event.type == pygame.QUIT:
            pg.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                player_speed += 7
            if event.key == pygame.K_w:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_s:
                player_speed -= 7
            if event.key == pygame.K_w:
                player_speed += 7

    #animation
    ball_anim()
    player_anim()
    opponent_ai()

    #Visuals
    screen.fill(bg_color)
    pg.draw.rect(screen, cyan, player)
    pg.draw.rect(screen, turqoise, opponent)
    pg.draw.ellipse(screen, light_grey, ball)
    pg.draw.aaline(screen, light_grey, (width/2 - 5,0), (width/2, height))

    if score_time:
        ball_rest()

    #Text Visuals
    player_text = game_font.render(f"{player_score}", False, light_grey)
    screen.blit(player_text, (660, 470))

    opponent_text = game_font.render(f"{opponent_score}", False, light_grey)
    screen.blit(opponent_text, (600, 470))

    pygame.display.flip()
    clock.tick(60)