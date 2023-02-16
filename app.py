import pygame
import random
import math

pygame.init()

screen = pygame.display.set_mode((800, 600))

# CREAMOS EL SCORE
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

#  MOSTRAR EL SCORE EN PANTALLA
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# IMAGEN DE FONDO
background = pygame.image.load('space.png')

# TITULO E ICONO
pygame.display.set_caption("space invaders")
icon = pygame.image.load('001-ufo.png')
pygame.display.set_icon(icon)

# ENEMIGO
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('001-alien.png'))
    enemyX.append(random.randint(0, 768))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.09)
    enemyY_change.append(40)

# BALA
bulletImg = pygame.image.load('001-bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0.3
bulletY_change = 0.9
new_x = 0
new_y = 0
bullet_state = "ready"  # READY = NO PUEDO VER LA BALA EN PANTALLA. FIRE = SE VE.

# JUGADOR
playerImg = pygame.image.load('001-space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0


# VARIABLES DE ROTACION
player_angle = 0
player_rotated_image = playerImg

# FUNCIONES DE LOS OBJETOS
def player(x, y):
    global player_rotated_image, player_angle
    player_rotated_image = pygame.transform.rotate(playerImg, player_angle)
    screen.blit(player_rotated_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))



# DISPARAR
def fire_bullet(x, y):
    global bullet_state, player_angle
    bullet_state = "fire"

    #  calculamos el angulo en radianes
    angle = math.radians(player_angle)

    # calculamos la posicion de la bala
    new_x = x - 10 + 15 * math.cos(angle)
    new_y = y + 10 - 20 * math.sin(angle)

    # Dibujamos la bala
    screen.blit(bulletImg, (new_x, new_y))

screen.blit(bulletImg, (new_x, new_y))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# GAME LOOP
running = True
while running:
    screen.fill((0, 0, 0))

    # IMAGEN DE FONDO
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # chequeamos que tecla fue presionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_e:
                player_angle += 5
            if event.key == pygame.K_q:
                player_angle -= 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # chequeando los limites
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX >= 768:
        playerX = 768
    
    #movimiento del enemigo
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i]= 0.09
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 768:
            enemyX_change[i] = -0.09
            enemyY[i] += enemyY_change[i]
        # detectar colision de la bala con el enemigo
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 768)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    if score_value == 20:
        # CARTEL DE VICTORIA
        font = pygame.font.Font(None, 36)
        text = font.render("YOU WIN", True, (255, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery
        screen.blit(text, text_rect)
        pygame.display.update()
        
        # BUCLE POST VICTORIA PARA CERRAR EL CLIENTE
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

    show_score(10, 10)
    player(playerX, playerY)
    pygame.display.update()


