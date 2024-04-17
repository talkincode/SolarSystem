configmap = {
    "display_width": 1440,
    "display_height": 900,
    "fullscreen": False,
    "bgm": {
        "sound": "sounds/bgm.ogg",
        "sound_volume": 0.5,
    },
    "background": {
        "images": ["images/background.webp"],
    },
    "hbackground": {
        "images": ["images/hbackground.webp"],
    },
    "planets": {
        "sun": {
            "image": "images/sun.webp",
            "orbit_size": 0,
            "orbit_speed": 0,
            "distance_from_sun": 0,
            "rotation_speed": 0.1,
        },
        "mercury": {
            "image": "images/mercury.webp",
            "orbit_size": 50,
            "orbit_speed": 0.5,
            "distance_from_sun": 80,
            "rotation_speed": 0.5,
        },
        "venus": {
            "image": "images/venus.webp",
            "orbit_size": 70,
            "orbit_speed": 0.35,
            "distance_from_sun": 110,
            "rotation_speed": 0.5,
        },
        "earth": {
            "image": "images/earth.webp",
            "orbit_size": 90,
            "orbit_speed": 0.3,
            "distance_from_sun": 150,
            "rotation_speed": 4,
        },
        "mars": {
            "image": "images/mars.webp",
            "orbit_size": 110,
            "orbit_speed": 0.24,
            "distance_from_sun": 190,
            "rotation_speed": 0.5,
        },
        "jupiter": {
            "image": "images/jupiter.webp",
            "orbit_size": 140,
            "orbit_speed": 0.13,
            "distance_from_sun": 240,
            "rotation_speed": 0.5,
        },
        "saturn": {
            "image": "images/saturn.webp",
            "orbit_size": 180,
            "orbit_speed": 0.09,
            "distance_from_sun": 290,
            "rotation_speed": 0.5,
        },
        "uranus": {
            "image": "images/uranus.webp",
            "orbit_size": 220,
            "orbit_speed": 0.06,
            "distance_from_sun": 340,
            "rotation_speed": 0.5,
        },
        "neptune": {
            "image": "images/neptune.webp",
            "orbit_size": 250,
            "orbit_speed": 0.05,
            "distance_from_sun": 380,
            "rotation_speed": 0.5,
        }
    },
    "meteor":{
        "meteor_shard": {
            "images": ["images/meteor_shard.webp","images/meteor_shard2.webp","images/meteor_shard3.webp"],
            "damage": 100,
            "life_value": 300,
            "score_value": 50,
            "speed": [4,5,6,7,8,9],
        },
        "meteor_core": {
            "images": ["images/meteor_core.webp", "images/meteor_core2.webp"],
            "damage": 0,
            "life_value": 500,
            "score_value": 300,
            "speed": [4,5,6,7,8,9],
        }
    },
}
