import random
import pygame
import ezpygame
import math

#TODO: handle bets, choose t and h side

def load_png(name):
    """
    Load image and return image object
    """
    try:
        image = pygame.image.load(name)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        print("Cannot load image: %s" % name)
    return image, image.get_rect()

class FontHandling:
    def __init__(self, name, letter_order, width, height):
        self.image = load_png(name)[0]
        self.letters = []
        for i in letter_order:
            self.letters += i
        self.letters_images = []
        self.width = width
        self.height = height
        self.letters_d = {}
        self.split_image()

    def render(self, text):
        #create surface (consider self.width and self.height)
        #put letters ~2px apart of each
        #if space then move whole self.width+2
        #ignore any punctuation marks
        bl = 2
        current_x = self.width
        surf = pygame.Surface(((self.width+bl)*len(text)+self.width, self.height))
        for i in text:
            if i in self.letters_d.keys():
                print(i)
                surf.blit(self.letters_d[i], (current_x, 0))
                current_x += self.width+bl
            elif i == " ":
                current_x += self.width+bl
            else:
                pass
        return surf
   
    def split_image(self):
        for x in range(len(self.letters)):
            rect = (0+self.width*x, 0, self.width, self.height)
            surface = pygame.Surface((self.width, self.height)).convert_alpha()
            surface.blit(self.image, (0, 0), area=rect)
            self.letters_images += [surface]
        for i, j in zip(self.letters, self.letters_images):
            self.letters_d.update({i: j})
            #print(self.letters_d)

def isPointInsideRect(pos, rect):
    """
    Checks if point is inside some rectangle (Rect object)
    :param x: horizontal
    :param y: vertical
    :param rect: rect to check inside
    :return: bool
    """
    x = pos[0]
    y = pos[1]
    if (x > rect[0]) and (x < rect[0]+rect[2]) and (y > rect[1]) and (y < rect[1]+rect[3]):
        return True
    else:
        return False

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
        self.bet = 0
        self.current_bet = "tails"
        self.bet_rate = 0.95
        self.font = FontHandling("font.png", "qwertyuiopasdfghjklzxcvbnm1234567890", 12, 16)
        #self.font = pygame.font.SysFont("Monospace", size=12)

    def on_enter(self, previous_scene):
        self.application.title = "Game(2)"

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if isPointInsideRect(pos, (100, 100, 100, 100)):
                self.coin.flip()
                if self.coin.sides[self.coin.side] == self.current_bet:
                    self.currency.amount += int(self.bet*self.bet_rate)
                else:
                   self.currency.amount -= self.bet
                   if self.currency.amount < 0:
                       self.currency.amount = 0
            if isPointInsideRect(pos, (10, 10, 10, 10)):
                if self.currency.amount > self.bet+1:
                    self.bet += 1
            if isPointInsideRect(pos, (10, 28, 10, 10)):
                if 0 <= self.bet-1:
                    self.bet -= 1
            if isPointInsideRect(pos, (10, 28+18, 10, 10)):
                self.current_bet = "tails"
            if isPointInsideRect(pos, (10, 28+2*18, 10, 10)):
                self.current_bet = "heads"

    def draw(self, screen):
        screen.fill((0,0,0))
        pygame.draw.rect(screen, (250, 5, 5), (10, 10, 10, 10))
        pygame.draw.rect(screen, (250, 5, 5), (10, 28, 10, 10))
        screen.blit(self.font.render("+"), (10, 10))
        screen.blit(self.font.render("-"), (10, 28))
        screen.blit(self.font.render("tails"), (10, 28+18))
        screen.blit(self.font.render("heads"), (10, 28+2*18))
        if self.current_bet == "tails":
            pygame.draw.rect(screen, (0, 255, 0), (10, 28+18, 10, 10))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (10, 28+18, 10, 10))

        if self.current_bet == "heads":
            pygame.draw.rect(screen, (0, 255, 0), (10, 28+2*18, 10, 10))
        else:
            pygame.draw.rect(screen, (255, 0, 0), (10, 28+2*18, 10, 10))

        pygame.draw.rect(screen, (255, 0, 255), (100, 100, 100, 100))
        screen.blit(self.font.render("Coin flip"), (150, 150))
        screen.blit(self.font.render("Coin side: %s" % self.coin.sides[self.coin.side]), (0, 400))
        screen.blit(self.font.render("Bet: %s  Flowers: %s" % (self.bet, self.currency.amount)), (0, 416))


app = ezpygame.Application(
        title="Test",
        resolution=(640, 480),
        update_rate=60,
)
menu = MenuScene()
app.run(GameScene())
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
