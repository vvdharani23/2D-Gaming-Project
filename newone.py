import pygame
import random
import os

# Initialize
pygame.init()
pygame.mixer.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Animal Fruit Catcher")
clock = pygame.time.Clock()

# Load assets
ASSET_PATH = "C:\\Users\\vignan\\Documents\\Danger\\Assets"
background_img = pygame.image.load(os.path.join(ASSET_PATH, "background.jpg"))
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
animal_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "cute-monkey.png")), (64, 64))
fruit_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "Fruit.png")), (64, 64))
flower_img = pygame.transform.scale(pygame.image.load(os.path.join(ASSET_PATH, "flower.png")), (64, 64))

# Load sounds
background_music = pygame.mixer.Sound("C:\\Users\\vignan\\Documents\\Danger\\Assets\\power-up-sparkle-1-177983.mp3")
fruit_sound = pygame.mixer.Sound("C:\\Users\\vignan\\Documents\\Danger\\Assets\\coin-recieved-230517.mp3")
flower_sound = pygame.mixer.Sound("C:\\Users\\vignan\\Documents\\Danger\\Assets\\ahoah-288047.mp3")

font = pygame.font.SysFont(None, 36)

class FallingObject:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(0, SCREEN_WIDTH - 64)
        self.y = random.randint(-300, -64)
        self.type = random.choice(['fruit', 'flower'])
        self.speed = random.randint(5, 9)

    def update(self, speed_boost=0):
        self.y += self.speed + speed_boost
        if self.y > SCREEN_HEIGHT:
            self.reset()

    def draw(self, surface):
        img = fruit_img if self.type == 'fruit' else flower_img
        surface.blit(img, (self.x, self.y))

    def collide(self, px, py):
        return (
            px < self.x + 64 and
            px + 64 > self.x and
            py < self.y + 64 and
            py + 64 > self.y
        )

class Game:
    def __init__(self):
        self.reset()
        background_music.play(loops=-1, maxtime=0, fade_ms=0)  # Play background music loop

    def reset(self):
        self.player_x = SCREEN_WIDTH // 2 - 32
        self.player_y = SCREEN_HEIGHT - 80
        self.score = 0
        self.lives = 3
        self.speed_boost = 0
        self.objects = [FallingObject() for _ in range(3)]
        self.running = True
        self.game_over = False

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player_x -= 10
        if keys[pygame.K_RIGHT]:
            self.player_x += 10

        # Clamp movement to screen bounds
        self.player_x = max(0, min(SCREEN_WIDTH - 64, self.player_x))

    def update_objects(self):
        self.speed_boost = self.score // 5
        for obj in self.objects:
            obj.update(self.speed_boost)
            if obj.collide(self.player_x, self.player_y):
                if obj.type == 'fruit':
                    self.score += 1
                    fruit_sound.play()  # Play fruit catch sound
                else:
                    self.lives -= 1
                    flower_sound.play()  # Play flower catch sound
                    if self.lives <= 0:
                        self.game_over = True
                obj.reset()

    def draw(self):
        screen.blit(background_img, (0, 0))  # Draw background
        screen.blit(animal_img, (self.player_x, self.player_y))
        for obj in self.objects:
            obj.draw(screen)
        score_text = font.render(f"Score: {self.score}", True, (0, 0, 0))
        lives_text = font.render(f"Lives: {self.lives}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

    def show_game_over(self):
        screen.fill((0, 0, 0))
        game_over_text = font.render("Game Over!", True, (255, 0, 0))
        final_score_text = font.render(f"Final Score: {self.score}", True, (255, 255, 255))
        restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 60))
        screen.blit(final_score_text, (SCREEN_WIDTH//2 - 110, SCREEN_HEIGHT//2))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 + 50))
        pygame.display.update()

    def run(self):
        while self.running:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_q:
                        self.running = False

            if not self.game_over:
                self.handle_input()
                self.update_objects()
                self.draw()
                pygame.display.update()
            else:
                self.show_game_over()

# Start the game
game = Game()
game.run()
pygame.quit()
