import math
import random
import pygame
from pygame.locals import *
from .common import (
    get_assets,
    res_manager,
    DISPLAY_WIDTH,
    DISPLAY_HEIGHT,
    Colors,
    days_to_dhms,
)
from .config import configmap

_sun_pos = (DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2.5)


class Background(pygame.sprite.Sprite):
    def __init__(self, config_data=None):
        pygame.sprite.Sprite.__init__(self)
        self.config = config_data
        original_image = res_manager.load_image(random.choice(self.config["images"]))
        original_width, original_height = original_image.get_size()
        scale_factor = DISPLAY_WIDTH / original_width
        new_height = int(original_height * scale_factor)

        self.image = pygame.transform.scale(original_image, (DISPLAY_WIDTH, new_height))
        self.rect = self.image.get_rect()


class HMoveBackground(pygame.sprite.Sprite):
    def __init__(self, config_data=None):
        pygame.sprite.Sprite.__init__(self)
        self.config = config_data
        original_image = res_manager.load_image(random.choice(self.config["images"]))
        original_width, original_height = original_image.get_size()
        original_width, original_height = original_image.get_size()
        scale_factor = DISPLAY_HEIGHT / original_height
        new_width = int(original_width * scale_factor)

        self.image = pygame.transform.scale(original_image, (new_width, DISPLAY_HEIGHT))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += 2  # Move the background down
        if self.rect.x >= 0:
            self.rect.x = - (self.rect.width- DISPLAY_WIDTH)


