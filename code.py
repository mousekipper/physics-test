import pygame
import math


class PhysicsEngine:
    def __init__(self):
        self.objects = []
        self.gravity = 0.5  
        self.friction = 0.99  

    def add_object(self, obj):
        self.objects.append(obj)

    def update(self):
        for obj in self.objects:
            
            obj.velocity[1] += self.gravity
            
            obj.velocity[0] *= self.friction
            obj.velocity[1] *= self.friction
          
            obj.position[0] += obj.velocity[0]
            obj.position[1] += obj.velocity[1]

            #
            if obj.position[1] >= 400 - obj.radius:
                obj.position[1] = 400 - obj.radius
                obj.velocity[1] = -obj.velocity[1]

            
            if obj.position[0] <= 0 + obj.radius or obj.position[0] >= 800 - obj.radius:
                obj.velocity[0] = -obj.velocity[0]


class PhysicsObject:
    def __init__(self, x, y, radius, color):
        self.position = [x, y]  
        self.velocity = [0, 0]  
        self.radius = radius  
        self.color = color  

    def apply_force(self, force):
        
        self.velocity[0] += force[0]
        self.velocity[1] += force[1]

    def reset(self):
        
        self.position = [400, 50]
        self.velocity = [0, 0]


pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()


font = pygame.font.SysFont("Arial", 24)


engine = PhysicsEngine()


ball = PhysicsObject(400, 50, 20, (255, 0, 0))
engine.add_object(ball)


time = 0


gravity_slider = 0.5  
friction_slider = 0.99  
velocity_slider = 0  


running = True
while running:
    screen.fill((255, 255, 255))  

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

  
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            
            if 50 <= mouse_x <= 250 and 320 <= mouse_y <= 340:
                gravity_slider = (mouse_x - 50) / 200
                engine.gravity = gravity_slider * 2 

      
            if 50 <= mouse_x <= 250 and 350 <= mouse_y <= 370:
                friction_slider = (mouse_x - 50) / 200
                engine.friction = friction_slider * 0.99 + 0.01  

           
            if 650 <= mouse_x <= 750 and 320 <= mouse_y <= 360:
                ball.reset()  


    engine.update()

   
    pygame.draw.circle(screen, ball.color, (int(ball.position[0]), int(ball.position[1])), ball.radius)
 
    time += 1
    velocity_text = f"Velocity: ({ball.velocity[0]:.2f}, {ball.velocity[1]:.2f})"
    position_text = f"Position: ({ball.position[0]:.2f}, {ball.position[1]:.2f})"
    time_text = f"Time: {time // 60}s {time % 60}ms"
    gravity_text = f"Gravity: {engine.gravity:.2f}"
    friction_text = f"Friction: {engine.friction:.2f}"


    screen.blit(font.render(velocity_text, True, (0, 0, 0)), (10, 10))
    screen.blit(font.render(position_text, True, (0, 0, 0)), (10, 40))
    screen.blit(font.render(time_text, True, (0, 0, 0)), (10, 70))
    screen.blit(font.render(gravity_text, True, (0, 0, 0)), (10, 100))
    screen.blit(font.render(friction_text, True, (0, 0, 0)), (10, 130))

   
    pygame.draw.rect(screen, (0, 0, 0), (50, 320, 200, 20))
    pygame.draw.rect(screen, (255, 0, 0), (50 + int(gravity_slider * 200), 320, 10, 20))
    screen.blit(font.render(f"Gravity: {gravity_slider * 2:.2f}", True, (0, 0, 0)), (270, 320))


    pygame.draw.rect(screen, (0, 0, 0), (50, 350, 200, 20))
    pygame.draw.rect(screen, (0, 255, 0), (50 + int(friction_slider * 200), 350, 10, 20))
    screen.blit(font.render(f"Friction: {friction_slider * 0.99 + 0.01:.2f}", True, (0, 0, 0)), (270, 350))


    pygame.draw.rect(screen, (0, 0, 255), (650, 320, 100, 40))
    screen.blit(font.render("Reset", True, (255, 255, 255)), (670, 330))

    pygame.display.flip()
    clock.tick(60)  

pygame.quit()
