import pygame, math
import object, abstract_drawable, abstract_physics, physics_object

class Tether(abstract_drawable.Drawable, abstract_physics.Physics):
    def __init__(self, objects: tuple[object.Object, object.Object]):
        self.objects = objects
    
    def act(self):
        # Calculates x/y component distances
        distance_x = self.objects[1].get_position()[0] - self.objects[0].get_position()[0]
        distance_y = self.objects[1].get_position()[1] - self.objects[0].get_position()[1]
        forces = ((0.0, 0.0), (0.0, 0.0))

        distance = math.sqrt(pow(distance_x, 2) + pow(distance_y, 2))
        radius_of_stretch = 30 # How much slack the tether has
        if distance >= radius_of_stretch:
            total_force = 30
            theta = (math.atan2(distance_y, distance_x), math.atan2(-distance_y, -distance_x)) # Angle of tether
            damping_force = (distance - radius_of_stretch) * 0.03

            # Final forces applied
            forces = (
                (total_force * math.cos(theta[0]) * damping_force, total_force * math.sin(theta[0]) * damping_force),
                (total_force * math.cos(theta[1]) * damping_force, total_force * math.sin(theta[1]) * damping_force),
            )
        
        # Apply forces
        for i in range(2):
            if isinstance(self.objects[i], physics_object.PhysicsObject):
                self.objects[i].apply_force([forces[i]])

    def point_on_line(self, coordinate: tuple[int, int]) -> bool:
        # Gathers relevant points and vectors
        points = (self.objects[0].get_position(), self.objects[1].get_position())
        
        v = (points[1][0] - points[0][0], points[1][1] - points[0][1])
        u = (points[0][0] - coordinate[0], points[0][1] - coordinate[1])

        unit_v = math.sqrt(pow(v[0], 2) + pow(v[1], 2))

        # Calculates how far down the line is the closest point to the coordinate
        ratio_closest_point = abs((v[0] * u[0] + v[1] * u[1]) / pow(unit_v, 2))
        
        # Coordinates of the closest point
        closest_point = (points[0][0] + ratio_closest_point * v[0], points[0][1] + ratio_closest_point * v[1])

        # Checks that the point is on the line
        lowX = min(points[0][0], points[1][0])
        lowY = min(points[0][1], points[1][1])
        highX = max(points[0][0], points[1][0])
        highY = max(points[0][1], points[1][1])
        out_of_line = (closest_point[0] < lowX or closest_point[0] > highX) or (closest_point[1] < lowY or closest_point[1] > highY)
        if out_of_line:
            return False

        # Checks that the point is within a certain radius from the coordinate
        distance_to_point = math.sqrt(pow(coordinate[0] - closest_point[0], 2) + pow(coordinate[1] - closest_point[1], 2))
        radius = 20
        return distance_to_point <= radius

    def render(self, surface):
        pygame.draw.line(surface, pygame.Color(120, 87, 145, a=125), self.objects[0].get_position(), self.objects[1].get_position(), 5)

    def get_length(self) -> float:
        return math.sqrt(pow(self.objects[0].get_position()[0] - self.objects[1].get_position()[0], 2) + pow(self.objects[0].get_position()[1] - self.objects[1].get_position()[1], 2))
