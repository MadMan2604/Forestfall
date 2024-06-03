import pygame 
import math 
import os 
import random 

from scripts.settings import * 
from scripts.entities import PhysicsEntity
from scripts.particle import Particle

class AIEnemy(PhysicsEntity):
    def __init__(self, game, pos, size, player):
        super().__init__(game, 'enemy', pos, size)
        self.air_time = 0
        self.jumps = 2
        self.wall_slide = False
        self.health = 200
        self.bar_length = 210
        self.dashing = 0
        self.target_player = player  # reference to the player object
        self.attacking = False


    def draw_health_bar(self, screen):
        # Same as Player class
        pass


    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)

        self.air_time += 1

        if self.air_time > 1000:
            self.game.dead += 1

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 2

        self.wall_slide = False
        if (self.collisions['right'] or self.collisions['left']) and self.air_time > 4:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True

            self.set_action('wall_slide')
            
            if not self.wall_slide:
                if self.air_time > 4:
                    self.set_action('jump')
                elif movement[0] != 0:
                    self.set_action('run')
                else:
                    self.set_action('idle')
            
            if abs(self.dashing) in {60, 50}:
                for i in range(20):
                    angle = random.random() * math.pi * 2
                    speed = random.random() * 0.5 + 0.5
                    pvelocity = [math.cos(angle) * speed, math.sin(angle) * speed]
                    #self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
                    self.game.particles.append(Particle(self.game, 'particle1', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))


            if self.dashing:
                self.stamina -= 1
            if self.dashing == 0 and self.stamina < 200:
                self.stamina += 5
            if self.stamina == 0 and self.stamina < 200:
                self.stamina += 5


            if self.dashing > 0:
                self.dashing = max(0, self.dashing - 1)
            if self.dashing < 0:
                self.dashing = min(0, self.dashing + 1)
            if abs(self.dashing) > 50:
                self.velocity[0] = abs(self.dashing) / self.dashing * 8
                if abs(self.dashing) == 51:
                    self.velocity[0] *= 0.1
                pvelocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
                #self.game.particles.append(Particle(self.game, 'particle', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
                self.game.particles.append(Particle(self.game, 'particle1', self.rect().center, velocity=pvelocity, frame=random.randint(0, 7)))
                    
            if self.velocity[0] > 0:
                self.velocity[0] = max(self.velocity[0] - 0.1, 0)
            else:
                self.velocity[0] = min(self.velocity[0] + 0.1, 0)
            # ...

        # Attacking Logic
        self.attacking = self.is_near_player()  # Replace this with your attack logic

        if self.attacking:
            # Perform attack animation and deal damage to player
            self.game.sfx['enemy_attack'].play()  # Add sound effect
            self.player.health -= 10  # Replace with your damage calculation

    def render(self, surf, offset=(0, 0)):
        if abs(self.dashing) <= 50:
            super().render(surf, offset=offset)

    def jump(self):
        # Same as Player class
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
                
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.air_time = 5
            return True

    def dash(self):
        # Same as Player class (might need adjustments for AI behavior)
        if not self.dashing:
            self.game.sfx['dash'].play()
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60


    def is_near_player(self):
        # Implement logic to check if the player is within attack range
        distance_x = abs(self.rect.centerx - self.target_player.rect.centerx)
        distance_y = abs(self.rect.centery - self.target_player.rect.centery)
        return distance_x < 100 and distance_y < 50  # Adjust these values based on your game

# create the ai chatgpt powered ai enemy that is a mirror image of the player with the additions of some powers & abilities 