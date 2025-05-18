import pygame
import random
import sys
import time
import os
import traceback

# Initialize Pygame
pygame.init()
pygame.mixer.init()  # Initialize mixer for sounds

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
PIG_SIZE = 50
BIRD_SIZE = 30
BIRD_WIDTH = 100
BIRD_HEIGHT = 150
BIRD_GAP = 200
LUCKY_BLOCK_SIZE = 30
LUCKY_BLOCK_CHANCE = 0.9  # 90% chance to spawn a lucky block
LUCKY_BLOCK_POINTS = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
GOLD = (255, 215, 0)

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dubai Flying Pig Game")

clock = pygame.time.Clock()

# Set up sound effects
try:
    COLLECT_SOUND = pygame.mixer.Sound('collect.wav')
except:
    COLLECT_SOUND = None

# Set up bird images after display is initialized
BIRD_IMAGES = []
BIRD_IMAGE_PATHS = [
    'images/bird_1.png',
    'images/bird_2.png',
    'images/bird_3.png',
]

# Try to load bird images
for path in BIRD_IMAGE_PATHS:
    try:
        print(f"\n=== Trying to load bird image: {path} ===")
        print(f"Path exists: {os.path.exists(path)}")
        print(f"Is file: {os.path.isfile(path)}")
        print(f"File size: {os.path.getsize(path) if os.path.exists(path) else 'N/A'} bytes")
        
        img = pygame.image.load(path)
        print(f"Image loaded successfully")
        print(f"Image size: {img.get_size()}")
        
        img = pygame.transform.scale(img, (BIRD_SIZE, BIRD_SIZE))
        img.convert_alpha()
        BIRD_IMAGES.append(img)
        print(f"Successfully loaded bird image: {path}")
    except Exception as e:
        print(f"Failed to load bird image {path}: {str(e)}")
        import traceback
        print("Full error trace:")
        traceback.print_exc()

# If we have no images, try to find any PNG files in the images folder
if not BIRD_IMAGES:
    print("No images loaded from paths. Searching for PNG files in images folder...")
    for file in os.listdir('images'):
        if file.lower().endswith('.png') or file.lower().endswith('.pn'):
            try:
                path = os.path.join('images', file)
                print(f"Found image file: {path}")
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (BIRD_SIZE, BIRD_SIZE))
                img.convert_alpha()
                BIRD_IMAGES.append(img)
                print(f"Successfully loaded image: {path}")
            except Exception as e:
                print(f"Failed to load image {path}: {str(e)}")

