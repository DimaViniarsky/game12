import pygame  
import sys

WHITE = (255, 255, 255)

class Wall:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen, (128, 128, 128), self.rect)

class Bullet:
    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x, y - 2, 10, 5) 
        self.speed = 5 * direction

    def update(self):
        self.rect.x += self.speed

pygame.init()

shooting = False
bullet = None

bullets = []

class Enemy:
    def __init__(self, x, y, image_path, initial_x, speed, vertical_movement=False):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.initial_x = initial_x
        self.speed = speed
        self.direction = 1
        self.vertical_movement = vertical_movement
        self.vertical_distance = 0
        self.alive = True 

    def check_bullet_collision(self, bullets, enemies):
        for bullet in bullets:
            bullet_rect = bullet.rect
            for enemy in enemies:
                if enemy.alive and enemy.rect.colliderect(bullet_rect):
                    enemy.alive = False 
                    bullets.remove(bullet) 
                    break 

    def update(self):
        if self.vertical_movement:
            self.rect.y += self.speed * self.direction
            self.vertical_distance += self.speed  

            if self.vertical_distance >= 100:
                self.direction = -self.direction
                self.vertical_distance = 0 
        else:
            if self.rect.x <= self.initial_x - 100:
                self.direction = 1
            if self.rect.x >= self.initial_x + 100:
                self.direction = -1
            self.rect.x += self.speed * self.direction

        self.rect.x = max(self.rect.x, 0)
        self.rect.x = min(self.rect.x, screen_width - self.rect.width)
        self.rect.y = max(self.rect.y, 0)
        self.rect.y = min(self.rect.y, screen_height - self.rect.height)

screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Гра 'Лабіринт'")

pygame.mixer.music.load('background_music.mp3')
coin_sound = pygame.mixer.Sound('coin_sound.wav')

background = pygame.image.load('fon.png')
background = pygame.transform.scale(background, (screen_width, screen_height))

character_image = pygame.image.load('character.png')
character_image = pygame.transform.scale(character_image, (50, 50))
character_rect = character_image.get_rect(center=(70, 550))

bullet_image = pygame.image.load('bullet.png') 
bullet_image = pygame.transform.scale(bullet_image, (20, 10))

coins = [pygame.image.load('coin.png') for _ in range(5)]
coin_size = (50, 50)
coins = [pygame.transform.scale(coin, coin_size) for coin in coins]

coins_collected = [False] * len(coins)
portal_rect = pygame.Rect(700, 500, 50, 50)

game_over = False

walls = [
    Wall(100, 0, 20, 100),
    Wall(0, 180, 200, 20),
    Wall(180, 180, 20, 300),
    Wall(0, 350, 100, 20),
    Wall(300, 460, 350, 20),
    Wall(300, 100, 20, 379),
    Wall(420, 0, 20, 379),
    Wall(420, 460, 20, 200),
    Wall(550, 100, 20, 280),
    Wall(550, 362, 280, 20),
    Wall(550, 100, 150, 20),
    Wall(670, 220, 150, 20)
]

walls2 = [
    Wall(0, 300, 700, 20),
    Wall(0, 450, 200, 20),
    Wall(360, 450, 310, 20),
    Wall(350, 300, 20, 170),
    Wall(450, 375, 400, 20),
    Wall(130, 380, 20, 85),
    Wall(500, 450, 20, 85),
    Wall(350, 540, 20, 85),
    Wall(600, 530, 200, 20),
    Wall(680, 100, 20, 220),
    Wall(580, 0, 20, 220),
    Wall(480, 100, 20, 220),
    Wall(380, 0, 20, 220),
    Wall(100, 200, 280, 20),
    Wall(0, 120, 280, 20)
]

walls3 = [
    Wall(680, 300, 20, 200),
    Wall(0, 480, 750, 20),
    Wall(680, 100, 20, 140),
    Wall(480, 100, 20, 380),
    Wall(570, 300, 120, 20),
    Wall(570, 220, 120, 20),
    Wall(200, 500, 20, 50),
    Wall(350, 555, 20, 50),
    Wall(650, 555, 20, 50),
    Wall(70, 100, 680, 20),
    Wall(100, 50, 20, 50),
    Wall(250, 0, 20, 45),
    Wall(400, 50, 20, 50),
    Wall(550, 0, 20, 45),
    Wall(70, 100, 20, 200),
    Wall(70, 280, 200, 20)
]

