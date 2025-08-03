from utils import resource_path
import pygame

class Card:
    def __init__(self, colour, number, pos):
        self.colour = colour
        self.number = number
        self.image = self.load_image()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)

        # Animation state
        self.animating = False
        self.start_pos = None
        self.target_pos = None
        self.animation_start_time = 0
        self.animation_duration = 500  # ms

    def load_image(self):
        path = resource_path(f"Uno/individual/{self.colour}/{self.number}_{self.colour}.png")
        return pygame.transform.scale(pygame.image.load(path), (75, 105)).convert_alpha()

    def matches(self, other_card):
        return self.colour == other_card.colour or self.number == other_card.number

    def start_animation(self, target_pos):
        self.animating = True
        self.start_pos = self.pos[:]
        self.target_pos = target_pos
        self.animation_start_time = pygame.time.get_ticks()

    def update_animation(self):
        if self.animating:
            now = pygame.time.get_ticks()
            elapsed = now - self.animation_start_time
            duration = self.animation_duration

            t = min(elapsed / duration, 1)  # Normalized time from 0 to 1

            # Linear interpolation
            self.pos[0] = self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * t
            self.pos[1] = self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * t
            self.rect.topleft = self.pos

            if t >= 1:
                self.animating = False

    def __repr__(self):
        return f"{self.colour} {self.number}"