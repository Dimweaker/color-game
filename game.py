import pygame
import player


class Color_Game:
    def __init__(self, player1, player2):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 640))
        self.clock = pygame.time.Clock()
        self.map = [[0 for _ in range(10)] for _ in range(10)]
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1
        self.waiting_player = self.player2
        self.players = {1: self.player1, 2: self.player2}
        self.nums = {self.player1: 1, self.player2: 2}
        self.draws = {"draw_up": (0, -1), "draw_down": (0, 1), "draw_left": (-1, 0), "draw_right": (1, 0)}
        self.reset()

    def reset(self):
        self.map = [[0 for _ in range(10)] for _ in range(10)]
        self.player1.x = 0
        self.player1.y = 0
        self.player2.x = 9
        self.player2.y = 9
        # 画一个10x10的格子
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 640, 640))
        for i in range(10):
            for j in range(10):
                pygame.draw.rect(self.screen, (0, 0, 0), (i * 64, j * 64, 64, 64), 1)
        # 画两个玩家
        self.screen.blit(self.player1.img,
                         self.index_to_location(self.player1.x, self.player1.y, self.player1.image_size))
        self.screen.blit(self.player2.img,
                         self.index_to_location(self.player2.x, self.player2.y, self.player2.image_size))

    def draw_player(self, player):
        self.screen.blit(player.img, self.index_to_location(player.x, player.y, player.image_size))

    def draw_block(self, x, y):
        pygame.draw.rect(self.screen, self.current_player.color, (x * 64, y * 64, 64, 64))

    def draw_stone(self, x, y):
        pygame.draw.rect(self.screen, (0, 0, 0), (x * 64, y * 64, 64, 64))

    def judge(self, x, y):
        if (x, y) == (self.current_player.x, self.current_player.y):
            return False, None
        if self.map[x][y] == 3:
            return False, None
        if self.map[x][y] == self.nums[self.current_player]:
            return (True, "move") if self.find(x, y) else (False, None)

        else:
            if self.current_player.x != x and self.current_player.y != y:
                return False, None
            elif abs(self.current_player.x + self.current_player.y - x - y) > 4:
                return False, None
            elif self.current_player.x == x:
                if self.current_player.y > y:
                    if self.map[x][self.current_player.y - 1] != 3:
                        return True, "draw_up"
                elif self.current_player.y < y:
                    if self.map[x][self.current_player.y + 1] != 3:
                        return True, "draw_down"
            elif self.current_player.y == y:
                if self.current_player.x > x:
                    if self.map[self.current_player.x - 1][y] != 3:
                        return True, "draw_left"
                elif self.current_player.x < x:
                    if self.map[self.current_player.x + 1][y] != 3:
                        return True, "draw_right"
        return False, None

    def is_finished(self):
        sides = [(x, y) for (x, y) in [(self.current_player.x, self.current_player.y - 1),
                                       (self.current_player.x, self.current_player.y + 1),
                                       (self.current_player.x - 1, self.current_player.y),
                                       (self.current_player.x + 1, self.current_player.y)] if
                 0 <= x < 10 and 0 <= y < 10]
        return [self.map[x][y] == 3 for (x, y) in sides].count(True) == len(sides) or self.current_player.alive is False

    def move(self, x, y):
        self.draw_block(self.current_player.x, self.current_player.y)
        self.map[self.current_player.x][self.current_player.y] = self.nums[self.current_player]
        self.map[x][y] = -self.nums[self.current_player]
        self.current_player.x = x
        self.current_player.y = y
        self.draw_player(self.current_player)

    def draw(self, x, y, dx, dy):
        if dx == 1:
            for i in range(self.current_player.x + 1, x + 1):
                if self.map[i][y] == self.nums[self.waiting_player]:
                    self.map[i][y] = 3
                    self.draw_stone(i, y)
                    break
                elif self.map[i][y] == -self.nums[self.waiting_player]:
                    self.waiting_player.alive = False
                    self.map[i][y] = -self.nums[self.current_player]
                    break
                else:
                    self.map[i][y] = self.nums[self.current_player]
                    self.draw_block(i, y)

        elif dx == -1:
            for i in range(self.current_player.x - 1, x - 1, -1):
                if self.map[i][y] == self.nums[self.waiting_player]:
                    self.map[i][y] = 3
                    self.draw_stone(i, y)
                    break
                elif self.map[i][y] == -self.nums[self.waiting_player]:
                    self.waiting_player.alive = False
                    self.map[i][y] = -self.nums[self.current_player]
                    break
                else:
                    self.map[i][y] = self.nums[self.current_player]
                    self.draw_block(i, y)
        elif dy == 1:
            for i in range(self.current_player.y + 1, y + 1):
                if self.map[x][i] == self.nums[self.waiting_player]:
                    self.map[x][i] = 3
                    self.draw_stone(x, i)
                    break
                elif self.map[x][i] == -self.nums[self.waiting_player]:
                    self.waiting_player.alive = False
                    self.map[x][i] = -self.nums[self.current_player]
                    break
                else:
                    self.map[x][i] = self.nums[self.current_player]
                    self.draw_block(x, i)
        elif dy == -1:
            for i in range(self.current_player.y - 1, y - 1, -1):
                if self.map[x][i] == self.nums[self.waiting_player]:
                    self.map[x][i] = 3
                    self.draw_stone(x, i)
                    break
                elif self.map[x][i] == -self.nums[self.waiting_player]:
                    self.waiting_player.alive = False
                    self.map[x][i] = -self.nums[self.current_player]
                    break
                else:
                    self.map[x][i] = self.nums[self.current_player]
                    self.draw_block(x, i)

    def find(self, target_x, target_y):
        queue = [(self.current_player.x, self.current_player.y)]
        visited = set()
        while queue:
            x, y = queue.pop(0)
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if nx == target_x and ny == target_y:
                    return True
                if 0 <= nx < 10 and 0 <= ny < 10 and self.map[nx][ny] == self.nums[self.current_player] and (
                        nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))
        return False

    @staticmethod
    def index_to_location(x, y, image_size):
        return x * 64 + (64 - image_size[0]) // 2, y * 64 + (64 - image_size[1]) // 2

    @staticmethod
    def location_to_index(x, y):
        return x // 64, y // 64

    def main_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    x, y = self.location_to_index(x, y)
                    print(x, y)
                    flag, action = self.judge(x, y)
                    print(flag, action)
                    if flag:
                        if action == "move":
                            self.move(x, y)
                        else:
                            self.draw(x, y, *self.draws[action])
                        self.current_player, self.waiting_player = self.waiting_player, self.current_player
                        if self.is_finished():
                            pygame.quit()

            pygame.display.update()
            game.clock.tick(30)


if __name__ == '__main__':
    game = Color_Game(player.Player((255, 0, 0), "img1.png"), player.Player((0, 0, 255), "img2.png"))
    game.reset()
    game.main_game()
