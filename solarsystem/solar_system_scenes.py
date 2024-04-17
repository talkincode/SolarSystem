import random
import pygame
from .common import Scene, Colors, get_assets
from .actors import Background, CelestialBody, Star
from .config import configmap


class SolarSystemScene(Scene):

    __name__ = "SolarSystemScene"

    def __init__(self, manager, clock):
        super().__init__(manager)
        self.clock = clock


    def on_enter(self, **kwargs):
        self.background = Background(config_data=configmap["background"])
        self.sun = CelestialBody.create_sun()
        self.mercury = CelestialBody.create_planet("mercury", self.sun)
        self.venus = CelestialBody.create_planet("venus", self.sun)
        self.earth = CelestialBody.create_planet("earth", self.sun)
        self.mars = CelestialBody.create_planet("mars", self.sun)
        self.jupiter = CelestialBody.create_planet("jupiter", self.sun)
        self.saturn = CelestialBody.create_planet("saturn", self.sun)
        self.uranus = CelestialBody.create_planet("uranus", self.sun)
        self.neptune = CelestialBody.create_planet("neptune", self.sun)
        self.planets = pygame.sprite.Group(
            self.mercury,
            self.venus,
            self.earth,
            self.mars,
            self.jupiter,
            self.saturn,
            self.uranus,
            self.neptune,
            self.sun,
        )

        self.all_bodies = pygame.sprite.Group(self.background)
        for _ in range(20):
            self.all_bodies.add(Star())

        self.play_bgm()
        

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_2:
                    self.manager.switch_scene("SolarProbeScene")
                    return
                if event.key == pygame.K_3:
                    self.manager.switch_scene("EarthMoveScene")
                    return

    def update(self):
        self.all_bodies.update()
        self.planets.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.all_bodies.draw(screen)
        for planet in self.planets:  # Assuming 'planets' is your list or group of CelestialBody instances
            planet.trail_group.draw(screen)
        
        self.planets.draw(screen)
        


    def on_exit(self, **kwargs):
        pass


    def play_bgm(self):
        """播放背景音乐""" ""
        pygame.mixer.music.load(get_assets(configmap["bgm"]["sound"]))
        pygame.mixer.music.set_volume(configmap["bgm"]["sound_volume"])
        pygame.mixer.music.play(-1) 