# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import sys
from circleshape import *
from constants import *
from player import *
from asteroid import *
from asteroidfield import *
from shot import *

def main():
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    pygame.init()
    pygame.joystick.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
    asteroid_field = AsteroidField()

    ## Setup score display
    font = pygame.font.Font(None,36)
    score_text = font.render(f"Score: {player.score}",True,"white")
    score_text_rect = score_text.get_rect(topleft=(10,10))

    ## Setup joystick
    joystick_count = pygame.joystick.get_count()

    if joystick_count == 0:
        print("No joystick detected!")
    else:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        print(f"Detected joystick: {joystick.get_name()}")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)

        for a in asteroids:
            for s in shots:
                if s.colliding(a):
                    s.kill()
                    player.score += a.split()
                    score_text = font.render(f"Score: {player.score}",True,"white")
            if a.colliding(player):
                print("Game over!")
                sys.exit(1)

        screen.fill("black")

        # "Bake in score display"
        screen.blit(score_text,score_text_rect)

        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()