def check_bullet_collision(bullets, enemies):
    for bullet in bullets:
        bullet_rect = bullet.rect
        for enemy in enemies:
            if enemy.alive and enemy.rect.colliderect(bullet_rect):
                enemy.alive = False 
                bullets.remove(bullet) 
                break

def level_menu():
    while True:
        screen.blit(background, (0, 0))

        level1_button = pygame.draw.rect(screen, (0, 128, 0), (300, 200, 200, 50))
        level2_button = pygame.draw.rect(screen, (0, 128, 0), (300, 300, 200, 50))
        level3_button = pygame.draw.rect(screen, (0, 128, 0), (300, 400, 200, 50))
        back_button = pygame.draw.rect(screen, (0, 0, 0), (320, 500, 175, 50))

        font = pygame.font.Font(None, 36)
        level1_text = font.render('Рівень 1', True, WHITE)
        level2_text = font.render('Рівень 2', True, WHITE)
        level3_text = font.render('Рівень 3', True, WHITE)
        back_text = font.render('Повернутися', True, WHITE)

        screen.blit(level1_text, (350, 210))
        screen.blit(level2_text, (350, 310))
        screen.blit(level3_text, (350, 410))
        screen.blit(back_text, (330, 510))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_button.collidepoint(pygame.mouse.get_pos()):
                    start_game(1)
                elif level2_button.collidepoint(pygame.mouse.get_pos()):
                    start_game(2)
                elif level3_button.collidepoint(pygame.mouse.get_pos()):
                    start_game(3)
                elif back_button.collidepoint(pygame.mouse.get_pos()):
                    return

