import retro
import numpy

env = retro.make(game="SuperMarioBros-Nes", state="Level1-1")
env.reset()

# Key input
env.step(numpy.array([0, 0, 0, 0, 0, 0, 0, 0, 0]))# B,NULL,SELECT,START,U,D,L,R,A

# Get screen bitmap
screen = env.get_screen()
print(screen.shape, end="\n")
print(screen, end="\n")