from time import sleep

from utils.actions import Instructions
from utils.screen import GameScreen

screen = GameScreen()
screen.register_screen()
screen.starting_timer()

instructions = Instructions(screen)
instructions.load_instructions()

iteration = 0
while True:
    wait = instructions.run_actions(iteration)
    iteration += 1
    sleep(wait.seconds)
