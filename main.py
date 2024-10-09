import pygame
import os
import random
import time

# Khởi tạo Pygame
pygame.init()
pygame.mixer.init()

# Kích thước cửa sổ game
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bomberman")

# Đường dẫn tới thư mục assets
ASSETS_DIR = os.path.join(os.path.dirname(__file__), 'Assets')

# Tải ảnh
PLAYER_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'images', 'player.png'))
WALL_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'images', 'wall.png'))
CRATE_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'images', 'crate.png'))
BOMB_IMG = pygame.image.load(os.path.join(ASSETS_DIR, 'images', 'bomb.png'))

# Tải các tệp âm thanh
# bomb_place_sound = pygame.mixer.Sound('Sounds/place.wav')
# explosion_sound = pygame.mixer.Sound('Sounds/explosion.wav')

# Kích thước ô và tốc độ
TILE_SIZE = 40
PLAYER_SIZE = TILE_SIZE

# Tạo lớp nhân vật
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pygame.image.load('images/player.png')
        self.speed = 5
        self.bombs = []
        self.is_alive = True

    def move(self, keys):
        if self.is_alive:
            if keys[pygame.K_LEFT]:
                self.x -= self.speed
            if keys[pygame.K_RIGHT]:
                self.x += self.speed
            if keys[pygame.K_UP]:
                self.y -= self.speed
            if keys[pygame.K_DOWN]:
                self.y += self.speed

    def place_bomb(self):
        if self.is_alive:
            # Phát âm thanh khi đặt bom
            bomb_place_sound.play()
            
            bomb = Bomb(self.x, self.y)
            self.bombs.append(bomb)
            return bomb

    def draw(self, window):
        if self.is_alive:
            window.blit(self.image, (self.x, self.y))

    def handle_bomb_explosion(self, bombs):
        # Xử lý bom nổ và cập nhật trạng thái của người chơi
        for bomb in bombs:
            if bomb.exploded:
                # Nếu người chơi đứng gần bom nổ, người chơi bị đánh bại
                if (self.x < bomb.x + bomb.width and
                    self.x + self.width > bomb.x and
                    self.y < bomb.y + bomb.height and
                    self.y + self.height > bomb.y):
                    self.is_alive = False

class Bot:
    def __init__(self, game_map, bot_position, player_position):
        self.game_map = game_map  # Bản đồ game
        self.bot_position = bot_position  # Vị trí của bot
        self.player_position = player_position  # Vị trí của người chơi
        self.bombs = []  # Danh sách các bom trên bản đồ

    def move(self):
        # Tìm đường đến người chơi hoặc power-up
        target_position = self.find_target()
        next_move = self.calculate_next_move(target_position)
        return next_move

    def place_bomb(self):
        # Đặt bom tại vị trí hiện tại của bot
        if self.is_safe_to_place_bomb():
            return "PLACE_BOMB"
        return "MOVE"

    def calculate_next_move(self, target_position):
        # Sử dụng thuật toán A* hoặc tìm đường ngắn nhất để di chuyển
        return a_star(self.bot_position, target_position, self.game_map)

    def find_target(self):
        # Tìm mục tiêu ưu tiên: người chơi, power-ups, hoặc phá vật cản
        if self.is_player_nearby():
            return self.player_position
        else:
            return self.find_closest_powerup_or_breakable_wall()

    def is_safe_to_place_bomb(self):
        # Kiểm tra nếu bot an toàn để đặt bom
        return not self.is_in_blast_radius()

    def is_in_blast_radius(self):
        # Kiểm tra nếu bot đang ở trong phạm vi nổ
        for bomb in self.bombs:
            if bomb.is_within_blast_radius(self.bot_position):
                return True
        return False


# Lớp Tường
class Wall:
    def __init__(self, x, y, destructible=False):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.destructible = destructible  # Biến để xác định tường có thể phá hủy hay không
        if destructible:
            self.image = pygame.transform.scale(CRATE_IMG, (self.width, self.height))
        else:
            self.image = pygame.transform.scale(WALL_IMG, (self.width, self.height))

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))  # Vẽ tường lên màn hình

    def destroy(self):
        # Chỉ có thể phá hủy nếu là tường phá hủy được
        if self.destructible:
            return True
        return False
    
# Lớp thùng
class Crate(Wall):
    def __init__(self, x, y):
        # Gọi tới hàm khởi tạo của Wall nhưng luôn đặt destructible = True
        super().__init__(x, y, destructible=True)
        self.image = pygame.transform.scale(CRATE_IMG, (self.width, self.height))

    def destroy(self):
        # Thùng gỗ bị phá hủy
        self.destroyed = True


# Lớp Bom
class Bomb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.image = pygame.transform.scale(BOMB_IMG, (self.width, self.height))
        self.time_to_explode = 3  # Bom sẽ nổ sau 3 giây
        self.exploded = False
        self.explode_time = time.time() + self.time_to_explode  # Thời gian bom sẽ nổ
        self.explosion_radius = 80  # Bán kính vụ nổ (điều chỉnh theo ý muốn)

    def draw(self, window):
        if not self.exploded:
            window.blit(self.image, (self.x, self.y))  # Vẽ bom lên màn hình

    def update(self):
        # Kiểm tra thời gian nổ
        if time.time() >= self.explode_time:
            self.exploded = True

    def explode(self, walls):
        # Kiểm tra phạm vi vụ nổ và phá hủy tường trong phạm vi đó
        affected_walls = []
        for wall in walls:
            distance = abs(self.x - wall.x) + abs(self.y - wall.y)
            if distance <= self.explosion_radius and wall.destructible:
                affected_walls.append(wall)
        return affected_walls  # Trả về danh sách các tường bị phá hủy