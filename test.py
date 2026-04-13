import pygame
from pygame import mixer, display



clock = pygame.time.Clock()

pygame.init()
screen = pygame.display.set_mode((618, 359))
display.set_caption("Test game")
icon = pygame.image.load('asset_level/background2.png').convert_alpha()
display.set_icon(icon)


bg_sound = pygame.mixer.Sound('sound/bg_sound.mp3')
bg_sound.set_volume(0.5)
bg_sound.play()

bg = pygame.image.load('asset_level/images/background13.png').convert_alpha()
ghost = pygame.image.load("newshaxter/ghost.png").convert_alpha()
ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2000)
ghost_list_in_game = []

bullet = pygame.image.load("newshaxter/bullet.png").convert_alpha()
bullets = []
bullets_left = 15

walk_left = [
    pygame.image.load('newshaxter/player_left_4.png').convert_alpha(),
    pygame.image.load('newshaxter/player_left_3.png').convert_alpha(),
    pygame.image.load('newshaxter/player_left_1.png').convert_alpha(),
    pygame.image.load('newshaxter/player_left_2.png').convert_alpha(),
]

walk_right = [
    pygame.image.load('newshaxter/player_right_1.png').convert_alpha(),
    pygame.image.load('newshaxter/player_right_2.png').convert_alpha(),
    pygame.image.load('newshaxter/player_right_3.png').convert_alpha(),
    pygame.image.load('newshaxter/player_right_4.png').convert_alpha(),
]

player_anim_count = 0
bg_x = 0

player_x = 150
player_y = 250
player_speed = 5


is_jump = False
jump_count = 8


gamePlay = True
label = pygame.font.Font('freesansbold.ttf', 34)
lose_label = label.render('you lose;loser', False, (193, 196, 199))
restart_label = label.render('Go again', False, (115, 130, 145))
restart_label_rect = restart_label.get_rect(topleft=(180,150))



running = True
while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg,(bg_x + 618,0))

    if gamePlay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        if ghost_list_in_game:
            for (i,elem) in enumerate (ghost_list_in_game):
                screen.blit(ghost,elem)
                elem.x -= 10


                if elem.x < -10:
                    ghost_list_in_game.pop(i)

                if player_rect.colliderect(elem):
                    gamePlay = False




        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))


        if keys[pygame.K_a] and player_x > 50:
            player_x -= player_speed
        elif keys[pygame.K_d]:
            player_x += player_speed


        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
                if jump_count >= -8:
                    if jump_count > 0:
                        player_y -= (jump_count ** 2) / 2
                    else:
                        player_y += (jump_count ** 2) / 2

                    jump_count -= 1
                else:
                    is_jump = False
                    jump_count = 8



        if bullets:
            for (i,elem) in enumerate (bullets):
                screen.blit(bullet,(elem.x, elem.y))
                elem.x += 4


                if elem.x >= 630:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index,ghost_elem) in enumerate (ghost_list_in_game):
                        if elem.colliderect(ghost_elem):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)



    else:
        screen.fill((87, 88, 89))
        screen.blit(lose_label, (180, 100))
        screen.blit(restart_label,restart_label_rect)


        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gamePlay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()


    display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
        if gamePlay and event.type == pygame.KEYUP and event.key == pygame.K_e and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=(player_x+30, player_y+10)))
            bullets_left -= 1

            
    clock.tick(15)


