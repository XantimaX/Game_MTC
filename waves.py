from entities import NormalEnemy, BruteEnemy, BossEnemy

waves = [
    [  # Wave 1
        {"type": "NormalEnemy", "pos": (1000, 200)},
        {"type": "NormalEnemy", "pos": (1000, 300)},
        {"type": "NormalEnemy", "pos": (1000, 500)}
    ],
    [  # Wave 2
        {"type": "NormalEnemy", "pos": (1400, 200)},
        {"type": "BruteEnemy", "pos": (1800, 400)},
        {"type": "BruteEnemy", "pos": (1800, 200)},
        {"type": "NormalEnemy", "pos": (1600, 500)},
        {"type": "NormalEnemy", "pos": (1400, 500)},
    ],
    [  # Wave 3
        {"type": "BruteEnemy", "pos": (400, 800)},
        {"type": "BruteEnemy", "pos": (700, 1000)},
        {"type": "BruteEnemy", "pos": (700, 1500)},
        {"type": "NormalEnemy", "pos": (500, 900)},
        {"type": "NormalEnemy", "pos": (500, 1200)},
        {"type": "NormalEnemy", "pos": (300, 900)},
        {"type": "NormalEnemy", "pos": (300, 1500)},
        {"type": "NormalEnemy", "pos": (1800, 900)},
    ],
    
    [  # Wave 4
        {"type": "BossEnemy", "pos": (400, 800)},
        {"type": "BruteEnemy", "pos": (700, 1000)},
        {"type": "BruteEnemy", "pos": (700, 1500)},
        {"type": "NormalEnemy", "pos": (500, 900)},
        {"type": "NormalEnemy", "pos": (500, 1200)},
    ]
]

def spawn_wave(wave_idx, enemy_group, camera_group):
    enemy_group.empty()  # Remove any existing enemies
    for enemy_info in waves[wave_idx]:
        enemy = None
        if enemy_info["type"] == "NormalEnemy":
            enemy = NormalEnemy(pos=enemy_info["pos"])
        elif enemy_info["type"] == "BruteEnemy":
            enemy = BruteEnemy(pos=enemy_info["pos"])
        elif enemy_info["type"] == "BossEnemy":
            enemy = BossEnemy(pos=enemy_info["pos"])
        enemy_group.add(enemy)
        camera_group.add(enemy)