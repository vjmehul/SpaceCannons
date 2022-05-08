##Version control
V2=True



DISPLAY_SIZE = (950,700)
P1_pos_x = 630
P1_pos_y = -10

P2_pos_x = 250
P2_pos_y = -10

PLAYER_HEALTH=30
coop_factor=0.5

game_difficulty_metric = 1
bullet_penalty = 0.5


miniboss_evade_penalty = -1
mini_evade_penalty = -1

if V2:
    bullet_speed = -25
    miniboss_health=160
    mini_health=6
    num_actions=3
else:
    bullet_speed = -45
    miniboss_health=40
    mini_health=4
    num_actions=4


#difficulty design

if game_difficulty_metric ==1:
    spawn_timer=120
    enemyspeed = 2.5
elif game_difficulty_metric ==2:
    spawn_timer=150
    enemyspeed = 3.5

