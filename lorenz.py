import numpy as np
import matplotlib.pyplot as plt
import os

class Lorenz:
    def __init__(self, wealth_values):
        self.wealth_values = wealth_values

    def calculate_lorenz_curve(self):
        self.wealth_values.sort()
        n = len(self.wealth_values)
        cumulative_wealth = np.cumsum(self.wealth_values) / sum(self.wealth_values)
        cumulative_wealth = np.insert(cumulative_wealth, 0, 0)

        self.lorenz_curve_x = np.linspace(0, 1, n+1)
        self.lorenz_curve_y = cumulative_wealth

    def calculate_gini_coefficient(self):
        # Calculate the area between the Lorenz curve and the line of perfect equality
        area_between_curve_and_line = 0.5 - np.trapz(self.lorenz_curve_y, self.lorenz_curve_x)

        # Calculate the area under the line of perfect equality
        area_under_line_of_equality = 0.5

        # Calculate the Gini coefficient
        gini_coefficient = area_between_curve_and_line / area_under_line_of_equality

        return gini_coefficient

    def plot_show(self):
        plt.figure(figsize=(8, 6))
        plt.plot(self.lorenz_curve_x, self.lorenz_curve_y, marker='o', linestyle='-')
        plt.plot([0, 1], [0, 1], linestyle='--', color='gray')  # The line of perfect equality
        plt.fill_between(self.lorenz_curve_x, self.lorenz_curve_y, self.lorenz_curve_x, alpha=0.2)
        
        # Display the Gini coefficient on the graph
        gini_coefficient = self.calculate_gini_coefficient()
        plt.text(0.7, 0.2, f'Gini Coefficient: {gini_coefficient:.2f}', fontsize=12, color='red')
        
        plt.title('Lorenz Curve')
        plt.xlabel('Cumulative Population (%)')
        plt.ylabel('Cumulative Wealth (%)')
        plt.grid(True)
        plt.show()

    def plot_save(self, sample_name, plot_title="Lorenz Curve"):
        subfolder = "LorenzPlots"
        file_name = f"{sample_name}_lorenz_curve.png"
        file_path = os.path.join(subfolder, file_name)

        if not os.path.exists(subfolder):
            os.makedirs(subfolder)

        plt.figure(figsize=(8, 6))
        plt.plot(self.lorenz_curve_x, self.lorenz_curve_y, marker='o', linestyle='-')
        plt.plot([0, 1], [0, 1], linestyle='--', color='gray')  # The line of perfect equality
        plt.fill_between(self.lorenz_curve_x, self.lorenz_curve_y, self.lorenz_curve_x, alpha=0.2)

        # Display the Gini coefficient on the graph
        gini_coefficient = self.calculate_gini_coefficient()
        plt.text(0.7, 0.2, f'Gini Coefficient: {gini_coefficient:.2f}', fontsize=12, color='red')

        plt.title(plot_title)  # Use the provided plot title
        plt.xlabel('Cumulative Population (%)')
        plt.ylabel('Cumulative Wealth (%)')
        plt.grid(True)
        plt.savefig(file_path)
        plt.close()

    def get_gini_coefficient(self):
        return self.calculate_gini_coefficient()


