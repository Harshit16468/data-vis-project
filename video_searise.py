import pygame  # Importing the pygame library
import os  # Importing the os library for working with files and directories
import numpy as np  # Importing the numpy library for numerical operations
import pandas as pd  # Importing the pandas library for working with data frames

# Define constants
WINDOW_WIDTH = 1200  # Width of the window
WINDOW_HEIGHT = 800  # Height of the window
SEA_COLOR = (0, 0, 255)  # Blue color for the sea
SEA_START_HEIGHT = 600  # Initial height of the sea
SEA_LEVEL_RISE_RATE = 0.7  # Rate of sea level rise
FPS = 10  # Frames per second
DATA_FILE = 'sea_level_data.csv'  # File containing sea level data
TOTAL_FRAMES = 0  # This will be determined based on the dataset

# Read sea level data from CSV
sea_level_data = pd.read_csv(DATA_FILE)  # Reading the CSV file

# Extract July sea level data for each year and calculate relative sea levels
initial_sea_level = sea_level_data.loc[sea_level_data['Time'].str.endswith('-07-15'), 'GMSL'].iloc[0]  # Getting the initial sea level
sea_level_data['Relative_GMSL'] = sea_level_data['GMSL'] - initial_sea_level  # Calculating relative sea level

# Extract years and relative sea levels
YEARS = sea_level_data['Time'].str[:4].astype(int)  # Extracting years
RELATIVE_GMSL = sea_level_data['Relative_GMSL']  # Extracting relative sea levels

# Initialize Pygame
pygame.init()  # Initializing Pygame
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Creating the window
pygame.display.set_caption("Global Sea Level Rise")  # Setting the window caption

# Create frames directory if it doesn't exist
if not os.path.exists('frames'):
    os.makedirs('frames')  # Creating the 'frames' directory if it doesn't exist

# Main loop
clock = pygame.time.Clock()  # Creating a clock object for controlling the frame rate

# Calculate total frames
TOTAL_FRAMES = len(YEARS)  # Calculating the total number of frames based on the number of years

# Calculate initial water level position
initial_water_level_y = WINDOW_HEIGHT - SEA_START_HEIGHT  # Calculating the initial water level position

# Calculate water level change for each frame
water_level_change = np.diff(sea_level_data['GMSL'])  # Calculating the water level change for each frame

for i, (year, relative_gmsl, change) in enumerate(zip(YEARS, RELATIVE_GMSL, water_level_change)):
    # Calculate current sea level
    sea_height = SEA_START_HEIGHT + relative_gmsl * SEA_LEVEL_RISE_RATE  # Calculating the current sea level

    # Calculate current water level position
    current_water_level_y = WINDOW_HEIGHT - sea_height  # Calculating the current water level position

    # Draw the sea
    screen.fill((255, 255, 255))  # Filling the screen with white color (background)
    pygame.draw.rect(screen, SEA_COLOR, (0, current_water_level_y, WINDOW_WIDTH, sea_height))  # Drawing the sea

    # Draw initial condition marker
    pygame.draw.line(screen, (255, 0, 0), (0, initial_water_level_y), (WINDOW_WIDTH, initial_water_level_y), 2)  # Drawing the initial condition marker

    # Display year and difference between initial and current sea levels
    font = pygame.font.Font(None, 36)  # Creating a font object
    difference_text = f"Difference from Initial: {relative_gmsl:.2f}"  # Formatting the difference text
    year_text = f"Year: {year}"  # Formatting the year text
    text_surface = font.render(f"{year_text} - {difference_text}", True, (0, 0, 0))  # Rendering the text
    screen.blit(text_surface, (10, 10))  # Blitting (drawing) the text on the screen

    pygame.display.flip()  # Updating the display

    # Capture frames
    pygame.image.save(screen, f'frames/frame_{i:04d}.png')  # Saving the current frame as a PNG image

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    clock.tick(FPS)  # Controlling the frame rate

# Quit Pygame
pygame.quit()

# Command to compile the frames into a video using ffmpeg
ffmpeg_command = f"ffmpeg -r {FPS} -i frames/frame_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p sea_level_rise.mp4"
os.system(ffmpeg_command)
