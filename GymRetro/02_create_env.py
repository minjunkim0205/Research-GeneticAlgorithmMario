import retro

env = retro.make(game='SuperMarioBros-Nes', state='Level1-1')
env.reset()

screen = env.get_screen()

print(screen.shape, end="\n\n")
print(screen, end="\n")