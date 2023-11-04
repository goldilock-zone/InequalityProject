import pygame
import sys
import os
import random
import math
from lorenz import Lorenz
import csv
import numpy as np
from scipy.stats import skew, kurtosis

# Global variable to control the overall size of entities
ENTITY_SIZE_FACTOR = 0.5

class Incentives:
    def __init__(self, x, y, size, speed=1):
        self.x = x
        self.y = y
        self.radius = size
        self.color = (255, 255, 0)  # Yellow color
        self.speed = speed * ENTITY_SIZE_FACTOR  # Adjust speed based on size factor
        self.angle = random.uniform(0, 2 * math.pi)

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Randomly change direction
        if random.random() < 0.1:
            self.angle += random.uniform(-0.2, 0.2)

        # Wrap around to the opposite side of the screen
        if self.x > screen_width:
            self.x = 0
        elif self.x < 0:
            self.x = screen_width
        if self.y > screen_height:
            self.y = 0
        elif self.y < 0:
            self.y = screen_height

    def change_speed(self, increment):
        self.speed += increment

class Players:
    def __init__(self, x, y, size, speed=2, sensing_radius=100):
        self.x = x
        self.y = y
        self.radius = size * ENTITY_SIZE_FACTOR  # Adjust size based on size factor
        self.color = (0, 255, 0)  # Green color
        self.speed = speed * ENTITY_SIZE_FACTOR  # Adjust speed based on size factor
        self.angle = random.uniform(0, 2 * math.pi)
        self.sensing_radius = sensing_radius
        self.wealth = 0  # Initialize wealth attribute

    def move(self, incentives):
        # Calculate the direction based on proximity to yellow dots
        eaten_incentives = []

        for incentive in incentives:
            distance = math.sqrt((self.x - incentive.x) ** 2 + (self.y - incentive.y) ** 2)
            if distance < self.sensing_radius:
                eaten_incentives.append(incentive)

        if not eaten_incentives:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

            # Wrap around to the opposite side of the screen
            self.x %= screen_width
            self.y %= screen_height

            return  # No nearby yellow dots, stay in place

        target_incentive = random.choice(eaten_incentives)
        target_angle = math.atan2(target_incentive.y - self.y, target_incentive.x - self.x)

        # Randomly change direction
        if random.random() < 0.1:
            target_angle += random.uniform(-0.2, 0.2)

        # Move towards the calculated direction
        self.angle = target_angle
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Wrap around to the opposite side of the screen
        self.x %= screen_width
        self.y %= screen_height

        # Remove eaten incentives, increase player's wealth, and increase player's radius
        for eaten_incentive in eaten_incentives:
            incentives.remove(eaten_incentive)
            self.wealth += 1  # Increase player's wealth when eating an incentive
            self.radius += 1  # Increase player's radius when eating an incentive

    def change_speed(self, increment):
        self.speed += increment

class IncentiveManager:
    def __init__(self, screen_width, screen_height, density=1000, size=3):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.density = density
        self.size = size * ENTITY_SIZE_FACTOR  # Adjust size based on size factor
        self.incentives = []

        # Initialize incentives with non-uniformly spaced positions
        for _ in range(density):
            x = random.randint(0, screen_width)
            y = random.randint(0, screen_height)
            incentive = Incentives(x, y, size)
            self.incentives.append(incentive)
        
        self.num_incentives  = len(self.incentives)

    def move(self):
        for incentive in self.incentives:
            incentive.move()

    def change_speed(self, increment):
        for incentive in self.incentives:
            incentive.change_speed(increment)

class PlayersManager:
    def __init__(self, screen_width, screen_height, density=100, size=10, speed=1, sensing_radius=10):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.density = density
        self.size = size * ENTITY_SIZE_FACTOR  # Adjust size based on size factor
        self.speed = speed * ENTITY_SIZE_FACTOR  # Adjust speed based on size factor
        self.sensing_radius = sensing_radius
        self.players = []

        # Initialize players with uniformly spaced positions
        for y in range(0, screen_height, density):
            for x in range(0, screen_width, density):
                player = Players(x, y, size, speed, sensing_radius)
                self.players.append(player)
        
        self.num_players = len(self.players)

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
    def __init__(self, players_density, incentives_density, sensing_radius, screenshot_name = "x"):
        pygame.init()
        self.players_density = players_density
        self.incentives_density = incentives_density
        self.sensing_radius = sensing_radius
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Pygame Window")
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.screenshot_name = screenshot_name

        self.incentive_manager = IncentiveManager(screen_width, screen_height, self.incentives_density, size=3)
        self.players_manager = PlayersManager(screen_width, screen_height, self.players_density, size=5, speed=2, sensing_radius=self.sensing_radius )

    def screenshot_name_set(self, screenshot_name):
        self.screenshot_name = screenshot_name

    def run(self):
        run_times = 0
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.incentive_manager.change_speed(1)
                        self.players_manager.change_speed(0.01)
                    elif event.key == pygame.K_DOWN:
                        self.incentive_manager.change_speed(-1)
                        self.players_manager.change_speed(-0.01)

            self.incentive_manager.move()
            self.players_manager.move(self.incentive_manager.incentives)
            self.update()
            self.render()
            self.clock.tick(60)
            run_times += 1

            if run_times >= 1000:
                pygame.image.save(self.screen, self.screenshot_name)
                self.is_running = False


        pygame.quit()
        wealth_list = []
        for player in self.players_manager.players:
            wealth_list.append(player.wealth)
        return wealth_list, self.players_manager.num_players, self.incentive_manager.num_incentives
        
    def update(self):
        # Add game logic here
        pass

    def render(self):
        self.screen.fill((255, 255, 255))  # Fill the screen with white
        for incentive in self.incentive_manager.incentives:
            pygame.draw.circle(self.screen, incentive.color, (int(incentive.x), int(incentive.y)), int(incentive.radius))
        for player in self.players_manager.players:
            pygame.draw.circle(self.screen, player.color, (int(player.x), int(player.y)), int(player.radius))
        pygame.display.flip()

if __name__ == "__main__":
    with open('experiment_results1.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "sample_name", 
            "number_of_players", 
            "number_of_incentives", 
            "mean_wealth", 
            "median_wealth", 
            "std_wealth", 
            "skewness", 
            "kurtosis", 
            "gini_coefficient"
        ])

        game = Game(players_density = 100, incentives_density = 1000, sensing_radius=10)
        wealth_values, num_players, num_incentives = game.run()
        lorenz = Lorenz(wealth_values)
        lorenz.calculate_lorenz_curve()
        gini_coefficient = lorenz.get_gini_coefficient()

        number_of_players = num_players
        number_of_incentives = num_incentives

        sample_name = "PIDC_single" + "plyr_" + str(num_players) + "_" + "inctvs_" + str(num_incentives) + "_"

        lorenz.plot_save(sample_name, plot_title=sample_name)
        # Calculate the mean
        mean_wealth = np.mean(wealth_values)

        # Calculate the median
        median_wealth = np.median(wealth_values)

        # Calculate the standard deviation (std)
        std_wealth = np.std(wealth_values)

        # Calculate the skewness
        skewness_wealth = skew(wealth_values)

        # Calculate the kurtosis
        kurtosis_wealth = kurtosis(wealth_values)

        with open('experiment_results2.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                sample_name, 
                number_of_players, 
                number_of_incentives, 
                mean_wealth, 
                median_wealth, 
                std_wealth, 
                skewness_wealth, 
                kurtosis_wealth, 
                gini_coefficient
            ])
        print(f"Sample Name: {sample_name}")
        



