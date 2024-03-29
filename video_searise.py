import pygame
import os
import numpy as np
import pandas as pd

# Define constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
SEA_COLOR = (0, 0, 255)  # Blue
SEA_START_HEIGHT = 600
SEA_LEVEL_RISE_RATE =0.7
FPS = 10
DATA_FILE = 'sea_level_data.csv'
TOTAL_FRAMES = 0  # This will be determined based on the dataset

# Read sea level data from CSV
sea_level_data = pd.read_csv(DATA_FILE)

# Extract July sea level data for each year and calculate relative sea levels
initial_sea_level = sea_level_data.loc[sea_level_data['Time'].str.endswith('-07-15'), 'GMSL'].iloc[0]
sea_level_data['Relative_GMSL'] = sea_level_data['GMSL'] - initial_sea_level

# Extract years and relative sea levels
YEARS = sea_level_data['Time'].str[:4].astype(int)
RELATIVE_GMSL = sea_level_data['Relative_GMSL']

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Global Sea Level Rise")

# Create frames directory if it doesn't exist
if not os.path.exists('frames'):
    os.makedirs('frames')

# Main loop
clock = pygame.time.Clock()

# Calculate total frames
TOTAL_FRAMES = len(YEARS)

# Calculate initial water level position
initial_water_level_y = WINDOW_HEIGHT - SEA_START_HEIGHT

# Calculate water level change for each frame
water_level_change = np.diff(sea_level_data['GMSL'])

for i, (year, relative_gmsl, change) in enumerate(zip(YEARS, RELATIVE_GMSL, water_level_change)):
    # Calculate current sea level
    sea_height = SEA_START_HEIGHT + relative_gmsl * SEA_LEVEL_RISE_RATE
    
    # Calculate current water level position
    current_water_level_y = WINDOW_HEIGHT - sea_height
    
    # Draw the sea
    screen.fill((255, 255, 255))  # White background
    pygame.draw.rect(screen, SEA_COLOR, (0, current_water_level_y, WINDOW_WIDTH, sea_height))
    
    # Draw initial condition marker
    pygame.draw.line(screen, (255, 0, 0), (0, initial_water_level_y), (WINDOW_WIDTH, initial_water_level_y), 2)
    
    # Display year and difference between initial and current sea levels
    font = pygame.font.Font(None, 36)
    difference_text = f"Difference from Initial: {relative_gmsl:.2f}"
    year_text = f"Year: {year}"
    text_surface = font.render(f"{year_text} - {difference_text}", True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))
    
    pygame.display.flip()

    # Capture frames
    pygame.image.save(screen, f'frames/frame_{i:04d}.png')

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    clock.tick(FPS)

# Quit Pygame
pygame.quit()