def start_game(level):
    global character_rect, coins_collected, bullets, character_direction, game_over

    if level == 1:
        new_coin_positions = [(700, 275), (25, 250), (25, 30), (500, 510), (470, 200)]
        coin_rects = [coin.get_rect(topleft=pos) for coin, pos in zip(coins, new_coin_positions,)]

        enemies = [
            Enemy(200, 120, 'enemy1.png', initial_x=100, speed=1),
            Enemy(590, 160, 'enemy2.png', initial_x=200, speed=1, vertical_movement=True),
            Enemy(490, 400, 'enemy3.png', initial_x=520, speed=1)
        ]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append(Bullet(character_rect.right, character_rect.centery, character_direction))

            if not game_over:
                keys = pygame.key.get_pressed()
                new_character_rect = character_rect.copy()

                for enemy in enemies:
                    enemy.update()
                    if enemy.rect.colliderect(character_rect):
                        game_over = True

                if keys[pygame.K_LEFT]:
                    new_character_rect.move_ip(-3, 0)
                    character_direction = -1 
                if keys[pygame.K_RIGHT]:
                    new_character_rect.move_ip(3, 0)
                    character_direction = 1  
                if keys[pygame.K_UP]:
                    new_character_rect.move_ip(0, -3)
                if keys[pygame.K_DOWN]:
                    new_character_rect.move_ip(0, 3)

                new_character_rect.left = max(new_character_rect.left, 0)
                new_character_rect.right = min(new_character_rect.right, screen_width)
                new_character_rect.top = max(new_character_rect.top, 0)
                new_character_rect.bottom = min(new_character_rect.bottom, screen_height)

                collision = False
                for wall in walls:
                    if new_character_rect.colliderect(wall.rect):
                        collision = True
                        break

                if not collision:
                    character_rect = new_character_rect

                new_bullets = []
                for bullet in bullets:
                    bullet.update()
                    screen.blit(bullet_image, bullet.rect)

                    hit_wall = False
                    for wall in walls:
                        if bullet.rect.colliderect(wall.rect):
                            hit_wall = True
                            break

                    if not hit_wall:
                        new_bullets.append(bullet)

                bullets = new_bullets

                for enemy in enemies:
                    if enemy.alive and enemy.rect.colliderect(character_rect):
                        game_over = True
                    enemy.check_bullet_collision(bullets, [enemy])  
                    screen.blit(enemy.image, enemy.rect)

                screen.blit(background, (0, 0))
                for wall in walls:
                    wall.draw(screen)

                enemies = [enemy for enemy in enemies if enemy.alive]

                for i, coin_rect in enumerate(coin_rects):
                    if not coins_collected[i]:
                        screen.blit(coins[i], coin_rect)

                for i, bullet in enumerate(bullets):
                    bullet.update()
                    screen.blit(bullet_image, bullet.rect)

                enemies = [enemy for enemy in enemies if enemy.alive]

                for i, coin_rect in enumerate(coin_rects):
                    if not coins_collected[i]:
                        screen.blit(coins[i], coin_rect)

                for enemy in enemies:
                    screen.blit(enemy.image, enemy.rect) 

                if all(coins_collected):
                    pygame.draw.rect(screen, (0, 0, 255), portal_rect)
                    if character_rect.colliderect(portal_rect):
                        next_level()

                collision_with_coin_indices = [i for i, coin_rect in enumerate(coin_rects) if character_rect.colliderect(coin_rect)]
                for index in collision_with_coin_indices:
                    coins_collected[index] = True
                    coin_rects[index] = pygame.Rect(0, 0, 0, 0)

                screen.blit(character_image, character_rect)

                if game_over:
                    game_over_image = pygame.image.load('game_over_image.png')
                    game_over_image = pygame.transform.scale(game_over_image, (800, 600))
                    screen.blit(game_over_image, (0, 0))

                    back_button = pygame.draw.rect(screen, (0, 128, 0), (305, 500, 200, 50))
                    font_obj = pygame.font.Font(None, 36)
                    back_text = font_obj.render('Повернутися', True, WHITE)
                    screen.blit(back_text, (330, 510))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if back_button.collidepoint(pygame.mouse.get_pos()):
                                character_rect.center = (70, 550)
                                bullets = []
                                coins_collected = [False] * len(coins)
                                for enemy in enemies:
                                    enemy.rect.topleft = (enemy.initial_x, enemy.rect.y)
                                    enemy.direction = 1
                                game_over = False 
                                game_loop()

                pygame.display.update()

    elif level == 2:
        new_coin_positions2 = [(305, 145), (750, 550), (25, 360), (720, 300), (460, 25)]
        coin_rects = [coin.get_rect(topleft=pos) for coin, pos in zip(coins, new_coin_positions2,)]

        enemies = [
            Enemy(200, 142, 'enemy1.png', initial_x=100, speed=1),
            Enemy(80, 310, 'enemy2.png', initial_x=200, speed=1, vertical_movement=True),
            Enemy(490, 400, 'enemy3.png', initial_x=520, speed=1),
            Enemy(515, 130, 'enemy1.png', initial_x=50, speed=1, vertical_movement=True),
            Enemy(415, 0, 'enemy2.png', initial_x=700, speed=1, vertical_movement=True),
        ]
        
        portal_rect = pygame.Rect(100, 50, 50, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append(Bullet(character_rect.right, character_rect.centery, character_direction))

            if not game_over:
                keys = pygame.key.get_pressed()
                new_character_rect = character_rect.copy()

                for enemy in enemies:
                    enemy.update()
                    if enemy.rect.colliderect(character_rect):
                        game_over = True

                if keys[pygame.K_LEFT]:
                    new_character_rect.move_ip(-3, 0)
                    character_direction = -1 
                if keys[pygame.K_RIGHT]:
                    new_character_rect.move_ip(3, 0)
                    character_direction = 1  
                if keys[pygame.K_UP]:
                    new_character_rect.move_ip(0, -3)
                if keys[pygame.K_DOWN]:
                    new_character_rect.move_ip(0, 3)

                new_character_rect.left = max(new_character_rect.left, 0)
                new_character_rect.right = min(new_character_rect.right, screen_width)
                new_character_rect.top = max(new_character_rect.top, 0)
                new_character_rect.bottom = min(new_character_rect.bottom, screen_height)

                collision = False
                for wall in walls2:
                    if new_character_rect.colliderect(wall.rect):
                        collision = True
                        break

                if not collision:
                    character_rect = new_character_rect

                new_bullets = []
                for bullet in bullets:
                    bullet.update()
                    screen.blit(bullet_image, bullet.rect)

                    hit_wall = False
                    for wall in walls2:
                        if bullet.rect.colliderect(wall.rect):
                            hit_wall = True
                            break

                    if not hit_wall:
                        new_bullets.append(bullet)

                bullets = new_bullets

                for enemy in enemies:
                    if enemy.alive and enemy.rect.colliderect(character_rect):
                        game_over = True
                    enemy.check_bullet_collision(bullets, [enemy])  
                    screen.blit(enemy.image, enemy.rect)

                screen.blit(background, (0, 0))
                for wall in walls2:
                    wall.draw(screen)

                enemies = [enemy for enemy in enemies if enemy.alive]

                for i, coin_rect in enumerate(coin_rects):
                    if not coins_collected[i]:
                        screen.blit(coins[i], coin_rect)

                for i, bullet in enumerate(bullets):
                    bullet.update()
                    screen.blit(bullet_image, bullet.rect)

                for enemy in enemies:
                    screen.blit(enemy.image, enemy.rect) 

                if all(coins_collected):
                    pygame.draw.rect(screen, (0, 0, 255), portal_rect)
                    if character_rect.colliderect(portal_rect):
                        next_level()

                collision_with_coin_indices = [i for i, coin_rect in enumerate(coin_rects) if character_rect.colliderect(coin_rect)]
                for index in collision_with_coin_indices:
                    coins_collected[index] = True
                    coin_rects[index] = pygame.Rect(0, 0, 0, 0)
                screen.blit(character_image, character_rect)

                if game_over:
                    game_over_image = pygame.image.load('game_over_image.png')
                    game_over_image = pygame.transform.scale(game_over_image, (800, 600))
                    screen.blit(game_over_image, (0, 0))

                    back_button = pygame.draw.rect(screen, (0, 128, 0), (305, 500, 200, 50))
                    font_obj = pygame.font.Font(None, 36)
                    back_text = font_obj.render('Повернутися', True, WHITE)
                    screen.blit(back_text, (330, 510))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if back_button.collidepoint(pygame.mouse.get_pos()):
                                character_rect.center = (70, 550)
                                bullets = []
                                coins_collected = [False] * len(coins)
                                for enemy in enemies:
                                    enemy.rect.topleft = (enemy.initial_x, enemy.rect.y)
                                    enemy.direction = 1
                                game_over = False 
                                game_loop()

                pygame.display.update()

    elif level == 3:
        new_coin_positions3 = [(560, 360), (560, 135), (130, 525), (150, 170), (460, 25)]
        coin_rects = [coin.get_rect(topleft=pos) for coin, pos in zip(coins, new_coin_positions3,)]

        enemies = [
            Enemy(150, 0, 'enemy1.png', initial_x=100, speed=1),
            Enemy(80, 310, 'enemy2.png', initial_x=200, speed=1, vertical_movement=True),
            Enemy(650, 500, 'enemy3.png', initial_x=520, speed=1),
            Enemy(515, 230, 'enemy1.png', initial_x=50, speed=1, vertical_movement=True),
            Enemy(200, 120, 'enemy2.png', initial_x=700, speed=1, vertical_movement=True),
        ]
        
        portal_rect = pygame.Rect(350, 400, 50, 50)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append(Bullet(character_rect.right, character_rect.centery, character_direction))

            if not game_over:
                keys = pygame.key.get_pressed()
                new_character_rect = character_rect.copy()

                for enemy in enemies:
                    enemy.update()
                    if enemy.rect.colliderect(character_rect):
                        game_over = True

                if keys[pygame.K_LEFT]:
                    new_character_rect.move_ip(-3, 0)
                    character_direction = -1 
                if keys[pygame.K_RIGHT]:
                    new_character_rect.move_ip(3, 0)
                    character_direction = 1  
                if keys[pygame.K_UP]:
                    new_character_rect.move_ip(0, -3)
                if keys[pygame.K_DOWN]:
                    new_character_rect.move_ip(0, 3)

                new_character_rect.left = max(new_character_rect.left, 0)
                new_character_rect.right = min(new_character_rect.right, screen_width)
                new_character_rect.top = max(new_character_rect.top, 0)
                new_character_rect.bottom = min(new_character_rect.bottom, screen_height)

                collision = False
                for wall in walls3:
                    if new_character_rect.colliderect(wall.rect):
                        collision = True
                        break

                if not collision:
                    character_rect = new_character_rect

                new_bullets = []
                for bullet in bullets:
                    bullet.update()
                    screen.blit(bullet_image, bullet.rect)

                    hit_wall = False
                    for wall in walls3:
                        if bullet.rect.colliderect(wall.rect):
                            hit_wall = True
                            break

                    if not hit_wall:
                        new_bullets.append(bullet)

                bullets = new_bullets

                for enemy in enemies:
                    if enemy.alive and enemy.rect.colliderect(character_rect):
                        game_over = True
                    enemy.check_bullet_collision(bullets, [enemy])  
                    screen.blit(enemy.image, enemy.rect)

                screen.blit(background, (0, 0))
                for wall in walls3:
                    wall.draw(screen)

                enemies = [enemy for enemy in enemies if enemy.alive]

                for i, coin_rect in enumerate(coin_rects):
                    if not coins_collected[i]:
                        screen.blit(coins[i], coin_rect)

                for i, bullet in enumerate(bullets):
                    bullet.update()
                    screen.blit(bullet_image, bullet.rect)

                for enemy in enemies:
                    screen.blit(enemy.image, enemy.rect) 

                if all(coins_collected):
                    pygame.draw.rect(screen, (0, 0, 255), portal_rect)
                    if character_rect.colliderect(portal_rect):
                        next_level()

                collision_with_coin_indices = [i for i, coin_rect in enumerate(coin_rects) if character_rect.colliderect(coin_rect)]
                for index in collision_with_coin_indices:
                    coins_collected[index] = True
                    coin_rects[index] = pygame.Rect(0, 0, 0, 0)
                screen.blit(character_image, character_rect)

                if game_over:
                    game_over_image = pygame.image.load('game_over_image.png')
                    game_over_image = pygame.transform.scale(game_over_image, (800, 600))
                    screen.blit(game_over_image, (0, 0))

                    back_button = pygame.draw.rect(screen, (0, 128, 0), (305, 500, 200, 50))
                    font_obj = pygame.font.Font(None, 36)
                    back_text = font_obj.render('Повернутися', True, WHITE)
                    screen.blit(back_text, (330, 510))

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if back_button.collidepoint(pygame.mouse.get_pos()):
                                character_rect.center = (70, 550)
                                bullets = []
                                coins_collected = [False] * len(coins)
                                for enemy in enemies:
                                    enemy.rect.topleft = (enemy.initial_x, enemy.rect.y)
                                    enemy.direction = 1
                                game_over = False 
                                game_loop()

                pygame.display.update()
        
def main_menu():
    while True:
        screen.blit(background, (0, 0))

        start_button = pygame.draw.rect(screen, (0, 128, 0), (300, 200, 200, 50))
        settings_button = pygame.draw.rect(screen, (0, 128, 0), (300, 300, 200, 50))
        exit_button = pygame.draw.rect(screen, (255, 0, 0), (300, 400, 200, 50))

        font = pygame.font.Font(None, 36)
        start_text = font.render('Пуск гри', True, WHITE)
        settings_text = font.render('Налаштування', True, WHITE)
        exit_text = font.render('Вихід', True, WHITE)

        screen.blit(start_text, (345, 210))
        screen.blit(settings_text, (315, 310))
        screen.blit(exit_text, (365, 410))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    level_menu()
                elif settings_button.collidepoint(pygame.mouse.get_pos()):
                    settings_menu()
                elif exit_button.collidepoint(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()

        pygame.mixer.music.play(-1)
        main_menu()

def settings_menu():
    music_on = True

    GREEN = (0, 128, 0)
    RED = (255, 0, 0)

    while True:
        screen.blit(background, (0, 0))

        if music_on:
            music_button_color = GREEN
        else:
            music_button_color = RED

        on_button = pygame.draw.rect(screen, music_button_color, (270, 190, 150, 50))
        back_button = pygame.draw.rect(screen, (0, 0, 0), (320, 400, 175, 50))

        font_obj = pygame.font.Font(None, 36)
        music_text = font_obj.render('Музика:', True, (0, 0, 0))
        music_status = font_obj.render('Увімкнено' if music_on else 'Вимкнено', True, (0, 0, 0))
        back_text = font_obj.render('Повернутися', True, (255, 255, 255))

        screen.blit(music_text, (300, 200))
        screen.blit(music_status, (450, 200))
        screen.blit(back_text, (330, 410))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if on_button.collidepoint(pygame.mouse.get_pos()):
                    music_on = not music_on
                    if music_on:
                        pygame.mixer.music.play(-1)
                    else:
                        pygame.mixer.music.stop()
                        coin_sound.stop() 
                elif back_button.collidepoint(pygame.mouse.get_pos()):
                    return

if __name__ == "__main__":
    pygame.mixer.music.play(-1)
    main_menu()