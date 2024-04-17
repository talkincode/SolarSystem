import random
import pygame
from .common import Scene, Colors, get_assets, DISPLAY_WIDTH, DISPLAY_HEIGHT
from .actors import Background, Star, ImageSprite, SuperProbe
from .config import configmap


class SolarProbeScene(Scene):

    __name__ = "SolarProbeScene"

    def __init__(self, manager, clock):
        super().__init__(manager)
        self.clock = clock

    def on_enter(self, **kwargs):
        self.background = Background(config_data=configmap["background"])
        self.sun = ImageSprite(
            128, 200, DISPLAY_HEIGHT // 2, get_assets("images/sun.webp"), True
        )
        self.earth = ImageSprite(
            72,
            self.sun.rect.centerx + 1000,
            DISPLAY_HEIGHT // 2,
            get_assets("images/earth.webp"),
            True,
        )

        self.planets = pygame.sprite.Group(
            self.earth,
            self.sun,
        )

        self.all_bodies = pygame.sprite.Group(self.background)
        for _ in range(20):
            self.all_bodies.add(Star())
            
        self.probe_bodies = pygame.sprite.Group()
            
        self.probe = None

        self.play_bgm()

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.manager.switch_scene("SolarSystemScene")
                    return
                if event.key == pygame.K_3:
                    self.manager.switch_scene("EarthMoveScene")
                    return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_7:
                    self.probe = SuperProbe(self.earth.rect.centerx, self.earth.rect.centery, 1, self.sun)
                    self.probe_bodies.add(self.probe)
                    

    def update(self):
        self.all_bodies.update()
        self.planets.update()
        self.probe_bodies.update()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.all_bodies.draw(screen)
        self.planets.draw(screen)
        for p in self.probe_bodies:
            p.trail_group.draw(screen)
        self.probe_bodies.draw(screen)
        if self.probe:
            self.probe.draw_text(screen)

    def on_exit(self, **kwargs):
        pass

    def play_bgm(self):
        """播放背景音乐""" ""
        pygame.mixer.music.load(get_assets(configmap["bgm"]["sound"]))
        pygame.mixer.music.set_volume(configmap["bgm"]["sound_volume"])
        # pygame.mixer.music.play(-1)
