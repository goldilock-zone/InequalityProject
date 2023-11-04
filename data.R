# Install and load the plotly library
install.packages("plotly")
library(plotly)
install.packages("dplyr")
library(dplyr)

# Read data from CSV file
data <- read.csv("final.csv")

# Select the variables for X, Y, and Z axes
x_variable <- data$number_of_players
y_variable <- data$number_of_incentives
z_variable <- data$gini_coefficient

model1 <- lm(gini_coefficient ~ number_of_players + number_of_incentives + mean_wealth +
              median_wealth + std_wealth + skewness + kurtosis, data = data)

# Print the summary of the linear model
summary(model1)

model2 <- lm(gini_coefficient ~ number_of_players + number_of_incentives, data = data)
summary(model2)

# Create a 3D surface plot
plot_ly(x = x_variable, y = y_variable, z = z_variable, type = "scatter3d", mode = "markers",
        marker = list(
          color = "green",  # Map color to the fourth variable
          size = 2,    # Map size to the fourth variable
          colorscale = "Viridis"  # Choose a color scale (optional)
        )) %>%
  layout(scene = list(
    xaxis = list(title = "number_of_players"),
    yaxis = list(title = "number_of_incentives"),
    zaxis = list(title = "gini_coefficient")
  ))

# Optionally, you can further customize the plot by adjusting labels, colors, and other plot properties as needed.
# Read data from your CSV file

# Select the relevant columns (excluding "sample_name")
library(ggplot2)
library(cowplot)
selected_cols <- c("number_of_players", "number_of_incentives", "mean_wealth",
                   "median_wealth", "std_wealth", "skewness", "kurtosis", "gini_coefficient")

# Create an empty list to store scatter plots
scatter_plots <- list()

# Loop through all pairs of selected columns
for (i in 1:(length(selected_cols) - 1)) {
  for (j in (i + 1):length(selected_cols)) {
    x_var <- selected_cols[i]
    y_var <- selected_cols[j]
    
    # Create a scatter plot using ggplot2 with less dark and more transparent dots and a line of best fit
    plot <- ggplot(data, aes_string(x = x_var, y = y_var)) +
      geom_point(alpha = 0.2) +  # Adjust alpha for transparency
      geom_smooth(method = "lm", se = FALSE, color = "blue") +  # Add a line of best fit
      labs(title = paste(x_var, "vs", y_var))
    
    # Add the scatter plot to the list
    scatter_plots[[paste(x_var, "vs", y_var)]] <- plot
  }
}

# Arrange and display the scatter plots using cowplot
plot_grid(plotlist = scatter_plots)

