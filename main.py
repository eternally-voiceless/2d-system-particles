import pygame
import numpy
import time
from objects.system_of_particles.particle import Particle, ParticleSystem

def rand_int(lower_range_limit: int=10, upper_range_limit: int=100):
    return numpy.random.randint(lower_range_limit, upper_range_limit)

pygame.init()

window_color = "#F0EBD8"
window_size = window_width, window_height = 1280, 720
screen = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()
dt = 0

center_position = pygame.Vector2(screen.get_width()/2, screen.get_height()/2)

test_system = ParticleSystem()
particles = []
for i in range(200):
    particles.append(Particle(
        radius=10, 
        init_position2=(rand_int(100, 300), rand_int(100, 700)), 
        init_velocity2=(rand_int(-200, 200), rand_int(-2000, 2000))
        ))
    
for i in range(80):
    particles.append(Particle(
        radius=20,
        init_position2=(rand_int(900, 1200), rand_int(100, 700)),
        init_velocity2=(rand_int(-200, 200), rand_int(-2000, 2000)),
        mass=20,
        color="#c1121f"
    ))

test_system.add(*particles)

#test_system.particles[0].color="#c1121f"
#test_system.particles[0].mass=10
#test_system.particles[1].color="#c1121f"
#test_system.particles[1].mass=10

def update(surface: pygame.Surface, ps: ParticleSystem, dt):
    for part in ps.particles:
        part.check_border_collision(surface)
    ps.update(surface, dt)

#time.sleep(3)
    
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    #main code
    # ----------------------------------------
    screen.fill(window_color)
    
    update(screen, test_system, dt)


    test_system.particles[0].print_velocity(end=" | ")
    test_system.particles[1].print_velocity(end=" | ")
    print(numpy.round(test_system.mean_of_squared_velocities()))
    #part1.print_position(end=" | ")
    #part1.print_velocity(end=" | ")
    #part2.print_velocity()
    # ----------------------------------------
    # mean_velocity_check = numpy.round(test_system.mean_of_squared_velocities())
    # if mean_velocity_check<400 or mean_velocity_check>1000: break
    # ----------------------------------------

    dt = clock.tick()/10000
    pygame.display.flip()

pygame.quit()