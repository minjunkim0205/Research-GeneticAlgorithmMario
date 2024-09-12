import retro
import numpy

env = retro.make(game="SuperMarioBros-Nes", state="Level1-1")
env.reset()

# Key input
env.step(numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))# B,NULL,SELECT,START,U,D,L,R,A

# Get ram info
ram = env.get_ram()
enemy_drawn = ram[0x000F:0x0013+1] # 0x000F-0x0013	Enemy drawn? Max 5 enemies at once. => 0:No,1:Yes (not so much drawn as "active" or something)
print(enemy_drawn, end="\n")

enemy_horizon = ram[0x006E:0x0072+1] # 0x006E-0x0072	Enemy horizontal position in level
enemy_screen_x = ram[0x0087:0x008B+1] # 0x0087-0x008B	Enemy x position on screen
enemy_y = ram[0x00CF:0x00D3+1] # 0x00CF-0x00D3	Enemy y pos on screen
enemy_x = (enemy_screen_x + (enemy_horizon * 256)) % 512
print(enemy_x, enemy_y, end="\n")

enemy_tile_x = (enemy_x + 8) // 16
enemy_tile_y = (enemy_y - 8) // 16 - 1
print(enemy_tile_x, enemy_tile_y, end="\n")
