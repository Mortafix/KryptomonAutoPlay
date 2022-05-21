from datetime import datetime, timedelta
from os.path import join
from time import sleep

from static.items import Box, Extra, Item, Kryptomon, Menu

# ---- Utils


def od(n):
    return f"{n}{'tsnrhtdd'[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10 :: 4]}"


class Instructions:
    def __init__(self, screen, folder):
        self.screen = screen
        self.folder = folder
        self.current_screen = 1
        self.gameplay_actions = {
            "food": Menu.food,
            "heal": Menu.health,
            "play": Menu.toys,
            "train": Menu.train,
        }
        self.other_action = {"screen": self.change_screen, "box": self.open_box}
        self.items = {1: Item.first, 2: Item.second, 3: Item.third, 4: Item.fourth}
        self.boxes = {1: Box.free, 2: Box.bronze, 3: Box.silver, 4: Box.gold}
        self.free_boxes = {1: 3, 2: 6, 3: 9, 4: 11, 5: 12}

    def load_instructions(self):
        instructions_file = join(self.folder, "static/instructions.txt")
        actions = [
            row.split(" ")
            for row in open(instructions_file).read().split("\n")
            if row and row[0] != "#"
        ]
        if actions[0][0] != "timeframe":
            raise self.MissingSetting("Timeframe missing on the 1st line")
        if not actions[0][1].isdigit():
            raise self.WrongParameter("Timeframe param must be an integer")
        if actions[1][0] != "kryptomons":
            raise self.MissingSetting("Kryptomons missing on the 2nd line")
        actions[1] = ["kryptomons", "".join(actions[1][1:]).split(",")]
        if not all(n.isdigit() for n in actions[1][1]):
            raise self.WrongParameter(
                "Kryptomons param must be integers separated by commas"
            )
        actions[1][1] = list(map(int, actions[1][1]))
        for action, *params in actions[2:]:
            if action in ("food", "heal", "play", "train"):
                if len(params) != 3:
                    raise self.WrongParameter(f"'{action}' parameters must be 3")
                for param in params:
                    if not param[1:].isdigit() or param[0] not in ("e", "k", "t"):
                        raise self.WrongParameter(
                            f"'{action}' param '{param}' not exists"
                        )
            elif action in ("screen", "box"):
                if len(params) != 2:
                    raise self.WrongParameter(f"'{action}' parameters must be 2")
                for param in params:
                    if not param[1:].isdigit() or param[0] not in ("p", "t"):
                        raise self.WrongParameter(
                            f"'{action}' param '{param}' not exists"
                        )
            else:
                raise self.WrongAction(f"Action '{action}' not exists")
        print("> Actions loaded correctly")
        self.timeframe = int(actions[0][1])
        self.kryptomons = actions[1][1]
        self.actions = [
            (action, {p[0]: int(p[1:]) for p in params})
            for action, *params in actions[2:]
        ]
        print(f"> Timeframe: {self.timeframe}m")
        kryptomons_str = " | ".join(f"⌜ {k} ⌟" for k in self.kryptomons)
        print(f"> Kryptomons: {kryptomons_str}")

    def run_actions(self, iteration):
        start_iteration = datetime.now()
        print(f"\n> Iteration #{iteration + 1} [{start_iteration:%d.%m.%Y %H:%M}]")
        # actions
        for action, params in self.actions:
            if iteration % params.get("t"):
                continue
            if category := self.gameplay_actions.get(action):
                kmon_idx, item_idx = params.get("k"), params.get("e")
                kryptomon = self.select_kryptomon(kmon_idx)
                item = self.items.get(item_idx)
                print(f"Give {od(item_idx)} {action} item to {od(kmon_idx)} kryptomon")
                self.give_item(kryptomon, category, item)
            if func := self.other_action.get(action):
                func(params.get("p"))
        # time remaining
        elapsed_time = datetime.now() - start_iteration
        eta_time = timedelta(seconds=self.timeframe * 60 - elapsed_time.seconds)
        next_iteration = datetime.now() + eta_time
        print(f"# Next iteration > {next_iteration:%d.%m.%Y %H:%M}")
        return eta_time

    # ---- Actions

    def select_kryptomon(self, index):
        kryptomons = {1: Kryptomon.solo, 2: Kryptomon.duo, 3: Kryptomon.trio}
        kryptomons_on_screen = self.kryptomons[self.current_screen - 1]
        return kryptomons.get(kryptomons_on_screen)[index - 1]

    def give_item(self, kryptomon, item_category, item):
        # be sure the items bar is open
        self.screen.click_on(*Extra.empty, amount=2)
        self.screen.click_on(*item_category)
        # try give item in multiple positions
        for x in range(*kryptomon, 10):
            for y in range(*Extra.rows, 10):
                self.screen.move_to(item, (x, y), drag="left")

    def change_screen(self, index):
        print(f"Change screen to #{index}")
        moves = index - self.current_screen
        for _ in range(abs(moves)):
            direction = Extra.screen_right if moves > 0 else Extra.screen_left
            self.screen.click_on(*direction)
            sleep(2)
        self.current_screen = index

    def open_box(self, index):
        names = {1: "free", 2: "bronze", 3: "silver", 4: "gold"}
        print(f"Open a {names.get(index)} box")
        self.screen.click_on(*Extra.empty, amount=2)
        self.screen.click_on(*Box.icon)
        self.screen.click_on(*self.boxes.get(index))
        amount = self.free_boxes.get(sum(self.kryptomons), 0) if index == 1 else 1
        for _ in range(amount):
            sleep(10)
            self.screen.click_on(*Box.cont)
        self.screen.click_on(*Box.close)

    # ---- Exception

    class MissingSetting(Exception):
        pass

    class WrongParameter(Exception):
        pass

    class WrongAction(Exception):
        pass