class ImageSprite(pygame.sprite.Sprite):
    def __init__(self, width, x, y, image_path, is_rotate=False):
        pygame.sprite.Sprite.__init__(self)
        # 加载并存储原始图片
        self.original_image = pygame.image.load(image_path)
        original_width, original_height = self.original_image.get_size()

        # 计算缩放比例并应用
        scale_factor = width / original_width
        new_height = int(original_height * scale_factor)
        self.scaled_image = pygame.transform.scale(
            self.original_image, (width, new_height)
        )

        # 初始化图像和位置
        self.image = self.scaled_image  # 初始化图像
        self.rect = self.image.get_rect(center=(x, y))
        self.is_rotate = is_rotate

        # 初始化旋转角度
        self.rotation_angle = 0

    def update(self):
        if self.is_rotate:
            # 旋转当前角度
            self.image = pygame.transform.rotate(self.scaled_image, self.rotation_angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.rotation_angle += 0.5  # 更新角度
            if self.rotation_angle >= 360:
                self.rotation_angle = 0  # 重置角度为0，避免无限增长
                
    
    def move_y(self, dx, speed):
        new_y = self.rect.y + dx * speed
        if 0 <= new_y or new_y >= DISPLAY_HEIGHT - 200:
            self.rect.y = new_y


class Star(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = res_manager.load_image(
            "images/star.webp"
        )  # 假设已经有了res_manager来处理资源加载
        self.image = self.image.convert_alpha()  # 确保图像有 alpha 通道

        # 随机缩放比例
        scale = random.uniform(0.6, 1)
        self.original_image = pygame.transform.scale(
            self.image,
            (int(self.image.get_width() * scale), int(self.image.get_height() * scale)),
        )

        # 随机透明度
        self.alpha = random.randint(100, 255)
        self.image = self.original_image.copy()
        self.image.set_alpha(self.alpha)

        # 随机位置
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, DISPLAY_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, DISPLAY_HEIGHT - self.rect.height)

        # 闪烁控制
        self.flicker_delay = random.randint(20, 60)  # 每隔10到30帧闪烁一次
        self.flicker_count = 0

    def update(self):
        self.flicker_count += 1
        if self.flicker_count >= self.flicker_delay:
            self.flicker()
            self.flicker_count = 0

    def flicker(self):
        # 动态调整星星的大小和透明度以实现闪烁效果
        self.scale_change = random.uniform(0.6, 1)
        self.alpha_change = random.randint(-10, 10)

        new_width = int(self.original_image.get_width() * self.scale_change)
        new_height = int(self.original_image.get_height() * self.scale_change)
        self.image = pygame.transform.scale(
            self.original_image, (new_width, new_height)
        )

        self.alpha = min(255, max(50, self.alpha + self.alpha_change))
        self.image.set_alpha(self.alpha)

        self.rect = self.image.get_rect(center=self.rect.center)


class TrailSprite(pygame.sprite.Sprite):
    def __init__(self, pos, color=(200, 200, 200), size=10, lifespan=7200):
        super().__init__()
        self.lifespan = lifespan
        size = size  # 增加轨迹点的尺寸以制作更大的光晕
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Fill with transparent color

        # 创建光晕效果，中心亮边缘暗
        for i in range(size // 2, 0, -1):  # 从中心到边缘
            alpha = int(128 * (i / (size / 2)))  # 中心更亮，边缘更暗
            pygame.draw.circle(self.image, color + (alpha,), (size // 2, size // 2), i)

        self.rect = self.image.get_rect(center=(pos[0], pos[1] + 2))

    def update(self):
        # 减少生命周期
        self.lifespan -= 1
        if self.lifespan <= 0:
            self.kill()  # 当生命结束时移除精灵
        else:
            # 通过减少 alpha 来淡出精灵
            alpha = max(
                0, min(255, int(255 * (self.lifespan / 120)))
            )  # 确保 alpha 在 0 到 255 范围内
            alpha_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            alpha_surface.fill((255, 255, 255, alpha))
            self.image.blit(alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


class CelestialBody(pygame.sprite.Sprite):
    def __init__(
        self,
        name,
        image,
        orbit_size,
        orbit_speed,
        distance_from_sun,
        subobj,
    ):
        super().__init__()
        self.name = name
        self.original_image = image
        self.image = image
        self.show_orbit = True  # 新增属性，用于控制轨道的显示
        if self.name == "sun":
            self.sun = self
            self.rect = self.image.get_rect(
                center=(_sun_pos[0] + distance_from_sun, _sun_pos[1])
            )
        else:
            self.sun = subobj
            self.rect = self.image.get_rect(
                center=(
                    self.sun.rect.centerx + distance_from_sun,
                    self.sun.rect.centery,
                )
            )

        self.orbit_size = orbit_size
        self.orbit_speed = orbit_speed * 2
        self.distance_from_sun = distance_from_sun
        self.angle = 0
        self.trail_group = pygame.sprite.Group()

        self.rotation_speed = 0.15  # 存储自转速度
        self.rotation_angle = 0  # 初始化旋转角度

    def update(self):
        if self.name == "sun":
            self.rotation_angle = (self.rotation_angle + self.rotation_speed) % 360
            self.image = pygame.transform.rotate(
                self.original_image, self.rotation_angle
            )
            self.rect = self.image.get_rect(center=self.rect.center)

        if self.distance_from_sun > 0:
            self.angle = (self.angle + self.orbit_speed) % 360
            radian_angle = math.radians(self.angle)

            # Calculate the base position without the perspective for orbit
            base_pos_x = (
                self.sun.rect.centerx + math.cos(radian_angle) * self.distance_from_sun
            )
            base_pos_y = (
                self.sun.rect.centery + math.sin(radian_angle) * self.orbit_size
            )

            # Apply perspective scaling to y position
            perspective_scale_y = 1.2 + 0.2 * math.sin(radian_angle)
            perspective_scale_x = 1.5 + 0.0001 * math.cos(radian_angle)

            # Adjust the position to simulate perspective
            pos_x = (
                self.sun.rect.centerx
                + (base_pos_x - self.sun.rect.centerx) * perspective_scale_x
            )
            pos_y = (
                self.sun.rect.centery
                + (base_pos_y - self.sun.rect.centery) * perspective_scale_y
            )

            self.rect.centerx, self.rect.centery = pos_x, pos_y

            # Adjust the size of the planet for perspective
            distance_to_camera = (pos_y - self.sun.rect.centery) * perspective_scale_y
            size_scale = max(0.2, 1 - abs(distance_to_camera) / (DISPLAY_HEIGHT // 2))
            new_width = int(self.original_image.get_width() * size_scale)
            new_height = int(self.original_image.get_height() * size_scale)
            self.image = pygame.transform.scale(
                self.original_image, (new_width, new_height)
            )

            # Add a trail sprite at the current position
            trail = TrailSprite(
                self.rect.center,
                Colors.white,
                size=self.rect.width // 3 * 2,
                lifespan=100,
            )
            trail2 = TrailSprite(
                self.rect.center, Colors.orange, size=2, lifespan=self.orbit_size * 21
            )
            self.trail_group.add(trail)
            self.trail_group.add(trail2)
            self.trail_group.update()

            # Update the scale and position of the planet image
            # The scale should be larger when the planet is closer to the bottom of the screen (closer to the viewer)
            if self.name != "sun":
                # Perspective depth adjustment
                depth_scale = 1 + (self.rect.centery - _sun_pos[1]) / (
                    DISPLAY_HEIGHT / 2
                )
                self.image = pygame.transform.scale(
                    self.original_image,
                    (
                        int(self.original_image.get_width() * depth_scale),
                        int(self.original_image.get_height() * depth_scale),
                    ),
                )
                self.rect = self.image.get_rect(center=(pos_x, pos_y))

    @classmethod
    def create_sun(cls):
        return CelestialBody(
            "sun", res_manager.load_image("images/sun.webp"), 0, 0, 0, None
        )

    @classmethod
    def create_planet(cls, name, sun):
        data = configmap["planets"][name]
        return CelestialBody(
            name,
            res_manager.load_image(data["image"]),
            data["orbit_size"],
            data["orbit_speed"],
            data["distance_from_sun"],
            sun,
        )


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color, speed_range=(0.1, 2), size_range=(1, 3, 5)):
        super().__init__()
        self.color = color
        self.size = random.choice(size_range)  # 粒子的初始直径
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=(x, y))

        # 随机分配速度和方向
        speed = random.uniform(*speed_range)
        angle = random.uniform(0, 2 * math.pi)
        self.vel_x = speed * math.cos(angle)
        self.vel_y = speed * math.sin(angle)

        self.lifetime = random.randint(20, 100)  # 随机生命周期

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.lifetime -= 1  # 递减生命周期
        self.size -= 0.05  # 逐渐减小粒子的大小，减小速度更慢一些以延长显示时间
        if self.size <= 0 or self.lifetime <= 0:
            self.kill()  # 当粒子消失或生命周期结束时，从精灵组中移除
        else:
            # 每次更新时重新创建圆形图像
            self.image = pygame.Surface(
                (int(self.size) * 2, int(self.size) * 2), pygame.SRCALPHA
            )
            self.image = self.image.convert_alpha()  # 确保支持透明度
            pygame.draw.circle(
                self.image, self.color, (int(self.size), int(self.size)), int(self.size)
            )
            self.rect = self.image.get_rect(
                center=(self.rect.centerx, self.rect.centery)
            )


class SuperProbe(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, target: pygame.sprite.Sprite):
        super().__init__()
        self.trail_group = pygame.sprite.Group()
        self.x = x
        self.y = y
        self.target = target  # 目标对象是另一个Sprite
        self.speed = speed
        self.speed_km = round(speed * 430 * 1000)
        # 加载图像时保留原始图像用于旋转
        self.original_image = res_manager.load_image("images/probe.webp")
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(self.x, self.y))

        distance_km = 149.6e6  # 地球到太阳的距离，单位公里
        self.total_days = distance_km / (self.speed_km * 24)  # 转换成天
        self.remaining_days = self.total_days
        self.initial_dist = math.hypot(
            self.target.rect.centerx - self.x, self.target.rect.centery - self.y
        )
        self.font = pygame.font.Font(get_assets("Imprint-MT-Shadow-2.ttf"), 64)

    def attack(self):
        # 计算到目标的距离和角度
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        angle = math.atan2(dy, dx)
        current_dist = math.hypot(dx, dy)

        if current_dist < 10:
            self.speed = 0  # 停止移动
            return  # 停止其他处理，防止超调

        # 更新剩余天数
        remaining_ratio = current_dist / self.initial_dist
        self.remaining_days = remaining_ratio * self.total_days

        # 调整位置
        self.rect.x += self.speed * math.cos(angle)
        self.rect.y += self.speed * math.sin(angle)

        # 旋转图像。注意Pygame中的角度是逆时针方向，需要转换为角度，并调整以使0度向上
        angle_degrees = math.degrees(angle) + 90
        self.image = pygame.transform.rotate(
            self.original_image, -angle_degrees
        )  # 注意这里的角度需要是负的，因为Pygame旋转方向与数学方向相反
        self.rect = self.image.get_rect(
            center=(self.rect.center)
        )  # 更新rect以保持中心位置不变

        # 边界检测
        if (
            self.rect.top < 0
            or self.rect.bottom > DISPLAY_HEIGHT
            or self.rect.left < 0
            or self.rect.right > DISPLAY_WIDTH
        ):
            self.kill()

    def update(self):
        self.attack()
        trail = TrailSprite(
            self.rect.center,
            Colors.white,
            size=self.rect.width // 2,
            lifespan=130,
        )
        self.trail_group.add(trail)
        self.trail_group.update()

    def draw_text(self, screen):
        # if self.speed > 0:
        text = days_to_dhms(self.total_days - self.remaining_days)
        text_surface = self.font.render(text, True, Colors.yellow)
        screen.blit(text_surface, (self.rect.x, self.rect.y + 100))


class EarthTrailSprite(pygame.sprite.Sprite):
    def __init__(
        self, position, wave_amplitude=45, wave_length=200, size=(6, 9), delay=0
    ):
        super().__init__()
        self.image = pygame.Surface(size, pygame.SRCALPHA)  # 使用带透明度的表面
        self.image.fill((0, 0, 0, 0))  # 填充透明
        pygame.draw.ellipse(
            self.image,
            random.choice([Colors.white, Colors.light_yellow, Colors.cyan]),
            [0, 0, size[0], size[1]],
        )  # 画一个白色椭圆形
        self.rect = self.image.get_rect(center=position)
        self.alpha = 255
        self.original_y = position[1] + random.choice(
            [-5, 5, -10, 10, -15, 15, -20, 20, -25, 25]
        )  # 随机位置
        self.wave_amplitude = wave_amplitude
        self.wave_length = wave_length
        self.frame_count = delay  # 初始延迟为周期的偏移

    def update(self):
        self.frame_count += 1
        wave_offset = self.wave_amplitude * math.sin(
            math.pi * self.frame_count * 2 / self.wave_length
        )
        self.rect.y = self.original_y + wave_offset
        self.rect.x += 1 # 每帧向右移动1像素

        # 透明度随时间减少
        self.alpha = max(0, 255 - (self.frame_count * 0.5))  # 减慢透明度变化速度
        self.image.set_alpha(self.alpha)
        if self.alpha <= 0:
            self.kill()



class Meteor(pygame.sprite.Sprite):
    
    def __init__(self, mtype, config_data):
        super().__init__()
        self.config = config_data
        self.x = -100
        self.y = random.choice([random.randint(100, DISPLAY_HEIGHT-100), random.randint(100, DISPLAY_HEIGHT-200)])
        self.speed = random.choice(self.config[mtype]["speed"])
        self.type = mtype
        self.image = res_manager.load_image(random.choice(self.config[self.type]["images"]))
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def update(self):
        self.x += self.speed
        self.rect.x = self.x
        if self.x > DISPLAY_WIDTH:
            self.kill()



class ShockParticle(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, color, speed=0.5):
        super().__init__()
        self.color = color
        self.speed = speed
        self.size = random.randint(9, b=15)  # 粒子的初始直径
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        self.image = self.image.convert_alpha()
        pygame.draw.circle(self.image, self.color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect(center=(center_x, center_y))

        # 随机生成一个角度
        angle = random.uniform(0, 2 * math.pi)
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed
        self.float_x = float(center_x)  # 添加这行
        self.float_y = float(center_y)  # 添加这行

        self.lifetime = random.randint(50, 100)  # 给粒子更长的生命周期

    def update(self):
        # 更新浮点数位置
        self.float_x += self.vel_x
        self.float_y += self.vel_y

        # 更新速度，使粒子加速
        self.vel_x *= 1.02
        self.vel_y *= 1.01

        # 减少生命周期，逐渐减小粒子的大小
        self.lifetime -= 0.3
        self.size -= 0.3

        if self.lifetime <= 0 or self.size <= 0:
            self.kill()  # 当生命周期结束或大小减小到0时，移除粒子
        else:
            # 重新创建图像以匹配新的大小，并保持中心位置不变
            self.image = pygame.Surface(
                (max(int(self.size * 2), 1), max(int(self.size * 2), 1)),
                pygame.SRCALPHA,
            )
            self.image = self.image.convert_alpha()
            pygame.draw.circle(
                self.image,
                self.color,
                (int(self.size), int(self.size)),
                max(int(self.size), 1),
            )

            # 更新rect对象，以便在绘制时使用正确的位置
            # 这里使用浮点数位置并转换为整数，保证粒子的中心位置绘制时不会因为尺寸变化而移动
            self.rect = self.image.get_rect(
                center=(int(self.float_x), int(self.float_y))
            )

