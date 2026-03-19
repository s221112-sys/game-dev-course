import pygame
import sys
import os

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

ABILITY_BOOST = 0
ABILITY_SKILL = 1
ABILITY_ENLARGE = 2
ABILITY_SHRINK_BALL = 3

ABILITIES = [
    ("Boost", "Speed up paddle"),
    ("Skill", "Slow ball"),
    ("Enlarge", "Enlarge paddle"),
    ("Shrink Ball", "Shrink ball")
]

HIGHSCORE_FILE = "highscores.txt"

def load_highscores():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            scores = [float(line.strip()) for line in f if line.strip()]
        scores.sort()
        return scores[:10]  # Top 10 fastest times
    return []

def save_highscores(scores):
    with open(HIGHSCORE_FILE, "w") as f:
        for score in scores:
            f.write(f"{score}\n")

class PaddleVertical:
    def __init__(self, x, y, ability):
        self.rect = pygame.Rect(x, y, 20, 90)  # Increased width to 20
        self.speed = 6
        self.boost_speed = 12
        self.boost_duration = 0
        self.boost_cooldown = 0
        self.skill_duration = 0
        self.skill_cooldown = 0
        self.enlarge_duration = 0
        self.enlarge_cooldown = 0
        self.shrink_cooldown = 0
        self.ability = ability
        self.previous_height = 90

    def draw(self, screen):
        # Adjust height for enlarge
        if self.enlarge_duration > 0 and self.previous_height == 90:
            self.rect.y -= 15
            self.previous_height = 120
        elif self.enlarge_duration == 0 and self.previous_height == 120:
            self.rect.y += 15
            self.previous_height = 90
        self.rect.height = self.previous_height
        pygame.draw.rect(screen, WHITE, self.rect)

    def move_up(self):
        current_speed = self.boost_speed if self.boost_duration > 0 else self.speed
        self.rect.y = max(0, self.rect.y - current_speed)

    def move_down(self):
        current_speed = self.boost_speed if self.boost_duration > 0 else self.speed
        self.rect.y = min(HEIGHT - self.rect.height, self.rect.y + current_speed)

    def update_boost(self):
        if self.boost_duration > 0:
            self.boost_duration -= 1
        if self.boost_cooldown > 0:
            self.boost_cooldown -= 1

    def activate_boost(self):
        if self.boost_cooldown == 0:
            self.boost_duration = 30  # Boost for 30 frames (0.5 seconds at 60 FPS)
            self.boost_cooldown = 180  # Cooldown for 3 seconds

    def activate_skill(self):
        if self.skill_cooldown == 0:
            self.skill_duration = 60  # Skill for 60 frames (1 second at 60 FPS)
            self.skill_cooldown = 300  # Cooldown for 5 seconds

    def update_skill(self):
        if self.skill_duration > 0:
            self.skill_duration -= 1
        if self.skill_cooldown > 0:
            self.skill_cooldown -= 1

    def activate_enlarge(self):
        if self.enlarge_cooldown == 0:
            self.enlarge_duration = 120  # Enlarge for 120 frames (2 seconds at 60 FPS)
            self.enlarge_cooldown = 600  # Cooldown for 10 seconds

    def update_enlarge(self):
        if self.enlarge_duration > 0:
            self.enlarge_duration -= 1
        if self.enlarge_cooldown > 0:
            self.enlarge_cooldown -= 1

    def activate_shrink_ball(self, ball):
        if self.shrink_cooldown == 0:
            ball.shrink_duration = 60  # Shrink for 60 frames (1 second at 60 FPS)
            self.shrink_cooldown = 300  # Cooldown for 5 seconds

    def update_shrink_ball(self):
        if self.shrink_cooldown > 0:
            self.shrink_cooldown -= 1

    def activate_ability(self, ball):
        if self.ability == ABILITY_BOOST:
            self.activate_boost()
        elif self.ability == ABILITY_SKILL:
            self.activate_skill()
        elif self.ability == ABILITY_ENLARGE:
            self.activate_enlarge()
        elif self.ability == ABILITY_SHRINK_BALL:
            self.activate_shrink_ball(ball)

    def update_ability(self):
        if self.ability == ABILITY_BOOST:
            self.update_boost()
        elif self.ability == ABILITY_SKILL:
            self.update_skill()
        elif self.ability == ABILITY_ENLARGE:
            self.update_enlarge()
        elif self.ability == ABILITY_SHRINK_BALL:
            self.update_shrink_ball()

    def get_ability_cooldown(self):
        if self.ability == ABILITY_BOOST:
            return max(0, self.boost_cooldown // FPS)
        elif self.ability == ABILITY_SKILL:
            return max(0, self.skill_cooldown // FPS)
        elif self.ability == ABILITY_ENLARGE:
            return max(0, self.enlarge_cooldown // FPS)
        elif self.ability == ABILITY_SHRINK_BALL:
            return max(0, self.shrink_cooldown // FPS)
        return 0

class PaddleHorizontal:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 6

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move_left(self):
        self.rect.x = max(0, self.rect.x - self.speed)

    def move_right(self):
        self.rect.x = min(WIDTH - self.rect.width, self.rect.x + self.speed)

class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)  # Increased size to 20x20
        self.speed_x = 5
        self.speed_y = 5
        self.shrink_duration = 0
        self.previous_size = 20

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

    def update(self, slow_multiplier=1.0):
        self.rect.x += self.speed_x * slow_multiplier
        self.rect.y += self.speed_y * slow_multiplier

        # Adjust size for shrink
        if self.shrink_duration > 0 and self.previous_size == 20:
            self.rect.x += 2.5
            self.rect.y += 2.5
            self.previous_size = 15
        elif self.shrink_duration == 0 and self.previous_size == 15:
            self.rect.x -= 2.5
            self.rect.y -= 2.5
            self.previous_size = 20
        self.rect.width = self.previous_size
        self.rect.height = self.previous_size

        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = 5 if pygame.time.get_ticks() % 2 else -5
        self.speed_y = 5
        self.shrink_duration = 0
        self.previous_size = 20
        self.rect = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)

def choose_ability(player_num):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)
    
    selected = 0
    while True:
        screen.fill(BLACK)
        title = font.render(f"Player {player_num}: Choose Ability", True, WHITE)
        screen.blit(title, (WIDTH // 2 - 150, 100))
        
        for i, (name, desc) in enumerate(ABILITIES):
            color = WHITE if i == selected else (100, 100, 100)
            text = font.render(f"{name}: {desc}", True, color)
            screen.blit(text, (WIDTH // 2 - 200, 200 + i * 50))
        
        instructions = small_font.render("Use UP/DOWN to select, SPACE to confirm", True, WHITE)
        screen.blit(instructions, (WIDTH // 2 - 200, 500))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(ABILITIES)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(ABILITIES)
                elif event.key == pygame.K_SPACE:
                    return selected

def choose_abilities(two_player):
    left_ability = choose_ability(1)
    
    if two_player:
        right_ability = choose_ability(2)
    else:
        right_ability = ABILITY_SKILL  # AI defaults to skill
    
    return left_ability, right_ability

def game_loop(two_player, four_player, left_ability, right_ability):
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    left_paddle = PaddleVertical(20, HEIGHT // 2 - 45, left_ability if not four_player else None)
    right_paddle = PaddleVertical(WIDTH - 40, HEIGHT // 2 - 45, right_ability if not four_player else None)
    ball = Ball()

    left_score = 0
    right_score = 0
    top_score = 0
    bottom_score = 0
    WIN_SCORE = 5
    
    game_start_time = pygame.time.get_ticks()
    last_speed_increase = game_start_time

    if four_player:
        top_paddle = PaddleHorizontal(WIDTH // 2 - 50, 0, 100, 20)
        bottom_paddle = PaddleHorizontal(WIDTH // 2 - 50, HEIGHT - 20, 100, 20)

    while True:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Increase ball speed by x1.1 every 10 seconds
        if current_time - last_speed_increase >= 10000:
            ball.speed_x *= 1.1
            ball.speed_y *= 1.1
            last_speed_increase = current_time

        keys = pygame.key.get_pressed()
        
        # Left player controls
        if keys[pygame.K_w]:
            left_paddle.move_up()
        if keys[pygame.K_s]:
            left_paddle.move_down()
        if not four_player and keys[pygame.K_d]:
            left_paddle.activate_ability(ball)
        
        # Right player controls
        if two_player or four_player:
            if keys[pygame.K_UP]:
                right_paddle.move_up()
            if keys[pygame.K_DOWN]:
                right_paddle.move_down()
            if not four_player and keys[pygame.K_LEFT]:
                right_paddle.activate_ability(ball)
        else:
            # AI logic
            if ball.rect.centery < right_paddle.rect.centery - 50:
                right_paddle.move_up()
            elif ball.rect.centery > right_paddle.rect.centery + 50:
                right_paddle.move_down()
        
        # 4-player controls
        if four_player:
            if keys[pygame.K_q]:
                top_paddle.move_left()
            if keys[pygame.K_e]:
                top_paddle.move_right()
            if keys[pygame.K_z]:
                bottom_paddle.move_left()
            if keys[pygame.K_c]:
                bottom_paddle.move_right()
        
        # Update abilities (only if not 4-player)
        if not four_player:
            left_paddle.update_ability()
            right_paddle.update_ability()

        # Determine slow multiplier
        slow_multiplier = 0.5 if (not four_player and ((left_paddle.ability == ABILITY_SKILL and left_paddle.skill_duration > 0) or (right_paddle.ability == ABILITY_SKILL and right_paddle.skill_duration > 0))) else 1.0

        ball.update(slow_multiplier)

        if ball.rect.colliderect(left_paddle.rect) and ball.speed_x < 0:
            ball.speed_x *= -1
        if ball.rect.colliderect(right_paddle.rect) and ball.speed_x > 0:
            ball.speed_x *= -1
        if four_player:
            if ball.rect.colliderect(top_paddle.rect) and ball.speed_y < 0:
                ball.speed_y *= -1
            if ball.rect.colliderect(bottom_paddle.rect) and ball.speed_y > 0:
                ball.speed_y *= -1

        if ball.rect.left < 0:
            right_score += 1
            ball.reset()
        if ball.rect.right > WIDTH:
            left_score += 1
            ball.reset()
        if four_player:
            if ball.rect.top < 0:
                bottom_score += 1
                ball.reset()
            if ball.rect.bottom > HEIGHT:
                top_score += 1
                ball.reset()

        screen.fill(BLACK)
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        if four_player:
            top_paddle.draw(screen)
            bottom_paddle.draw(screen)
        ball.draw(screen)

        if four_player:
            score_text = font.render(f"L:{left_score} R:{right_score} T:{top_score} B:{bottom_score}", True, WHITE)
        else:
            score_text = font.render(f"{left_score}  {right_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - 80 if not four_player else WIDTH // 2 - 150, 20))

        # Display ability cooldowns (only if not 4-player)
        if not four_player:
            left_cd_sec = left_paddle.get_ability_cooldown()
            right_cd_sec = right_paddle.get_ability_cooldown()
            left_cd_text = small_font.render(f"Left CD: {left_cd_sec}s (D)", True, WHITE)
            if two_player:
                right_cd_text = small_font.render(f"Right CD: {right_cd_sec}s (LEFT)", True, WHITE)
            else:
                right_cd_text = small_font.render(f"Right CD: {right_cd_sec}s", True, WHITE)
            screen.blit(left_cd_text, (20, HEIGHT - 50))
            screen.blit(right_cd_text, (WIDTH - 300, HEIGHT - 50))

        # Check for winner
        if (not four_player and (left_score >= WIN_SCORE or right_score >= WIN_SCORE)) or (four_player and (left_score >= WIN_SCORE or right_score >= WIN_SCORE or top_score >= WIN_SCORE or bottom_score >= WIN_SCORE)):
            game_time = (current_time - game_start_time) / 1000.0  # Time in seconds
            highscores = load_highscores()
            highscores.append(game_time)
            highscores.sort()
            highscores = highscores[:10]
            save_highscores(highscores)
            
            if four_player:
                winner = "Left" if left_score >= WIN_SCORE else "Right" if right_score >= WIN_SCORE else "Top" if top_score >= WIN_SCORE else "Bottom"
            else:
                winner = "Left" if left_score >= WIN_SCORE else "Right"
            winner_text = small_font.render(f"{winner} Player Wins in {game_time:.2f}s! Press SPACE to return to menu", True, WHITE)
            screen.blit(winner_text, (WIDTH // 2 - 300, HEIGHT // 2))
            pygame.display.flip()
            
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        return

        pygame.display.flip()

def show_highscores():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.Font(None, 50)
    small_font = pygame.font.Font(None, 36)
    
    highscores = load_highscores()
    
    while True:
        screen.fill(BLACK)
        title = font.render("Top 10 Records (Fastest Times)", True, WHITE)
        screen.blit(title, (WIDTH // 2 - 250, 50))
        
        for i, score in enumerate(highscores):
            text = small_font.render(f"{i+1}. {score:.2f}s", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 100, 150 + i * 40))
        
        back_text = small_font.render("Press SPACE to return to menu", True, WHITE)
        screen.blit(back_text, (WIDTH // 2 - 200, 550))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong - Menu")
    font = pygame.font.Font(None, 50)

    while True:
        screen.fill(BLACK)
        title = font.render("PONG", True, WHITE)
        one_player = font.render("Press 1 for 1 Player", True, WHITE)
        two_player = font.render("Press 2 for 2 Players", True, WHITE)
        four_player = font.render("Press 4 for 4 Players", True, WHITE)
        highscores = font.render("Press H for High Scores", True, WHITE)

        screen.blit(title, (WIDTH // 2 - 80, 100))
        screen.blit(one_player, (WIDTH // 2 - 200, 250))
        screen.blit(two_player, (WIDTH // 2 - 200, 350))
        screen.blit(four_player, (WIDTH // 2 - 200, 450))
        screen.blit(highscores, (WIDTH // 2 - 200, 550))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    left_abil, right_abil = choose_abilities(False)
                    game_loop(False, False, left_abil, right_abil)
                if event.key == pygame.K_2:
                    left_abil, right_abil = choose_abilities(True)
                    game_loop(True, False, left_abil, right_abil)
                if event.key == pygame.K_4:
                    game_loop(True, True, None, None)
                if event.key == pygame.K_h:
                    show_highscores()

main_menu()