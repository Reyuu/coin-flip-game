import random
import pygame
import ezpygame
import math

class Coin:
    def __init__(self, name="Coin"):
        self.name = name
        self.side = None
        self.sides = {0: "heads", 1: "tails"}
        self.rsides = {"heads": 0, "tails": 1, "t": 1, "h": 0}
        self.flip()
        # 0 - head
        # 1 - tails

    def flip(self):
        self.side = random.randint(0, 1)
        return self.side

    def flipn(self, n):
        for i in range(n):
            self.side = random.randint(0,1)
        return self.side

class Flowers:
    def __init__(self, name="Flowers", starting_amount=50):
        self.name = name
        self.amount = starting_amount

class MenuScene(ezpygame.Scene):
    def __init__(self):
        super().__init__()
        self.coin = Coin()
        self.currency = Flowers()
        self.font = pygame.font.SysFont("Monospace", size=12)

    def on_enter(self, previous_scene):
        self.application.title = "Main menu(1)"

    def draw(self, screen):
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (250, 5, 5), (100, 100+1*16, 100, 50))
        pygame.draw.rect(screen, (250, 5, 5), (100, 100+50+2*16, 100, 50))
        pygame.draw.rect(screen, (250, 5, 5), (100, 100+2*50+3*16, 100, 50))
        screen.blit(self.font.render("Start", True, (0, 0, 0)), (150, 100+16))
        screen.blit(self.font.render("Options", True, (0, 0, 0)), (150, 100+50+2*16))
        screen.blit(self.font.render("Exit", True, (0, 0, 0)), (150, 100+2*50+3*16))

class GameScene(ezpygame.Scene):
    def __init__(self):
        super().__init__()
        self.coin = Coin()
        self.currency = Flowers()

    def on_enter(self, previous_scene):
        self.application.title = "Game(2)"

    def draw(self, screen):
        screen.fill((0,0,0))


app = ezpygame.Application(
        title="Test",
        resolution=(640, 480),
        update_rate=60,
)
menu = MenuScene()
app.run(menu)
"""
class Game:
    def __init__(self):
        self.flowers = Flowers()
        self.coin = Coin()
        self.running = True
        self.bet_rate = 0.95
        self.main_loop()

    def main_loop(self):
        while self.running == True:
            print("---%s flowers" % self.flowers.amount)
            cmd = input(">>>")
            if len(cmd) < 1:
                continue
            if cmd[0] == "b":
                cmd = cmd.split(" ")
                if len(cmd) <= 2:
                    print("b[et] amount side(t|h)")
                    continue
                amount = int(cmd[1])
                side_bet = self.coin.rsides[cmd[2]]
                if (self.flowers.amount < amount):
                    continue
                if (self.coin.flip() == side_bet):
                    self.flowers.amount += int(amount*self.bet_rate)
                    print("You won %s flowers!" % str(int(amount*self.bet_rate)))
                    continue
                else:
                    self.flowers.amount -= amount
                    print("You lost %s flowers. Better luck next time!" % amount)

            if cmd[0] == "f":
                times = cmd.split(" ")[-1]
                if not(times == cmd):
                    self.coin.flipn(int(times))
                    print("Flipped coin %s times, result: %s" % (times, self.coin.sides[self.coin.side]))
                    continue
                else:
                    self.coin.flip()
                    print("Flipped coin, result: %s" % self.coin.sides[self.coin.side])

x = Game()
"""
