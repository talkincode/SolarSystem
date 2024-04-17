import math
import random
import pygame
from .common import Scene, Colors, get_assets, DISPLAY_WIDTH, DISPLAY_HEIGHT, res_manager
from .actors import Background, Meteor, ShockParticle, Star, ImageSprite, EarthTrailSprite, HMoveBackground
from .config import configmap


class EarthMoveScene(Scene):

    __name__ = "EarthMoveScene"

    def __init__(self, manager, clock):
        super().__init__(manager)
        self.clock = clock

    def on_enter(self, **kwargs):
        self.background = HMoveBackground(config_data=configmap["hbackground"])
        self.earth = ImageSprite(
            200,
            DISPLAY_WIDTH,
            DISPLAY_HEIGHT // 2,
            get_assets("images/earth_big.webp"),
            True,
        )

        self.planets = pygame.sprite.Group(
            self.earth,
        )

        self.all_bodies = pygame.sprite.Group(self.background)        
        self.frame_count = 0
        
        self.moving_up = False
        self.moving_down = False
        
        self.METEOR_EVENT = pygame.USEREVENT + 10
        pygame.time.set_timer(self.METEOR_EVENT, 5000)
        
        self.meteor_group = pygame.sprite.Group()
        self.shock_particles = pygame.sprite.Group()
        
        self.play_bgm()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == self.METEOR_EVENT:
                for _ in range(random.choice([1,2,3,4])):
                    meteor = Meteor(
                        random.choice(["meteor_shard"]), configmap["meteor"]
                    )
                    self.meteor_group.add(meteor)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.manager.switch_scene("SolarSystemScene")
                    return
                if event.key == pygame.K_2:
                    self.manager.switch_scene("SolarProbeScene")
                    return
                elif event.key == pygame.K_UP:
                    self.moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.moving_down = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.moving_down = False

    def create_hit_shock_particle(self, actor_obj, num):
        blast_sound = res_manager.load_sound("sounds/fire_blast.ogg")
        blast_sound.play()
        for _ in range(int(num)):
            particle = ShockParticle(
                actor_obj.rect.x + actor_obj.rect.width // 2,
                actor_obj.rect.y + actor_obj.rect.height // 2,
                random.choice([Colors.orange_light, Colors.orange, Colors.yellow]),
                speed=1.8,
            )
            self.shock_particles.add(particle)

    def custom_collision(self, sprite1, sprite2):
        # 计算两个精灵中心点之间的距离
        distance = math.hypot(sprite1.rect.centerx - sprite2.rect.centerx, sprite1.rect.centery - sprite2.rect.centery)
        # 判断距离是否小于或等于100像素
        return distance <= (sprite1.rect.width + sprite2.rect.width -35) // 2

    def update(self):
        self.all_bodies.update()
        self.planets.update()
        self.meteor_group.update()
        self.shock_particles.update()
        
        if self.moving_up:
            self.earth.move_y(-1, 8)  # 移动速度为每帧4像素
        if self.moving_down:
            self.earth.move_y(1, 8)   # 移动速度为每帧4像素
        
        if self.frame_count % 5 == 0:
            for i in range(10):  # 创建5个波浪，每个波浪的延迟递增
                wave_delay = i * 120  # 每个波浪之间有20帧的延迟
                trail = EarthTrailSprite(self.earth.rect.center, size=(5,5), delay=wave_delay)
                self.all_bodies.add(trail)
            for i in range(10):  
                wave_delay = i * 240 
                trail = EarthTrailSprite(self.earth.rect.center, size=(3,3), delay=wave_delay)
                self.all_bodies.add(trail)
            for i in range(10):  
                wave_delay = i * 60 
                trail = EarthTrailSprite(self.earth.rect.center, size=(5,5), delay=wave_delay)
                self.all_bodies.add(trail)
        self.frame_count += 1
        
        if self.earth.rect.centerx >= DISPLAY_WIDTH // 2:
            self.earth.rect.x -= 1
        
        collisions = pygame.sprite.groupcollide(
            self.planets, self.meteor_group, False, True, collided=self.custom_collision
        )
        for myb, ubs in collisions.items():
            for ub in ubs:
                self.create_hit_shock_particle(ub, 100)
        
        

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.all_bodies.draw(screen)
        self.planets.draw(screen)
        self.meteor_group.draw(screen)
        self.shock_particles.draw(screen)

    def on_exit(self, **kwargs):
        pass

    def play_bgm(self):
        """播放背景音乐""" ""
        pygame.mixer.music.load(get_assets(configmap["bgm"]["sound"]))
        pygame.mixer.music.set_volume(configmap["bgm"]["sound_volume"])
        pygame.mixer.music.play(-1)
