# Shmup Game
import pygame
import random
import shmup



# initialize pygame and create window
screen, clock = shmup.init()
shmup.Sound.explosions()  # load explosion sounds

def init_game(level=1):
    # Sprite Groups
    all_sprites = pygame.sprite.Group()
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    
    if level == 1:
        player = shmup.Player("red")
        # create 8 mobs(enemies)
        for i in range(5):
            shmup.new_mob(all_sprites, mobs)

    elif level == 2:
        player = shmup.Player("blue")
        for i in range(15):
            shmup.new_mob(all_sprites, mobs)

    all_sprites.add(player)

    # set player score to zero
    player.score = 0
    # play music in background
    pygame.mixer.music.play(loops=-1)

    return all_sprites, mobs, bullets, powerups, player, level

# intitial the game
all_sprites, mobs, bullets, powerups, player, level = init_game(1)

running = True
flag = True

while running:
    # keep loop running at the right speed
    clock.tick(shmup.Window.FPS)

    #   -- PROCESS INPUT(EVENTS) --
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if level == 1:
                    bullet = player.shoot("red")
                elif level == 2:
                    bullet = player.shoot("blue")

                all_sprites.add(bullet)
                bullets.add(bullet)
                
    #    -- UPDATE --
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        player.score += 50 - hit.radius
        random.choice(shmup.Sound.explosion_sounds).play()
        expl = shmup.Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = shmup.Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        shmup.new_mob(all_sprites, mobs)

    # change level if player score is greater than 200
    if player.score >= 1000 and flag:
        all_sprites, mobs, bullets, powerups, player, level = init_game(2)
        all_sprites.draw(screen)
        shmup.draw_text(screen, "Level 2", 50, shmup.Window.WIDTH//2, shmup.Window.HEIGHT//2)
        pygame.display.update()
        pygame.time.delay(1000)
        flag = False
        
        
    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = shmup.Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        shmup.new_mob(all_sprites, mobs)
        if player.shield <= 0:
            shmup.Sound.PLAYER_DIE.play()
            death_explosion = shmup.Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100
    
    # check to see if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()
    
    # if the player die and the explosion has finished playing
    if player.lives == 0 and not death_explosion.alive():
        running = False
        
    #   -- Draw (render) --
    screen.fill(shmup.Color.BLACK)
    if level == 1:
        screen.blit(shmup.Image.BACKGROUND, shmup.Image.BACKGROUND_RECT)
    elif level == 2: 
        screen.blit(shmup.Image.BACKGROUND2, shmup.Image.BACKGROUND2_RECT)

    all_sprites.draw(screen)
    shmup.draw_text(screen, str(player.score), 18, shmup.Window.WIDTH / 2, 10)
    # shmup.draw_text(screen, "Level 2", 50, shmup.Window.WIDTH / 2, shmup.Window.HEIGHT / 2)
    shmup.draw_shield_bar(screen, 5, 5, player.shield)
    shmup.draw_lives(screen, shmup.Window.WIDTH-100, 5, player.lives, shmup.Image.PLAYER_MINI)

    # *after* drawing everyting, flip the display
    pygame.display.flip()

# closing the game
pygame.quit()
