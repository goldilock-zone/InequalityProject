import pygame
import sys
import random
import math

class Incentives:
    def __init__(self, x, y, size, speed=1):
        self.x = x
        self.y = y
        self.radius = size
        self.color = (255, 255, 0)  # Yellow color
        self.speed = speed
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Randomly change direction
        if random.random() < 0.1:
            self.angle += random.uniform(-0.2, 0.2)

        # Bounce off the screen edges
        if self.x + self.radius > screen_width:
            self.x = screen_width - self.radius
            self.angle = math.pi - self.angle
        elif self.x - self.radius < 0:
            self.x = self.radius
            self.angle = math.pi - self.angle

        if self.y + self.radius > screen_height:
            self.y = screen_height - self.radius
            self.angle = -self.angle
        elif self.y - self.radius < 0:
            self.y = self.radius
            self.angle = -self.angle

    def change_speed(self, increment):
        self.speed += increment

class Players:
    def __init__(self, x, y, size, speed=0.2, sensing_radius=100):
        self.x = x
        self.y = y
        self.radius = size
        self.color = (0, 255, 0)  # Green color
        self.speed = speed
        self.angle = random.uniform(0, 2 * math.pi)
        self.sensing_radius = sensing_radius

    def move(self, incentives):
        # Calculate the direction based on yellow dots density
        x_sum = 0
        y_sum = 0

        for incentive in incentives:
            if (
                abs(incentive.x - self.x) <= self.sensing_radius
                and abs(incentive.y - self.y) <= self.sensing_radius
            ):
                x_sum += incentive.x
                y_sum += incentive.y

        if x_sum == 0 and y_sum == 0:
            return  # No nearby yellow dots, stay in place

        target_angle = math.atan2(y_sum - self.y, x_sum - self.x)

        # Randomly change direction
        if random.random() < 0.1:
            target_angle += random.uniform(-0.2, 0.2)

        # Move towards the calculated direction
        self.angle = target_angle
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Wrap around to the opposite side of the screen
        if self.x > screen_width:
            self.x = 0
        elif self.x < 0:
            self.x = screen_width
        if self.y > screen_height:
            self.y = 0
        elif self.y < 0:
            self.y = screen_height

class IncentiveManager:
    def __init__(self, screen_width, screen_height, density=1000, size=3, speed=0.2):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.density = density
        self.size = size
        self.speed = speed
        self.incentives = []

        # Initialize incentives with non-uniformly spaced positions
        for _ in range(density):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            incentive = Incentives(x, y, size, speed)
            self.incentives.append(incentive)

    def move(self):
        for incentive in self.incentives:
            incentive.move()

    def change_speed(self, increment):
        for incentive in self.incentives:
            incentive.change_speed(increment)

class PlayersManager:
    def __init__(self, screen_width, screen_height, density=100, size=3, speed=0.2, sensing_radius=100):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.density = density
        self.size = size
        self.speed = speed
        self.sensing_radius = sensing_radius
        self.players = []

        # Calculate spacing between players
        spacing_x = int(screen_width / (density ** 0.5))
        spacing_y = int(screen_height / (density ** 0.5))

        # Initialize players with uniformly spaced positions
        for y in range(0, screen_height, spacing_y):
            for x in range(0, screen_width, spacing_x):
                player = Players(x, y, size, speed, sensing_radius)
                self.players.append(player)

    def move(self, incentives):
        for player in self.players:
            player.move(incentives)

    def change_speed(self, increment):
        for player in self.players:
            player.change_speed(increment)

# Constants
screen_width = 800
screen_height = 600

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pygame Window")
        self.clock = pygame.time.Clock()
        self.is_running = True

        self.incentive_manager = IncentiveManager(screen_width, screen_height)
        self.players_manager = PlayersManager(screen_width, screen_height, density=10, size=10, speed=0.2, sensing_radius=100)

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.incentive_manager.change_speed(1)
                        self.players_manager.change_speed(0.1)
                    elif event.key == pygame.K_DOWN:
                        self.incentive_manager.change_speed(-1)
                        self.players_manager.change_speed(-0.1)

            self.incentive_manager.move()
            self.players_manager.move(self.incentive_manager.incentives)
            self.update()
            self.render()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

    def update(self):
        # Add game logic here
        pass

    def render(self):
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        for incentive in self.incentive_manager.incentives:
            pygame.draw.circle(self.screen, incentive.color, (int(incentive.x), int(incentive.y)), incentive.radius)
        for player in self.players_manager.players:
            pygame.draw.circle(self.screen, player.color, (int(player.x), int(player.y)), player.radius)
        pygame.display.flip()

if __name__ == "__main__":
    game = Game()
    game.run()
