import os
import sys
import math
import random
import pygame
import json 

from scripts.utils import load_image, load_images, Animation
from scripts.entities import PhysicsEntity, Player, Enemy, NPC1, NPC2
from scripts.ai_enemy import AIEnemy
from scripts.portals import Portals
from scripts.tilemap import Tilemap
#from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.settings import * 
from states.base_state import BaseState
from scripts.rect_button import RectButton
#from scripts.grass import GrassManager
from scripts.animated_button import AnimatedButton

# this is the portal class using the particles class as reference 


class InGame(BaseState):

    def __init__(self, game):
        super().__init__(game)
        pygame.display.set_caption('')
        self.screen = self.game.screen
        self.display = pygame.Surface((WIDTH / 5, HEIGHT / 5))
        
        self.clock = pygame.time.Clock()
        self.pause = False
        self.movement = [False, False]
        self.assets = {
            'decor': load_images('tiles/decor'),
            'buildings': load_images('tiles/buildings'),
            'trees': load_images('tiles/trees'),
            'cave_stone': load_images('tiles/cave_stone'),
            'alt_grass': load_images('tiles/alt_grass'), 
            'alt_large_decor_1': load_images('tiles/alt_large_decor_1'),
            'signposts': load_images('tiles/signposts'),
            'bridge': load_images('tiles/bridge'),
            'grass': load_images('tiles/grass'),
            'grass2': load_images('tiles/grass2'),
            'brick': load_images('tiles/brick'),
            #'jungle_bg_tiles': load_images('tiles/jungle_bg'),
            'dirt': load_images('tiles/dirt'),
            'large_decor': load_images('tiles/large_decor'),
            'bgstone': load_images('tiles/bgtiles'),
            'player': load_image('entities/player.png'),
            #'weeds': load_images('tiles/weeds'),
            'portal/idle': Animation(load_images('entities/portal'), img_dur=6),
            'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
            'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
            'player/idle': Animation(load_images('entities/player/idle'), img_dur=2),
            'player/run': Animation(load_images('entities/player/run'), img_dur=6),
            'player/jump': Animation(load_images('entities/player/jump')),
            'player/slide': Animation(load_images('entities/player/slide')),
            'player/wall_slide': Animation(load_images('entities/player/wall_slide')),
            'npc1/idle': Animation(load_images('entities/npc1/idle'), img_dur=6),
            'npc1/run': Animation(load_images('entities/npc1/run'), img_dur=4),
            'npc2/idle': Animation(load_images('entities/npc2/idle'), img_dur=6),
            'npc2/run': Animation(load_images('entities/npc2/run'), img_dur=4),
            #'aienemy/idle': Animation(load_images('entities/aienemy/idle'), img_dur=2),
            #'aienemy/run': Animation(load_images('entities/aienemy/run'), img_dur=6),
            #'aienemy/jump': Animation(load_images('entities/aienemy/jump')),
            #'aienemy/slide': Animation(load_images('entities/aienemy/slide')),
            #'aienemy/wall_slide': Animation(load_images('entities/aienemy/wall_slide')),
            #'npc3/idle': Animation(load_images('entities/npc3/idle'), image_dur=6),
            #'npc3/run': Animation(load_images('entities/npc3/run'), img_dur=4),
            #'npc4/idle': Animation(load_images('entities/npc4/idle'), image_dur=6),
            #'npc4/run': Animation(load_images('entities/npc4/run'), img_dur=4),
            'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
            'particle/cherry_leaf': Animation(load_images('particles/cherry_leaf'), img_dur=20, loop=False),
            'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
            'particle/particle1': Animation(load_images('particles/particle1'), img_dur=6, loop=False),
            'bow': load_image('bow.png'),
            'arrow': load_image('arrow.png'),
            'speech_bubble': load_image('speech_bubble.png'),
            
        }
        # music initialisation
        self.level1_music = 'data/music/forest_ambience.mp3'
        self.level2_music = 'data/music/Decayed_in_the_Darkness.mp3'

        self.sfx = {
            'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
            'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
            'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
        }

        self.cursor = pygame.image.load('data/images/cursor.png').convert_alpha()
        self.cursor = pygame.transform.scale(self.cursor, (32, 32))

        # speech bubble icon
        self.interaction_icon = pygame.image.load('data/images/speech_bubble.png')
        self.interaction_icon = pygame.transform.scale(self.interaction_icon, (32, 32))

        
        # load music for each level
        self.level_music_objects = {}

        self.sfx['ambience'].set_volume(0.7)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['hit'].set_volume(0.2)
        
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)
        
        # Assuming you have at least one signpost image loaded
        self.level = 0
        alt_level = 'alt'
        self.alt_level = alt_level
        self.load_level(self.level)
        self.screenshake = 0

        # the backgrounds
        self.background1 = pygame.image.load(BACKGROUND_PATH + 'bg1.png')
        self.background2 = pygame.image.load(BACKGROUND_PATH + 'bg2.png')
        self.alt_background = pygame.image.load(BACKGROUND_PATH + 'altbg.png')
        self.background3 = pygame.image.load(BACKGROUND_PATH + 'bg3.png')
        

        # the speech icon 
        self.speech_bubble = pygame.image.load('data/images/speech_bubble.png')


    def load_level(self, map_id):
        self.tilemap.load('data/maps/' + str(map_id) + '.json')

        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        for tree in self.tilemap.extract([('trees', 0)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        for tree in self.tilemap.extract([('trees', 4)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        
        self.cherry_leaf_spawners = []
        for tree in self.tilemap.extract([('trees', 3)], keep=True):
            self.cherry_leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))
        
            
        self.enemies = []
        self.ai_enemies = []
        self.npcs = []
        self.portals = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1), ('spawners', 2), ('spawners', 3), ('spawners', 4), ('spawners', 5)]):
            if spawner['variant'] == 0:
                self.player.pos = spawner['pos']
                self.player.air_time = 0
            elif spawner['variant'] == 1:
                self.enemies.append(Enemy(self, spawner['pos'], (6, 15)))
            elif spawner['variant'] == 2:
                self.npcs.append(NPC1(self, spawner['pos'], (8, 15)))
            elif spawner['variant'] == 3:
                self.npcs.append(NPC2(self, spawner['pos'], (8, 15)))
            elif spawner['variant'] == 4:
                #self.portals.append(Portals(self, 'portal', spawner['pos'], velocity=[0, 0], frame=random.randint(0, 7)))
                self.portals.append(Portals(self, spawner['pos'], (65, 65)))
            elif spawner['variant'] == 5:
                self.ai_enemies.append(AIEnemy(self, spawner['pos'], (8, 15)))


       
        self.projectiles = []
        self.particles = []
        self.sparks = []
        
        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30

    
    # function that loads the minimap at the top right of the screen
    def draw_map_icon(self, screen):
        pass 
  

    def update(self, events):
        
        

        # get the mouse position
        # the arpg mouse cursor image 
        pygame.mouse.set_visible(False)


        
        if self.level == 0:
            pygame.mixer.music.load(self.level1_music)
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        self.pause = False 
        self.perk_menu = False 

        while True:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.movement[0] = True
                    if event.key == pygame.K_d:
                        self.movement[1] = True
                    if event.key == pygame.K_SPACE:
                        self.player.jump()
                    if event.key == pygame.K_LSHIFT:
                        self.player.dash()
                    if event.key == pygame.K_ESCAPE:
                        self.pause = not self.pause
                    if event.key == pygame.K_TAB:
                        self.perk_menu = not self.perk_menu
                        
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                
                click = pygame.mouse.get_pressed()
                if click[0]:
                    self.player.dash()
                
           
            
            if self.pause == False and self.perk_menu == False:
                if self.level == 0:
                    self.display.blit(self.background1, (0, -100))
                if self.level == 1:
                    self.display.blit(self.background2, (0, 0))
                if self.alt_level == True:
                    self.display.blit(self.alt_background, (0, 0))
                if self.level == 2:
                    self.display.blit(self.background3, (0, 0))
                
                

                # if the number of enemies in the map = 0, the level transition plays and the next level loads
                if not len(self.enemies):
                    self.transition += 1
                    if self.transition > 30:
                        self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                        self.load_level(self.level)
                if self.transition < 0:
                    self.transition += 1
                

                if self.dead:
                    self.dead += 1
                    if self.dead >= 10:
                        self.transition = min(30, self.transition - 1)
                    if self.dead > 40:
                        
                        self.player.health = 200
                        self.player.stamina = 200
                
                self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
                self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
                render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
                
                for rect in self.leaf_spawners:
                    if random.random() * 49999 < rect.width * rect.height:
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
                
                for rect in self.cherry_leaf_spawners:
                    if random.random() * 49999 < rect.width * rect.height:
                        pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                        self.particles.append(Particle(self, 'cherry_leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
                
                self.tilemap.render(self.display, offset=render_scroll)
                

               
                
                for enemy in self.enemies.copy():
                    kill = enemy.update(self.tilemap, (0, 0))
                    enemy.render(self.display, offset=render_scroll)
                    if kill:
                        self.enemies.remove(enemy)
                        self.player.points += 3
                
                for npc in self.npcs.copy():
                    npc.update(self.tilemap, (0, 0))
                    npc.render(self.display, offset=render_scroll)
                
                if not self.dead:
                    self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                    self.player.render(self.display, offset=render_scroll)
                
                for portal in self.portals.copy():
                    portal.update(self.tilemap, (0, 0))
                    portal.render(self.display, offset=render_scroll)
                    
                
                for projectile in self.projectiles.copy():
                    projectile[0][0] += projectile[1]
                    projectile[2] += 1
                    img = self.assets['arrow']
                    self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                    if self.tilemap.solid_check(projectile[0]):
                        self.projectiles.remove(projectile)
                        for i in range(4):
                            self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                    elif projectile[2] > 360:
                        self.projectiles.remove(projectile)
                    elif abs(self.player.dashing) < 50:
                        if self.player.rect().collidepoint(projectile[0]):
                            self.projectiles.remove(projectile)
                            self.player.health -= 12
                            if self.player.health < 0:
                                self.load_level(0)
                            self.screenshake = max(16, self.screenshake)
                            for i in range(30):
                                angle = random.random() * math.pi * 2
                                speed = random.random() * 5
                                self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                                #self.particles.append(Particle(self, 'particle', self.player.rect().center, velocity=[math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame=random.randint(0, 7)))
                            
                for spark in self.sparks.copy():
                    kill = spark.update()
                    spark.render(self.display, offset=render_scroll)
                    if kill:
                        self.sparks.remove(spark)
                
                for particle in self.particles.copy():
                    kill = particle.update()
                    particle.render(self.display, offset=render_scroll)
                    if particle.type == 'leaf':
                        particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                    if kill:
                        self.particles.remove(particle)
                         
                if self.transition:
                    transition_surf = pygame.Surface(self.display.get_size())
                    pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                    transition_surf.set_colorkey((255, 255, 255))
                    self.display.blit(transition_surf, (0, 0))
                
                screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)
                self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), screenshake_offset)
                
                
                self.screenshake = max(0, self.screenshake - 1)

                x, y = pygame.mouse.get_pos()
                self.screen.blit(self.cursor, (x, y))

                #self.points_text = self.game.font5.render('{self.player.points}', True, WHITE)
                #self.game.screen.blit(self.points_text, (13, 602))

                self.player.draw_health_bar(self.screen)
                self.player.draw_stamina_bar(self.screen)
                self.player.draw_icon(self.screen)
                self.player.draw_points_box(self.screen)

              
                pygame.display.update()
                self.clock.tick(60)
            
            if self.pause == True:
                
                pygame.mouse.set_visible(True)
                # the pause menu screen 
                self.pause_surf = pygame.Surface((WIDTH, HEIGHT))
                self.pause_surf.fill((65, 72, 89))
                self.pause_surf.set_alpha(15) # sets the transparrency of the background

                

                resume_button = RectButton(self.pause_surf, DARK_CYAN, 100, 250, 192, 51, "Resume", WHITE, self.game.font5)
                restart_button = RectButton(self.pause_surf, DARK_CYAN, 100, 350, 192, 51, "Restart", WHITE, self.game.font5)
                options_button = RectButton(self.pause_surf, DARK_CYAN, 100, 450, 192, 51, "Options", WHITE, self.game.font5)
                quit_button = RectButton(self.pause_surf, DARK_CYAN, 100, 550, 192, 51, "Quit", WHITE, self.game.font5)


                if resume_button.is_clicked():
                    self.pause = not self.pause # resume the game
                    pygame.mouse.set_visible(False)
                if restart_button.is_clicked():
                    self.level = 0
                    self.load_level(0) # restarts the run from the very first room 
                    self.player.health = 200
                    self.player.stamina = 200
                    self.pause = not self.pause # closes the pause menu to restart the game 
                if options_button.is_clicked():
                    self.game.state_manager.change_state("options_menu") # open the options menu 
                if quit_button.is_clicked():
                    pygame.quit() # quit the game 
                    sys.exit()
                

           
                resume_button.draw()
                restart_button.draw()
                options_button.draw()
                quit_button.draw()

                self.screen.blit(self.pause_surf, (0, 0)) # load the menu onto the screen using an alpha mask

                pygame.display.update()

            if self.perk_menu == True:

                pygame.mouse.set_visible(True)

                # perk menu gfx setup 
                self.perk_surf = pygame.Surface((WIDTH, HEIGHT))
                self.perk_surf.fill((0, 0, 0))
                self.perk_surf.set_alpha(15) # the transparency effect for the background

                self.screen.blit(self.perk_surf, (0, 0))






               
            
            
