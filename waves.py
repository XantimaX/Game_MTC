from entities import NormalEnemy, BruteEnemy

waves = [
    [  # Wave 1
        {"type": "NormalEnemy", "pos": (400, 200)},
        {"type": "NormalEnemy", "pos": (600, 300)},
    ],
    [  # Wave 2
        {"type": "NormalEnemy", "pos": (400, 200)},
        {"type": "BruteEnemy", "pos": (800, 400)},
        {"type": "NormalEnemy", "pos": (600, 500)},
    ],
    [  # Wave 3
        {"type": "BruteEnemy", "pos": (400, 800)},
        {"type": "BruteEnemy", "pos": (700, 1000)},
        {"type": "NormalEnemy", "pos": (500, 900)},
    ]
]

def spawn_wave(wave_idx, enemy_group, camera_group):
    enemy_group.empty()  # Remove any existing enemies
    for enemy_info in waves[wave_idx]:
        if enemy_info["type"] == "NormalEnemy":
            enemy = NormalEnemy(pos=enemy_info["pos"])
        elif enemy_info["type"] == "BruteEnemy":
            enemy = BruteEnemy(pos=enemy_info["pos"])
        enemy_group.add(enemy)
        camera_group.add(enemy)