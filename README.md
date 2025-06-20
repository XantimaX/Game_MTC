# How to run the game ?
1) Clone this repo.
2) Download Python 3.6 or above
3) Open the Command Line Prompt
4) Make sure your current directory is in the Game_MTC folder.
5) then pip install the following libraries :
   `pip install pygame pytmx numpy`
6) Finally run this command
   `python main.py` or `python3 main.py`

# What is the game about ?
This is a top down shooter. Your goal is to kill all the enemies per wave. There are total of 4 waves, with wave 4 having a boss fight.

## Enemy Types
Normal Enemies (Blue) : Health : 5HP, Damage : 1 
Brute Enemies (Red) : Health : 10HP, Damage : 2, throws grenade every 3 seconds. Grenade Damage : 3
Boss (Surprise) : Health : 20HP, Damage: 3, throws grenade every second. Grenade Damage : 3

## Score 
You have 3 lives. Each life has 1000 points.
What time you finish determines score.
< 4:00 -> 3000 points
< 5:00 -> 2000 points
< 6:00 -> 1000 points

So the highest score you can get is 6000.


