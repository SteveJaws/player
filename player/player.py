import pygame

class Player:
    def __init__(self, pos_x, pos_y, width, height, move_speed, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.horizontal = 0
        self.vertical = 0
        self.last_horizontal = 0
        self.last_vertical = 0
        self.move_speed = move_speed
        self.standard_speed = move_speed
        self.color = color
        self.dashing = False

    def draw(self, screen, dt):
        pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, self.width, self.height))

        self.get_input(dt, screen)

    def get_input(self, dt, screen):
        keys = pygame.key.get_pressed()

        if self.dashing == False:
            if keys[pygame.K_a]:
                self.horizontal = -1
                self.last_horizontal = -1
                if keys[pygame.K_w] == False and keys[pygame.K_s] == False:
                    self.last_vertical = 0
            elif keys[pygame.K_d]:
                self.horizontal = 1
                self.last_horizontal = 1
                if keys[pygame.K_w] == False and keys[pygame.K_s] == False:
                    self.last_vertical = 0
            else:
                self.horizontal = 0

            if keys[pygame.K_w]:
                self.vertical = -1
                self.last_vertical = -1
                if keys[pygame.K_a] == False and keys[pygame.K_d] == False:
                    self.last_horizontal = 0
            elif keys[pygame.K_s]:
                self.vertical = 1
                self.last_vertical = 1
                if keys[pygame.K_a] == False and keys[pygame.K_d] == False:
                    self.last_horizontal = 0
            else:
                self.vertical = 0

            if keys[pygame.K_LSHIFT] and self.dashing == False:
                self.move_speed *= 3
                self.dashing = True
        
        self.move(dt, screen)

    def move(self, dt, screen):
        if self.dashing == False:
            if self.horizontal != 0 and self.vertical != 0:
                self.horizontal *= 0.7
                self.vertical *= 0.7

            self.pos_x += self.horizontal * self.move_speed * dt
            self.pos_y += self.vertical * self.move_speed * dt
        else:
            if self.move_speed > self.standard_speed:
                self.move_speed -= self.move_speed * 0.05
            else:
                self.move_speed = self.standard_speed
                self.dashing = False
            self.dash(dt, screen)


    def dash(self, dt, screen):
        self.pos_x += self.last_horizontal * self.move_speed * dt
        self.pos_y += self.last_vertical * self.move_speed * dt