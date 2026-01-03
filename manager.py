import pygame
import object, tether, physics_object, abstract_drawable, abstract_physics

class Manager:
    def __init__(self):
        physics_objects = []
        static_objects = []
        tethers = []
        
        # GRID PATTERN
        #___________________________________________________________________________________________
        rows = 10
        columns = 20
        distance_x = 1280 / columns
        distance_y = 720 / rows
        grid = [[None for _ in range(rows)] for _ in range(columns)]
        for i in range(columns):
            for j in range(rows):
                if j == 0:
                    current_object = object.Object((i * distance_x, j))
                    grid[i][j] = current_object
                    static_objects.append(current_object)
                    continue
                current_object = physics_object.PhysicsObject((i * distance_x, j * distance_y))
                grid[i][j] = current_object
                physics_objects.append(current_object)
                tethers.append(tether.Tether((current_object, grid[i][j - 1])))
                if i != 0:
                    tethers.append(tether.Tether((current_object, grid[i - 1][j])))
        #____________________________________________________________________________________________

        # WREACKING BALL
        #___________________________________________________________________________________________
        # static_objects.append(object.Object((640, 0)))
        # links = 7
        # for i in range(links):
        #     physics_objects.append(physics_object.PhysicsObject((500 - i * 100, 50)))
        #     if i == 0:
        #         tethers.append(tether.Tether((static_objects[0], physics_objects[0])))
        #     else:
        #         tethers.append(tether.Tether((physics_objects[i - 1], physics_objects[i])))

        # physics_objects.append(physics_object.PhysicsObject((500 - links * 100, 0), 5))
        # tethers.append(tether.Tether((physics_objects[links - 1], physics_objects[links])))
        #____________________________________________________________________________________________
        
        self.objects = []
        self.objects += tethers
        self.objects += physics_objects
        self.objects += static_objects
    
    def draw(self, surface: pygame.Surface):
        # Draws and updates objects
        for object in self.objects:
            if isinstance(object, abstract_drawable.Drawable):
                object.render(surface)
            if isinstance(object, abstract_physics.Physics):
                object.act()

        # Rips tethers
        threshold = 400
        for object in self.objects:
            if isinstance(object, tether.Tether) and ((pygame.mouse.get_pressed()[0] and object.point_on_line(pygame.mouse.get_pos())) or object.get_length() > threshold):
                self.objects.remove(object)
