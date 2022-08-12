import pygame
import os
pygame.font.init()
WIDTH, HEIGHT = 900, 500

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

BG = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bg.jpg')), (900, 500))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

BORDER = pygame.Rect(445, 0, 10, 500)
WHITE = (255, 255, 255)

FIRST_HIT = pygame.USEREVENT + 1
SECOND_HIT = pygame.USEREVENT + 2

PACMAN1_IMG = pygame.image.load(os.path.join('assets', 'pac1.png'))
PACMAN2_IMG = pygame.image.load(os.path.join('assets', 'pac2.png'))

PACMAN1 = pygame.transform.scale(PACMAN1_IMG, (60, 70))
PACMAN2 = pygame.transform.flip(pygame.transform.scale(PACMAN2_IMG, (60, 70)), True, False)
#Frames per second (to limit the speed of the cycle, so on all computers our game works at the same speed)
FPS = 60 #loop will run 60 time per second (or less)
VEL = 3 #velocity
BULLET_VEL = 10
MAX_BULLETS = 4


def drawWindow(first, second, first_bullets, second_bullets, first_health, second_health):
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, (33, 140, 77), BORDER)

    first_health_text = HEALTH_FONT.render('Health: ' + str(first_health), 1, WHITE)
    second_health_text = HEALTH_FONT.render('Health: ' + str(second_health), 1, WHITE)
    WIN.blit(first_health_text, (10, 0))
    WIN.blit(second_health_text, (720, 0))

    WIN.blit(PACMAN1, (first.x, first.y))
    WIN.blit(PACMAN2, (second.x, second.y))
    for bullet in first_bullets:
        pygame.draw.rect(WIN, (177, 216, 255), bullet)
    for bullet in second_bullets:
        pygame.draw.rect(WIN, (240, 240, 0), bullet)
    pygame.display.update()

def first_movements(keys_pressed, first):
    if keys_pressed[pygame.K_a] and first.x - VEL > 0:
        first.x -= VEL
    if keys_pressed[pygame.K_d] and first.x + VEL < 385:
        first.x += VEL
    if keys_pressed[pygame.K_w] and first.y - VEL > 0:
        first.y -= VEL
    if keys_pressed[pygame.K_s] and first.y + VEL < 430:
        first.y += VEL

def second_movements(keys_pressed, second):
    if keys_pressed[pygame.K_LEFT] and second.x - VEL > 455:
        second.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and second.x + VEL < 840:
        second.x += VEL
    if keys_pressed[pygame.K_UP] and second.y - VEL > 0:
        second.y -= VEL
    if keys_pressed[pygame.K_DOWN] and second.y + VEL < 430:
        second.y += VEL

def handle_bullets(first_bullets, second_bullets, first, second):
    for bullet in first_bullets:
        bullet.x += BULLET_VEL
        if second.colliderect(bullet):
            pygame.event.post(pygame.event.Event(SECOND_HIT))
            first_bullets.remove(bullet)
        elif bullet.x > 900:
            first_bullets.remove(bullet)
    for bullet in second_bullets:
        bullet.x -= BULLET_VEL
        if first.colliderect(bullet):
            pygame.event.post(pygame.event.Event(FIRST_HIT))
            second_bullets.remove(bullet)
        elif bullet.x < 0:
            second_bullets.remove(bullet)

def draw_winner(text):
    winnerText = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winnerText, (100, 100))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    first = pygame.Rect(100, 300, 100, 200)
    second = pygame.Rect(700, 300, 720, 200)
    first_bullets = []
    second_bullets = []
    first_health = 5
    second_health = 5
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(first_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(first.x + 40, first.y + 30, 10, 5)
                    first_bullets.append(bullet)
                if event.key == pygame.K_RETURN and len(second_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(second.x + 10, second.y + 30, 10, 5)
                    second_bullets.append(bullet)
            if event.type == FIRST_HIT:
                first_health -= 1
            if event.type == SECOND_HIT:
                second_health -= 1
        drawWindow(first, second, first_bullets, second_bullets, first_health, second_health)
        winner_text = ""
        if first_health <= 0:
            winner_text = 'Second player wins!'
        if second_health <= 0:
            winner_text = 'First player wins!'
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        first_movements(keys_pressed, first)
        second_movements(keys_pressed, second)

        handle_bullets(first_bullets, second_bullets, first, second)


    pygame.quit()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
