import pygame

from env_logic.environment import Environment

env = Environment(enable_rendering=True)
clock = pygame.time.Clock()
end_sim = False

while not end_sim:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_sim = True

    pressed = pygame.key.get_pressed()
    action_val = 0
    if pressed[pygame.K_LEFT]:
        action_val = 1
    if pressed[pygame.K_RIGHT]:
        action_val = 2
    if pressed[pygame.K_UP]:
        action_val = 3
    if pressed[pygame.K_DOWN]:
        action_val = 4
    if pressed[pygame.K_SPACE]:
        action_val = 5
    if pressed[pygame.K_r]:
        action_val = 6
    if pressed[pygame.K_UP] and pressed[pygame.K_RIGHT]:
        action_val = 7
    if pressed[pygame.K_UP] and pressed[pygame.K_LEFT]:
        action_val = 8

    _, _, done, _ = env.step(action_val)
    env.render()
    if done:
        env.reset()

    clock.tick(60)

pygame.quit()
