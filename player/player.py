import pygame
import math

class Player:
    def __init__(self, pos_x, pos_y, width, height, move_speed, color):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.horizontal = 0
        self.vertical = 0
        self.last_frame_horizontal = 0
        self.last_frame_vertical = 0
        self.last_dash_horizontal = 0
        self.last_dash_vertical = 0
        self.move_speed = move_speed
        self.standard_speed = move_speed
        self.color = color
        self.dashing = False
        self.count = 0
        self.last_update = pygame.time.get_ticks()  # Store the last frame update time  

        self.frames_right = [
            pygame.transform.scale(pygame.image.load("player_frames/walk_right_1.png"), (64, 64)),
            pygame.transform.scale(pygame.image.load("player_frames/walk_right_2.png"), (64, 64)),
            pygame.transform.scale(pygame.image.load("player_frames/walk_right_3.png"), (64, 64)),
            pygame.transform.scale(pygame.image.load("player_frames/walk_right_4.png"), (64, 64))
        ]
        self.frames_left = [pygame.transform.flip(frame, True, False) for frame in self.frames_right]
        self.frames_down = [
            pygame.transform.scale(pygame.image.load("player_frames/walking_down_1.png"), (64, 64)),
            pygame.transform.scale(pygame.image.load("player_frames/walking_down_2.png"), (64, 64)),
            pygame.transform.scale(pygame.image.load("player_frames/walking_down_3.png"), (64, 64)),
            pygame.transform.scale(pygame.image.load("player_frames/walking_down_4.png"), (64, 64)),
        ]
        self.frames_up = [pygame.transform.scale(pygame.image.load("player_frames/walking_up.png"), (64, 64))]



    def draw(self, screen, dt):
        # pygame.draw.rect(screen, self.color, (self.pos_x, self.pos_y, self.width, self.height))

        current_frame = self.frames_right[1]

        if self.horizontal > 0:
            current_frame = self.frames_right[self.count]
        elif self.horizontal < 0:
            current_frame = self.frames_left[self.count]
        elif self.vertical > 0:
            current_frame = self.frames_down[self.count]
        elif self.vertical < 0:
            current_frame = self.frames_up[0]
        else:
            if self.last_frame_horizontal > 0:
                current_frame = self.frames_right[1]
            elif self.last_frame_horizontal < 0:
                current_frame = self.frames_left[1]
            elif self.last_frame_vertical > 0:
                current_frame = self.frames_down[1]
            elif self.last_frame_vertical < 0:
                current_frame = self.frames_up[0]
        

        screen.blit(current_frame, (self.pos_x, self.pos_y))

        if pygame.time.get_ticks() - self.last_update >= 100:
            if self.count < 3:
                self.count += 1
            else:
                self.count = 0
            self.last_update = pygame.time.get_ticks()

        self.get_input(dt, screen)

    def get_input(self, dt, screen):
        keys = pygame.key.get_pressed()

        if self.dashing == False:
            if keys[pygame.K_a]:
                self.horizontal = -1
                self.last_dash_horizontal = -1
                self.last_frame_horizontal = -1
                self.last_frame_vertical = 0
                if keys[pygame.K_w] == False and keys[pygame.K_s] == False:
                    self.last_dash_vertical = 0
            elif keys[pygame.K_d]:
                self.horizontal = 1
                self.last_dash_horizontal = 1
                self.last_frame_horizontal = 1
                self.last_frame_vertical = 0
                if keys[pygame.K_w] == False and keys[pygame.K_s] == False:
                    self.last_dash_vertical = 0
            else:
                self.horizontal = 0

            if keys[pygame.K_w]:
                self.vertical = -1
                self.last_dash_vertical = -1
                self.last_frame_vertical = -1
                self.last_frame_horizontal = 0
                if keys[pygame.K_a] == False and keys[pygame.K_d] == False:
                    self.last_dash_horizontal = 0
            elif keys[pygame.K_s]:
                self.vertical = 1
                self.last_dash_vertical = 1
                self.last_frame_vertical = 1
                self.last_frame_horizontal = 0
                if keys[pygame.K_a] == False and keys[pygame.K_d] == False:
                    self.last_dash_horizontal = 0
            else:
                self.vertical = 0

            if keys[pygame.K_LSHIFT] and self.dashing == False:
                self.move_speed *= 3
                self.dashing = True
        
        self.move(dt, screen)

    def move(self, dt, screen):
        if self.dashing == False:
            if self.horizontal and self.vertical:
                length = math.hypot(self.horizontal, self.vertical)
                self.horizontal /= length
                self.vertical /= length

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
        self.pos_x += self.last_dash_horizontal * self.move_speed * dt
        self.pos_y += self.last_dash_vertical * self.move_speed * dt