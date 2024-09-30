import pygame
import time
import objects.system_of_particles.particle as p

pygame.init()

window_color = "#F0EBD8"
window_size = window_width, window_height = 1280, 720
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
dt = 0

test_particle_1 = p.Particle(
    radius=10,
    init_position2=(100, 100),
    init_velocity2=(100, 120),
    color="#38a3a5"
)

test_particle_2 = p.Particle()
test_particle_2.radius=20
test_particle_2.position2 = (200, 100)
test_particle_2.velocity2 = (-100, 120)
test_particle_2.color="#780000"

objects = p.ParticleSystem(test_particle_1, test_particle_2, p.Particle(radius=20, init_position2=(screen.get_width()/2, screen.get_height()/2), init_velocity2=(0,0), mass=1))
player = objects.particles[2]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(window_color)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.velocity2.y = -500
        player.position2.y += player.velocity2.y*dt
    if keys[pygame.K_s]:
        player.velocity2.y = 500
        player.position2.y += player.velocity2.y*dt
    if keys[pygame.K_a]:
        player.velocity2.x = -500
        player.position2.x += player.velocity2.x*dt
    if keys[pygame.K_d]:
        player.velocity2.x = 500
        player.position2.x += player.velocity2.x*dt

    player.velocity2 = (0, 0)

    objects.update(screen, dt)


    dt = clock.tick()/1000
    pygame.display.flip()

