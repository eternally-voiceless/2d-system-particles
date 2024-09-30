import re
import pygame
import numpy
import itertools

class Particle (pygame.sprite.Sprite):
    """Representing a simple physical round particle"""
    def __init__(self, radius: float = 10, init_position2: pygame.Vector2 = (0,0), init_velocity2: pygame.Vector2 = (0,0), mass: float=1, color: str = "#3E5C76"):
        super().__init__()
        self.__mass = mass
        self.__radius = radius
        self.__color = color
        self.__position2 = pygame.Vector2(init_position2)
        self.__velocity2 = pygame.Vector2(init_velocity2)

    # ------------------------------------------------------------------------
    def update(self, surface: pygame.Surface, dt: float):
        self.x += self.velocity_x*dt
        self.y += self.velocity_y*dt
        self.check_border_collision(surface)
        pygame.draw.circle(surface, self.color, self.position2, self.radius, width=0)

    def check_border_collision(self, surface: pygame.Surface):
        delta = 0.1
        if self.x <= self.radius:
            self.velocity_x = -self.velocity_x
            self.x = self.radius + delta
        if self.x >= surface.get_width()-self.radius:
            self.velocity_x = -self.velocity_x
            self.x = surface.get_width()-self.radius-delta
        if self.y <= self.radius:
            self.velocity_y = -self.velocity_y
            self.y = self.radius + delta
        if self.y >= surface.get_height()-self.radius:
            self.velocity_y = -self.velocity_y
            self.y = surface.get_height()-self.radius-delta

    def handle_collisions(self, particle: 'Particle'):
        delta = 0.2
        mass_1, mass_2 = self.mass, particle.mass
        v1: numpy.ndarray = self.velocity2
        v2: numpy.ndarray = particle.velocity2
        r1: numpy.ndarray = self.position2
        r2: numpy.ndarray = particle.position2

        v1_normal: float = numpy.dot(v1, r2-r1)/numpy.linalg.norm(r2-r1)
        v2_normal: float = numpy.dot(v2, r1-r2)/numpy.linalg.norm(r1-r2)
        
        v1_tangential: numpy.ndarray = v1-v1_normal/numpy.linalg.norm(r2-r1)*(r2-r1)
        v2_tangential: numpy.ndarray = v2-v2_normal/numpy.linalg.norm(r1-r2)*(r1-r2)

        radius_1: float = self.radius
        radius_2: float = particle.radius
        while distance_between_two_particles(self, particle)<radius_1+radius_2:
            r=r1-r2
            r1 += delta/numpy.linalg.norm(r)*r
            r2 -= delta/numpy.linalg.norm(r)*r
            self.position2, particle.position2 = r1, r2

        v1_new_normal: numpy.ndarray = (mass_2*(v1_normal+2*v2_normal)-mass_1*v1_normal)/(mass_1+mass_2)/numpy.linalg.norm(r1-r2)*(r1-r2)
        v2_new_normal: numpy.ndarray = (mass_1*(2*v1_normal+v2_normal)-mass_2*v2_normal)/(mass_1+mass_2)/numpy.linalg.norm(r2-r1)*(r2-r1)

        v1_new_tangential: numpy.ndarray = v1_tangential
        v2_new_tangential: numpy.ndarray = v2_tangential

        v1_new: numpy.ndarray = v1_new_normal+v1_new_tangential
        v2_new: numpy.ndarray = v2_new_normal+v2_new_tangential

        self.velocity2 = pygame.Vector2(v1_new[0], v1_new[1])
        particle.velocity2 = pygame.Vector2(v2_new[0], v2_new[1])
        

        

    def print_position(self, end: str="\n"):
        print(self.position2, end=end)

    def print_velocity(self, end: str="\n"):
        print(self.velocity2, end=end)

    @property
    def x(self):
        return self.__position2.x
    @x.setter
    def x(self, coord_x: float):
        self.__position2.x = coord_x

    @property
    def y(self):
        return self.__position2.y
    @y.setter
    def y(self, coord_y: float):
        self.__position2.y = coord_y

    @property
    def position2(self):
        return self.__position2
    @position2.setter
    def position2(self, coord: tuple[float, float]):
        self.__position2.x, self.__position2.y = coord

    @property
    def velocity_x(self):
        return self.__velocity2.x
    @velocity_x.setter
    def velocity_x(self, vel_x_value: float):
        self.__velocity2.x = vel_x_value
    
    @property
    def velocity_y(self):
        return self.__velocity2.y
    @velocity_y.setter
    def velocity_y(self, vel_x_value: float):
        self.__velocity2.y = vel_x_value

    @property
    def velocity2(self):
        return self.__velocity2
    @velocity2.setter
    def velocity2(self, vel_value: tuple[float, float]):
        self.__velocity2.x, self.__velocity2.y = vel_value

    @property
    def color(self):
        return self.__color
    @color.setter
    def color(self, color_code: str):
        if bool(re.match(r'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})', color_code)):
            self.__color = color_code

    @property
    def radius(self):
        return self.__radius
    @radius.setter
    def radius(self, radius_value: float):
        if radius_value>=0:
            self.__radius = radius_value

    @property
    def mass(self):
        return self.__mass
    @mass.setter
    def mass(self, mass_value: float):
        if mass_value>0:
            self.__mass = mass_value

def distance_between_two_particles(p1: Particle, p2: Particle)->float:
    return (p1.position2-p2.position2).magnitude()

class ParticleSystem:
    def __init__(self, *args: Particle):
        self.__particles: list[Particle] = [part for part in args]

    @property
    def particles(self):
        return self.__particles
    
    def add(self, *args: Particle):
        for p in args:
            self.particles.append(p)
    
    def __collision_detection(self)->bool:
        #max_radius: float = max([p.radius for p in self.particles])
        for p1, p2 in list(itertools.combinations(self.particles, 2)):
            if distance_between_two_particles(p1, p2)<=p1.radius+p2.radius:
                p1.handle_collisions(p2)

    def update(self, surface: pygame.Surface, dt: float):
        self.__collision_detection()
        for p in self.particles:
            p.update(surface, dt)

    def mean_of_squared_velocities(self):
        particle_velocities = [p.velocity2 for p in self.particles]
        squared_velocities = numpy.array([v.as_polar()[0]**2 for v in particle_velocities])
        sum_of_squared_velocities = numpy.sum(squared_velocities)
        number_of_particles = len(self.particles)
        mean_value = sum_of_squared_velocities/number_of_particles
        return numpy.sqrt(mean_value)