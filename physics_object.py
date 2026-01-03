import pygame
import object, abstract_physics, abstract_drawable

class PhysicsObject(object.Object, abstract_physics.Physics,abstract_drawable.Drawable):
    def __init__(self, position, mass = 1):
        super().__init__(position)
        self.velocity = (0.0, 0.0)
        self.mass = mass

        self.forces = [(0.0, 9.81)]

    def act(self):
        # Finds acceleration
        force_vector = self.calculate_force()
        acceleration_vector = (force_vector[0] / self.mass, force_vector[1] / self.mass)

        # Converts acceleration to position
        acceleration_damp = 0.15
        self.velocity = (self.velocity[0] + acceleration_vector[0] * acceleration_damp, self.velocity[1] + acceleration_vector[1] * acceleration_damp)
        self.position = (self.position[0] + self.velocity[0], self.position[1] + self.velocity[1])

        # Resets values and applies "drag"
        drag = 0.95
        self.velocity = (self.velocity[0] * drag, self.velocity[1] * drag)
        self.reset_forces()

    def apply_force(self, force):
        self.forces += force

    def reset_forces(self):
        self.forces = [(0.0, 9.81)]

    def calculate_force(self) -> tuple[float, float]:
        # Adds all forces up
        sum_force = (0.0, 0.0)
        for force in self.forces:
            sum_force = (sum_force[0] + force[0] * self.mass, sum_force[1] + force[1] * self.mass)
        return sum_force
    
    def render(self, surface):
        pygame.draw.circle(surface, pygame.Color(206, 107, 219), self.position , self.mass * 10)
    
    def get_velocity(self) -> tuple[float, float]:
        return self.velocity