if not BIRD_IMAGES:
    print("No bird images found. Using default bird shape.")
    # Create simple bird shapes if images not found
    bird_surface = pygame.Surface((BIRD_SIZE, BIRD_SIZE), pygame.SRCALPHA)
    pygame.draw.polygon(bird_surface, (255, 215, 0), [(0, BIRD_SIZE//2), (BIRD_SIZE, 0), (BIRD_SIZE, BIRD_SIZE)])
    pygame.draw.circle(bird_surface, (0, 0, 0), (BIRD_SIZE//4, BIRD_SIZE//4), 2)  # Eye
    BIRD_IMAGES.append(bird_surface)  # Use the same bird for all positions

# Set up background images
BACKGROUND_IMAGES = []
BACKGROUND_IMAGE_PATHS = ['images/dubai_1.png', 'images/dubai_2.png', 'images/dubai_3.png']

# Try to load background images
for path in BACKGROUND_IMAGE_PATHS:
    try:
        print(f"Trying to load background image: {path}")
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        BACKGROUND_IMAGES.append(img)
        print(f"Successfully loaded background image: {path}")
    except Exception as e:
        print(f"Failed to load background image {path}: {str(e)}")

if not BACKGROUND_IMAGES:
    print("No background images found. Using default white background.")
    BACKGROUND_IMAGES.append(pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT)))
    BACKGROUND_IMAGES[0].fill(WHITE)
    for file in os.listdir('images'):
        if file.lower().endswith('.png') or file.lower().endswith('.pn'):
            try:
                path = os.path.join('images', file)
                print(f"Found image file: {path}")
                img = pygame.image.load(path)
                img = pygame.transform.scale(img, (BIRD_SIZE, BIRD_SIZE))
                img.convert_alpha()
                BIRD_IMAGES.append(img)
                print(f"Successfully loaded image: {path}")
            except Exception as e:
                print(f"Failed to load image {path}: {str(e)}")

if not BIRD_IMAGES:
    print("No bird images found. Using default bird shape.")
    # Create simple bird shapes if images not found
    bird_surface = pygame.Surface((BIRD_SIZE, BIRD_SIZE), pygame.SRCALPHA)
    pygame.draw.polygon(bird_surface, (255, 215, 0), [(0, BIRD_SIZE//2), (BIRD_SIZE, 0), (BIRD_SIZE, BIRD_SIZE)])
    pygame.draw.circle(bird_surface, (0, 0, 0), (BIRD_SIZE//4, BIRD_SIZE//4), 2)  # Eye
    BIRD_IMAGES.append(bird_surface)  # Use the same bird for all positions

# Set up background images
BACKGROUND_IMAGES = []
BACKGROUND_IMAGE_PATHS = ['images/dubai_1.png', 'images/dubai_2.png', 'images/dubai_3.png']

# Try to load background images
for path in BACKGROUND_IMAGE_PATHS:
    try:
        print(f"Trying to load background image: {path}")
        img = pygame.image.load(path)
        img = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
        BACKGROUND_IMAGES.append(img)
        print(f"Successfully loaded background image: {path}")
    except Exception as e:
        print(f"Failed to load background image {path}: {str(e)}")

if not BACKGROUND_IMAGES:
    print("No background images found. Using default white background.")

# Set up sound effects
try:
    COLLECT_SOUND = pygame.mixer.Sound('collect.wav')
except:
    COLLECT_SOUND = None

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Dubai Flying Pig Game")

clock = pygame.time.Clock()

# Background class
class Background:
    def __init__(self):
        self.x = 0
        self.speed = 2
        self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.image.fill(WHITE)  # Default white background
        
        # Try to load Dubai background images
        try:
            for i in range(1, 4):  # Try to load up to 3 images
                try:
                    img = pygame.image.load(f'images/dubai_{i}.png')
                    img = pygame.transform.scale(img, (WINDOW_WIDTH, WINDOW_HEIGHT))
                    self.image = img
                    break  # Use the first successfully loaded image
                except:
                    continue
        except:
            pass
    
    def move(self):
        self.x -= self.speed
        if self.x <= -WINDOW_WIDTH:
            self.x = 0
            # Reset to default white if no images found
            self.image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.image.fill(WHITE)
    
    def draw(self):
        # Draw two copies of the background to create scrolling effect
        screen.blit(self.image, (self.x, 0))
        screen.blit(self.image, (self.x + WINDOW_WIDTH, 0))

# Player class
class LuckyBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = LUCKY_BLOCK_SIZE
        self.height = LUCKY_BLOCK_SIZE
        self.speed = 5
        self.spawn_time = time.time()
        self.duration = 5  # Lucky blocks disappear after 5 seconds
    
    def move(self):
        self.x -= self.speed
    
    def draw(self):
        pygame.draw.rect(screen, GOLD, (self.x, self.y, self.width, self.height))
    
    def off_screen(self):
        return self.x + self.width < 0 or time.time() - self.spawn_time > self.duration

class Player:
    def __init__(self):
        try:
            # Try to load pig image
            self.image = pygame.image.load(os.path.join('images', 'flying_pig.png'))
            self.image = pygame.transform.scale(self.image, (PIG_SIZE, PIG_SIZE))
            # Make sure the image has a transparent background
            self.image.convert_alpha()
        except Exception as e:
            print(f"Error loading pig image: {str(e)}")
            # If image not found, create a simple pig-like shape with transparency
            self.image = pygame.Surface((PIG_SIZE, PIG_SIZE), pygame.SRCALPHA)
            # Draw a more pig-like shape with transparency
            # Body (with transparency)
            pygame.draw.circle(self.image, (200, 100, 100, 200), (PIG_SIZE//2, PIG_SIZE//2), PIG_SIZE//2)  # Body
            # Eyes
            pygame.draw.circle(self.image, (255, 255, 255, 200), (PIG_SIZE//3, PIG_SIZE//3), 3)  # Eye
            pygame.draw.circle(self.image, (255, 255, 255, 200), (2*PIG_SIZE//3, PIG_SIZE//3), 3)  # Eye
            # Pupils
            pygame.draw.circle(self.image, (0, 0, 0, 255), (PIG_SIZE//3, PIG_SIZE//3), 1)  # Pupil
            pygame.draw.circle(self.image, (0, 0, 0, 255), (2*PIG_SIZE//3, PIG_SIZE//3), 1)  # Pupil
            # Snout
            pygame.draw.circle(self.image, (200, 100, 100, 200), (PIG_SIZE//2, PIG_SIZE//2 - PIG_SIZE//4), PIG_SIZE//8)
            # Ears
            pygame.draw.circle(self.image, (200, 100, 100, 200), (PIG_SIZE//4, PIG_SIZE//4), PIG_SIZE//6)
            pygame.draw.circle(self.image, (200, 100, 100, 200), (3*PIG_SIZE//4, PIG_SIZE//4), PIG_SIZE//6)
        
        self.x = WINDOW_WIDTH // 4
        self.y = WINDOW_HEIGHT // 2
        self.speed = 5
        self.width = PIG_SIZE
        self.height = PIG_SIZE
        
    def move(self, direction):
        if direction == 'up':
            self.y -= self.speed
        elif direction == 'down':
            self.y += self.speed
        
        # Keep player within bounds
        self.y = max(0, min(self.y, WINDOW_HEIGHT - self.height))
    
    def draw(self):
        try:
            screen.blit(self.image, (self.x, self.y))
        except Exception as e:
            print(f"Error drawing player: {str(e)}")
            # Fallback to drawing a simple rectangle if blitting fails
            pygame.draw.rect(screen, (200, 100, 100, 200), (self.x, self.y, self.width, self.height))

class BirdFlock:
    def __init__(self):
        self.x = WINDOW_WIDTH
        self.y = random.randint(0, WINDOW_HEIGHT - BIRD_HEIGHT - BIRD_GAP)
        self.speed = 5
        self.birds = []
        
        print(f"\n=== Creating new BirdFlock at x={self.x}, y={self.y} ===")
        print(f"Number of bird images loaded: {len(BIRD_IMAGES)}")
        
        # Create a random number of birds in the flock (3-5 birds)
        num_birds = random.randint(3, 5)
        print(f"Creating {num_birds} birds in this flock")
        
        for i in range(num_birds):
            # Create birds with slightly different positions and sizes
            bird_x = self.x + i * (BIRD_WIDTH // num_birds)
            bird_y = self.y + random.randint(-20, 20)
            bird_size = BIRD_SIZE + random.randint(-5, 5)
            
            if BIRD_IMAGES:
                bird_image = pygame.transform.scale(random.choice(BIRD_IMAGES), (bird_size, bird_size))
                print(f"Bird {i+1}: Using image from BIRD_IMAGES")
            else:
                bird_surface = pygame.Surface((bird_size, bird_size), pygame.SRCALPHA)
                pygame.draw.polygon(bird_surface, (255, 215, 0), [(0, bird_size//2), (bird_size, 0), (bird_size, bird_size)])
                pygame.draw.circle(bird_surface, (0, 0, 0), (bird_size//4, bird_size//4), 2)  # Eye
                bird_image = bird_surface
                print(f"Bird {i+1}: Using default triangle shape")
            
            self.birds.append({
                'x': bird_x,
                'y': bird_y,
                'size': bird_size,
                'image': bird_image
            })
            
        # Randomly add a lucky block
        if random.random() < LUCKY_BLOCK_CHANCE:
            self.lucky_block = LuckyBlock(
                self.x + BIRD_WIDTH + 50,  # Position it after the flock
                random.randint(0, WINDOW_HEIGHT - LUCKY_BLOCK_SIZE)
            )
        else:
            self.lucky_block = None
    
    def move(self):
        self.x -= self.speed
        if self.lucky_block:
            self.lucky_block.move()
        
        # Update bird positions
        for bird in self.birds:
            bird['x'] -= self.speed
            # Add slight up/down movement to make birds look like they're flying
            bird['y'] += random.randint(-2, 2)
            bird['y'] = max(0, min(bird['y'], WINDOW_HEIGHT - bird['size']))
    
    def draw(self):
        # Draw each bird in the flock
        for bird in self.birds:
            screen.blit(bird['image'], (bird['x'], bird['y']))
        # Draw lucky block if it exists
        if self.lucky_block:
            self.lucky_block.draw()
    
    def off_screen(self):
        return self.x + BIRD_WIDTH < 0
    
    def check_lucky_block_collision(self, player):
        if not self.lucky_block:
            return False
            
        return (player.x < self.lucky_block.x + self.lucky_block.width and 
                player.x + player.width > self.lucky_block.x and 
                player.y < self.lucky_block.y + self.lucky_block.height and 
                player.y + player.height > self.lucky_block.y)
    
    def check_collision(self, player):
        # Check collision with each bird in the flock
        for bird in self.birds:
            if (player.x < bird['x'] + bird['size'] and 
                player.x + player.width > bird['x'] and 
                player.y < bird['y'] + bird['size'] and 
                player.y + player.height > bird['y']):
                return True
        return False

def main():
    player = Player()
    bird_flocks = []
    score = 0
    game_over = False
    background = Background()
    
    # Create first bird flock
    bird_flocks.append(BirdFlock())
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    # Restart game
                    player = Player()
                    bird_flocks = [BirdFlock()]
                    score = 0
                    game_over = False
                    background = Background()  # Reset background

        if not game_over:
            # Handle player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player.move('up')
            if keys[pygame.K_DOWN]:
                player.move('down')
            
            # Update background
            background.move()
            
            # Update bird flocks
            for flock in bird_flocks:
                flock.move()
                
                # Check collision with birds
                if flock.check_collision(player):
                    game_over = True
                
                # Check collision with lucky blocks
                if flock.check_lucky_block_collision(player):
                    score += LUCKY_BLOCK_POINTS
                    flock.lucky_block = None  # Remove the lucky block
            
            # Remove off-screen bird flocks
            bird_flocks = [f for f in bird_flocks if not f.off_screen()]
            
            # Add new bird flock if needed
            if not bird_flocks or bird_flocks[-1].x < WINDOW_WIDTH - 300:
                bird_flocks.append(BirdFlock())
                score += 1
            
            # Draw everything
            background.draw()
            player.draw()
            for flock in bird_flocks:
                flock.draw()
            
            # Draw score
            font = pygame.font.Font(None, 36)
            score_text = font.render(f'Score: {score}', True, BLACK)
            screen.blit(score_text, (10, 10))
            
            if game_over:
                game_over_text = font.render('Game Over! Press SPACE to restart', True, BLACK)
                screen.blit(game_over_text, (WINDOW_WIDTH//2 - 150, WINDOW_HEIGHT//2))
            
            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    main()
