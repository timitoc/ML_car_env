import pygame

from env_logic.environment import Environment

env = Environment(enable_rendering=True)
clock = pygame.time.Clock()
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    action_val = 0
    if pressed[pygame.K_LEFT]:
        action_val = 2
    if pressed[pygame.K_RIGHT]:
        action_val = 3
    if pressed[pygame.K_UP]:
        action_val += 4
    if pressed[pygame.K_DOWN]:
        action_val = 5
    if pressed[pygame.K_r]:
        action_val = 1

    env.step(action_val)
    env.render()

    clock.tick(60)

pygame.quit()
