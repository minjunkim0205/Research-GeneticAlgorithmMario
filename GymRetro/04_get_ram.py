import retro
import numpy

env = retro.make(game="SuperMarioBros-Nes", state="Level1-1")
env.reset()

# Key input
env.step(numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))# B,NULL,SELECT,START,U,D,L,R,A

# Get ram info
ram = env.get_ram()
print(ram.shape, end="\n")
print(ram, end="\n")
print(ram[0x0003], end="\n")# 0x0003	Player's direction (and others) => 1:Right,2:Left