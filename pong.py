import pygame
import sys
from random import randint
from degrees_to_velocuty import degrees_to_velocity

pygame.init()  # инициализация модулей пайгейма


# константы
WHITE = (255, 255, 255)  # белый цвет
BLACK = (0, 0, 0)  # черный цвет
FPS = 30

# экран
screen_info = pygame.display.Info()
screen_width = screen_info.current_w  # ширина экрана в пикселях
screen_height = screen_info.current_h  # высота экрана в пикселях
screen = pygame.display.set_mode(
    (screen_width, screen_height),
    pygame.FULLSCREEN
)
screen_rect = screen.get_rect()

# игрок 1
player_width1 = 13  # ширина игрока
player_height1 = 80  # высота игрока
player1_score = 0
player1_speed = 10
player_x1 = 100  # игрок в центре по ширине
player_y1 = screen_height // 2 - player_height1 // 2
player1 = pygame.Rect((player_x1, player_y1, player_width1, player_height1))

# игрок 2
player_width2 = 13  # ширина игрока
player_height2 = 80  # высота игрока
player2_score = 0
player2_speed = 10
player_x2 = screen_width - 100 - player_width2
player_y2 = screen_height // 2 - player_height2 // 2
player2 = pygame.Rect((player_x2, player_y2, player_width2, player_height2))

# мяч
ball_width = 10
ball_height = 10
ball = pygame.Rect((1, 1, ball_height, ball_width))
ball_direction = degrees_to_velocity(45, 10)
ball_speed_x = ball_direction[0]
ball_speed_y = ball_direction[1]


def ball_to_center():
    ball.x = screen_width // 2 - ball_width
    ball.y = screen_height // 2 - ball_height


def rotate_ball():
    if randint(0, 1):
        ball_direction = degrees_to_velocity(randint(225, 315), 10)
    else:
        ball_direction = degrees_to_velocity(randint(45, 135), 10)
    ball_speed_x = ball_direction[0]
    ball_speed_y = ball_direction[1]
    return (ball_speed_x, ball_speed_y)


# часы
clock = pygame.time.Clock()

# табло
score_1 = pygame.font.Font(None, 50)  # создание табло
score_2 = pygame.font.Font(None, 50)


ball_to_center()
speeds = rotate_ball()
ball_speeds_x = speeds[0]
ball_speeds_y = speeds[1]
game = True
while game:
    player2_move1 = player2.y
    """
        Главный цикл игры
        Цикл должен обязательно закончится обновлением дисплея,
        если выйти по break, то игра зависнет!
        Контролируем, идет ли игра, переменной game
    """

    # события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # обработка события выхода
            game = False
        if event.type == pygame.KEYDOWN:  # нажатая клавиша (не зажатая!)
            if event.key == pygame.K_ESCAPE:  # клавиша Esc
                game = False
    keys = pygame.key.get_pressed()  # собираем коды нажатых клавиш в список
    """
    if keys[pygame.K_UP]:  # клавиша стрелка вверх
        if player2.y >= 0:
            player2.y -= player2_speed  # двигаем игрока вверх (в PG Y растет вниз)
    if keys[pygame.K_DOWN]:  # клавиша стрелка вниз
        if player2.y <= (screen_height - player_height2):
            player2.y += player2_speed  # двигаем игрока вниз
    """
    if keys[pygame.K_w]:  # клавиша стрелка вверх
        if player1.y >= 0:
            player1.y -= player1_speed  # двигаем игрока вверх (в PG Y растет вниз)
    if keys[pygame.K_s]:  # клавиша стрелка вниз
        if player1.y <= (screen_height - player_height2):
            player1.y += player1_speed  # двигаем игрока вниз

    # логика
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # комп двигает ракетку
    if ball.centery > player2.centery:  #
        player2.y += player2_speed
    if ball.centery < player2.centery:  #
        player2.y -= player2_speed
    # ограничение на движение компа
    if player2.top < 0:
        player2.top = 0
    if player2.bottom > screen_height:
        player2.bottom = screen_height
    # отскоки от бортов
    if ball.y < 0:
        ball_speed_y *= -1
    if ball.y > screen_height - ball_height:
        ball_speed_y *= -1

    # отскок от ракетки
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1
    if player2.y > player2_move1:
        print("игрок двигается вниз")
    elif player2.y < player2_move1:
        print("игрок двигается вверх")
    else:
        print("игрок не двигается")

    # ведём счёт
    if ball.x < 0:  # забил 2-й игрок
        player2_score += 1
        ball_to_center()
        speeds = rotate_ball()
        ball_speed_x = speeds[0]
        ball_speed_y = speeds[1]
    if ball.x > screen_width - ball_width:  # забил 1-й игрок
        player1_score += 1
        ball_to_center()
        speeds = rotate_ball()
        ball_speed_x = speeds[0]
        ball_speed_y = speeds[1]

    # отрисовка
    screen.fill(BLACK)  # заливаем экран чёрным
    pygame.draw.line(
        screen,
        WHITE,
        (screen_rect.centerx, 0),
        (screen_rect.centerx, screen_height)
     )
    pygame.draw.rect(screen, WHITE, ball)
    pygame.draw.rect(screen, WHITE, player1)  # рисуем игрока
    pygame.draw.rect(screen, WHITE, player2)
    score_1_img = score_1.render(str(player1_score), True, WHITE)  # снимаем с табло
    score_2_img = score_2.render(str(player2_score), True, WHITE)
    screen.blit(score_1_img, (screen_width * 0.25, 50))
    screen.blit(score_2_img, (screen_width * 0.75, 50))
    pygame.display.flip()  # обновляем экран

    # тик
    clock.tick(FPS)  # количество кадров в секунду

# после завершения главного цикла
pygame.quit()  # выгрузили модули pygame из пямяти
sys.exit()  # закрыли программу