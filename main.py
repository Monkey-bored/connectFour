import pygame

map_arr = [[0 for _ in range(7)] for _ in range(6)]

RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH = 700
HEIGHT = 600
LINE_WIDTH = 8
COLUMNS = 7
ROWS = 6
x_graphic_len = WIDTH // COLUMNS
y_graphic_len = HEIGHT // ROWS
x_len = len(map_arr[0])
y_len = len(map_arr)


def draw_map(screen):
    screen.fill(WHITE)

    for i in range(1, y_len):
        pygame.draw.line(screen, BLACK, (0, i * y_graphic_len), (WIDTH, i * y_graphic_len), LINE_WIDTH)
    for i in range(1, x_len):
        pygame.draw.line(screen, BLACK, (i * x_graphic_len, 0), (i * x_graphic_len, HEIGHT), LINE_WIDTH)


def update_map(screen):
    for y in range(y_len):
        for x in range(x_len):
            if map_arr[y][x] > 0:
                pygame.draw.circle(
                    screen,
                    RED if map_arr[y][x] == 1 else BLUE,
                    ((x + 0.5) * x_graphic_len, (y + 0.5) * y_graphic_len),
                    x_graphic_len // 3
                )


def check_win(y, x, currentPlayer):
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
    # Row, Column, Diagonal one way, Diagonal another way

    def check_direction(dy, dx):
        for i in range(1, 4):
            new_y, new_x = y + i * dy, x + i * dx
            if (
                    not (0 <= new_y < len(map_arr) and 0 <= new_x < len(map_arr[0]))
                    or map_arr[new_y][new_x] != currentPlayer
            ):
                return False
        return True

    # Sign each time will be equal to either negative 1 or 1, that way we can check both directions
    # (backwards and forwards)
    for delta_y, delta_x in directions:
        for sign in [-1, 1]:
            if check_direction(delta_y * sign, delta_x * sign):
                return currentPlayer

    return 0


def main():
    player_1 = 1
    player_2 = 2
    currentPlayer = 1
    question = "Where would you like to place? player {} "
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Connect four")
    running = True
    draw_map(screen)
    pygame.display.flip()
    while running:
        turn = True
        event_list = pygame.event.get()
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN and turn:
                column = event.pos[0] // (WIDTH // COLUMNS)
                for i in range(len(map_arr) - 1, -1, -1):
                    if not map_arr[i][column]:
                        turn = False
                        map_arr[i][column] = currentPlayer
                        update_map(screen)
                        pygame.display.flip()
                        winner = check_win(i, column, currentPlayer)
                        if winner:
                            print(winner)
                            running = False
                        currentPlayer = (currentPlayer % 2) + 1
                        break
    print("game over")


if __name__ == "__main__":
    main()
