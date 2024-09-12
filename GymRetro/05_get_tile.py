import retro
import numpy

env = retro.make(game="SuperMarioBros-Nes", state="Level1-1")
env.reset()

# Key input
env.step(numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))# B,NULL,SELECT,START,U,D,L,R,A

# Get ram info
ram = env.get_ram()

# Get 1-dimensional tile map(Current page and next page tiles)
tiles = ram[0x0500:0x069F+1] # 0x0500-0x069F	Current tile (Does not effect graphics)
tile_count = tiles.shape[0]
print(tiles, end="\n")
print("\n", end="")

# Convert a 1-dimensional tile map to a 2-dimensional tile map
tiles_current = tiles[:tile_count//2].reshape((13, 16))
tiles_next = tiles[tile_count//2:].reshape((13, 16))
tiles = numpy.concatenate((tiles_current, tiles_next), axis=1).astype(numpy.int32)
print(tiles, end="\n")
print("\n", end="")

# Implementation of screen side scrolling
current_screen_page = ram[0x071A] # 0x071A	Current screen (in level)
screen_position = ram[0x071C] # 0x071C	ScreenEdge X-Position, loads next screen when player past it?
screen_offset = (256 * current_screen_page + screen_position) % 512
screen_tile_offset = screen_offset // 16
tiles = numpy.concatenate((tiles, tiles), axis=1)[:, screen_tile_offset:screen_tile_offset+16]
print(tiles, end="\n")
print("\n", end="")