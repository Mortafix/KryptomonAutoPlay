from time import sleep

from pyautogui import click, mouseDown, mouseUp, moveTo, position
from pynput.mouse import Listener


class GameScreen:
    top_left_corner = None, None
    bottom_right_corner = None, None

    def __str__(self):
        tlx, tly = self.top_left_corner
        brx, bry = self.bottom_right_corner
        screen_size = f"{self.width:.0f}x{self.heigth:.0f}"
        return f"[screen {screen_size}] ⌜ {tlx:.0f}:{tly:.0f} | {brx:.0f}:{bry:.0f} ⌟"

    def _on_click(self, x, y, button, pressed):
        if pressed:
            self.top_left_corner = x, y
        if not pressed:
            self.bottom_right_corner = x, y
            return False

    def _calculate_position(self, relativeX, relativeY):
        originX, originY = self.top_left_corner
        x = originX + self.width * (relativeX / 100)
        y = originY + self.heigth * (relativeY / 100)
        return x, y

    def register_screen(self):
        print("> Highlight the play screen with the mouse")
        print("  Click on the top left corner and release on the bottom right one")
        with Listener(on_click=self._on_click) as listener:
            listener.join()
        tlx, tly = self.top_left_corner
        brx, bry = self.bottom_right_corner
        self.width = brx - tlx
        self.heigth = bry - tly
        print(f"> Registered {self}")

    def register_mouse_position(self):
        def report_position(x, y, button, pressed):
            if pressed:
                x, y = self.percentage_position(x, y)
                print(f"{x:.1f}, {y:.1f}")

        with Listener(on_click=report_position) as listener:
            listener.join()

    def starting_timer(self, seconds=5):
        print(f"> Starting in {seconds} seconds.. (focus the game window!)")
        sleep(seconds - 3)
        for i in range(3, 0, -1):
            print(i)
            sleep(1)

    def click_on(self, relX, relY, amount=1, only_move=False, wait_after=0.5):
        x, y = self._calculate_position(relX, relY)
        click(x, y, clicks=amount) if not only_move else moveTo(x, y)
        sleep(wait_after)

    def move_to(self, *positions, exit_condition=None, duration=0, drag=False):
        if drag:
            x, y = self._calculate_position(*positions[0])
            moveTo(x, y)
            mouseDown()
        for relX, relY in positions:
            x, y = self._calculate_position(relX, relY)
            moveTo(x, y, duration)
            if exit_condition and exit_condition(x, y):
                break
        mouseUp()

    def mouse_position(self):
        return position()

    def percentage_position(self, posX, posY):
        originX, originY = self.top_left_corner
        relX = (posX - originX) / self.width * 100
        relY = (posY - originY) / self.heigth * 100
        return relX, relY
