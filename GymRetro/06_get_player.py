import retro
import numpy

env = retro.make(game="SuperMarioBros-Nes", state="Level1-1")
env.reset()

# Key input
env.step(numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))# B,NULL,SELECT,START,U,D,L,R,A

# Get ram info
ram = env.get_ram()
player_x = ram[0x03AD] # 0x03AD	Player x pos within current screen offset
player_y = ram[0x03B8] # 0x03B8	Player y pos within current screen
print(player_x, player_y, end="\n")

# Convert screen coordinates to tile coordinates
player_tile_x = (player_x + 8) // 16
player_tile_y = (player_y + 8) // 16 - 1
print(player_tile_x, player_tile_y, end="\n")