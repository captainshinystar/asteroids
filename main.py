import pygame
import sys
from constants import *
from player import *
from asteroid import *
from asteroidfield import AsteroidField
from shot import Shot
from text_utils import *

def load_high_score():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0

def save_high_score(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))

def main():
    import os
    os.environ['SDL_AUDIODRIVER'] = 'pulseaudio'
    pygame.init()
    background = pygame.image.load("asteroids.jpg")
    pygame.mixer.init(44100, -16, 2, 2048)
    try:
        pygame.mixer.music.load("Battle in the Stars.ogg")
    except pygame.error:
        print("Could not load background music")
    pygame.mixer.music.set_volume(0.3) #adjust volume (0.0 to 1.0)
    pygame.mixer.music.play(-1) #-1 means loop forever
    crash_sound = pygame.mixer.Sound("explosion.wav")
    crash_sound.set_volume(0.4)
    asteroid_sound = pygame.mixer.Sound("destroy_asteroid.wav")
    asteroid_sound.set_volume(0.5)
    multiplier_sound = pygame.mixer.Sound("Rise02.wav")
    multiplier_sound.set_volume(0.5)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0
    high_score = load_high_score()
    original_high_score = high_score
    score = 0
    multiplier = 1
    last_hit_time = 0
    last_decay_time = 0
    font = pygame.font.Font(None, 36)
    game_over_font = pygame.font.Font(None, 74)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Asteroid.containers = (updatable, drawable, asteroids)
    Player.containers = (updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (updatable, drawable, shots)
    
    player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
    asteroidfield = AsteroidField()

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
            if event.type == pygame.QUIT:
                return
        
        current_time = pygame.time.get_ticks()
        if current_time - last_hit_time > 2000:
            if current_time - last_decay_time > 2000:
                if multiplier > 1.0:
                    multiplier = max(1, multiplier - 0.2)
                    last_decay_time = current_time
            
        for thing in updatable:
            thing.update(dt)
        
        screen.blit(background, (0,0))
        for thing in drawable:
            thing.draw(screen)

        draw_outlined_text(screen, f"Score: {score} (x{multiplier:.1f})", font, (10, 10))
        draw_outlined_text(screen, f"High Score: {high_score}", font, (10, 50))        
     

        for asteroid in asteroids:
            if asteroid.collision(player):
                print("Game over!")
                crash_sound.play()
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.load("Game Over II.ogg")
                except pygame.error:
                    print("Could not load background music")
                pygame.mixer.music.play()
                draw_outlined_text_centered(screen, "Game Over!", game_over_font, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), "red", "black")
                draw_outlined_text_centered(screen, "Press Space to Close", font, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100), "white", "black")
                draw_outlined_text_centered(screen, "Press R to Retry", font, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 150), "white", "black")
               
                if score > original_high_score:
                    draw_outlined_text_centered(screen, f"New High Score: {score}!", font, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50), "yellow", "black")
                else:
                    draw_outlined_text_centered(screen, f"Final Score: {score}", font, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50), "white", "black")
                               
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                sys.exit()
                            if event.key == pygame.K_r:
                                score = 0
                                multiplier = 1
                                last_hit_time = 0
                                last_decay_time = 0
                                updatable.empty()
                                drawable.empty()
                                asteroids.empty()
                                shots.empty()
                                player = Player((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))
                                asteroidfield = AsteroidField()
                                updatable.add(player)
                                drawable.add(player)
                                try:
                                    pygame.mixer.music.load("Battle in the Stars.ogg")
                                except pygame.error:
                                    print("Could not load background music")
                                pygame.mixer.music.play(-1)
                                break
                    else:
                        continue
                    break
                continue
            for shot in shots:
                if shot.collision(asteroid):
                    if asteroid.radius == ASTEROID_MAX_RADIUS:
                        points = 25
                    elif asteroid.radius == (ASTEROID_MAX_RADIUS - 20):
                        points = 50
                    elif asteroid.radius == ASTEROID_MIN_RADIUS:
                        points = 100
                    score += int(points * multiplier)
                    old_multiplier = multiplier
                    multiplier = min(MAX_MULTIPLIER, multiplier + 0.1)
                    if int(multiplier) > int(old_multiplier):
                        multiplier_sound.play()
                    last_hit_time = current_time
                    shot.kill()
                    asteroid.split()
                    asteroid_sound.play()
        
        if score > high_score:
            high_score = score
            save_high_score(high_score)
        
        
        
        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()