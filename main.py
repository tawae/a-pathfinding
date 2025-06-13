import pygame 
from algorithm import a_star

pygame.font.init()
# Kich thuoc cua cua so game
WIDTH = 600
ROWS = 50

# Dinh nghia cac mau su dung
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
TURQUOISE = (64, 224, 208)
PURPLE = (128, 0, 128)

# Tao cua so game
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Pathfinding")

class Spot:
    # Khoi tao mot o trong grid
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # Tra ve vi tri cua o
    def get_pos(self):
        return self.row, self.col

    # Cac ham kiem tra trang thai cua o
    def is_closed(self): return self.color == RED
    def is_open(self): return self.color == GREEN
    def is_barrier(self): return self.color == BLACK
    def is_start(self): return self.color == ORANGE
    def is_end(self): return self.color == TURQUOISE

    # Cac ham thay doi trang thai cua o
    def reset(self): self.color = WHITE
    def make_start(self): self.color = ORANGE
    def make_closed(self): self.color = RED
    def make_open(self): self.color = GREEN
    def make_barrier(self): self.color = BLACK
    def make_end(self): self.color = TURQUOISE
    def make_path(self): self.color = PURPLE

    # Ve o len man hinh
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Cap nhat cac o hang xom khong bi chan
    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    # Ghi de operator < (khong so sanh Spot theo gia tri)
    def __lt__(self, other): return False

# Tao grid 2D gom cac Spot
def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([Spot(i, j, gap, rows) for j in range(rows)])
    return grid

# Ve duong ke luoi
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Ve tat ca Spot trong grid
def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

# Chuyen toa do chuot ve chi so row/col
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    return y // gap, x // gap

def show_message(win, width, message):
    font = pygame.font.SysFont('Arial', 28, bold=True)
    text = font.render(message, True, (255, 0, 0))

    # Kích thước hộp thông báo
    box_width, box_height = 400, 100
    box_x = (width - box_width) // 2
    box_y = (width - box_height) // 2

    # Vẽ nền hộp và viền
    pygame.draw.rect(win, (255, 255, 255), (box_x, box_y, box_width, box_height))  # nền trắng
    pygame.draw.rect(win, (0, 0, 0), (box_x, box_y, box_width, box_height), 3)     # viền đen

    # Hiển thị chữ vào giữa hộp
    text_rect = text.get_rect(center=(width // 2, width // 2))
    win.blit(text, text_rect)

    pygame.display.update()
    pygame.time.delay(3000)

# Ham main chay chuong trinh
def main(win, width):
    grid = make_grid(ROWS, width)
    start = end = None
    run = True
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # Click chuot trai
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != start and spot != end:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # Click chuot phai
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start: start = None
                elif spot == end: end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    # Cap nhat cac neighbor truoc khi chay A*
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    # Goi thuat toan A*
                    found_path = a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    if found_path:
                        show_message(win, width, "Tìm thấy đường đi!")
                    else:
                        show_message(win, width, "Không có đường đi!")

                if event.key == pygame.K_c:
                    # Reset grid
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

if __name__ == "__main__":
    main(WIN, WIDTH)
