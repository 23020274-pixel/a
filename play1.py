import pygame
import utils1 as utils
import AI1 as AI

CELL_SIZE = 60
MARGIN = 30

WIDTH = utils.BOARD_SIZE * CELL_SIZE + MARGIN * 2
HEIGHT = WIDTH + 50

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Caro AI")

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

board = utils.create_board()

game_over = False
winner = None


def draw_board():

    screen.fill((245, 222, 179))

    # vẽ bàn cờ
    for i in range(utils.BOARD_SIZE):

        x = MARGIN + i * CELL_SIZE

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (x, MARGIN),
            (x, MARGIN + CELL_SIZE * (utils.BOARD_SIZE - 1)),
            2
        )

    for i in range(utils.BOARD_SIZE):

        y = MARGIN + i * CELL_SIZE

        pygame.draw.line(
            screen,
            (0, 0, 0),
            (MARGIN, y),
            (MARGIN + CELL_SIZE * (utils.BOARD_SIZE - 1), y),
            2
        )

    # vẽ quân cờ
    for r in range(utils.BOARD_SIZE):
        for c in range(utils.BOARD_SIZE):

            # tâm giao điểm
            center_x = MARGIN + c * CELL_SIZE
            center_y = MARGIN + r * CELL_SIZE

            if board[r][c] == utils.HUMAN:

                text = font.render("X", True, (0, 0, 0))

                # căn giữa chữ
                text_rect = text.get_rect(
                    center=(center_x, center_y)
                )

                screen.blit(text, text_rect)

            elif board[r][c] == utils.AI:

                text = font.render("O", True, (0, 0, 0))

                text_rect = text.get_rect(
                    center=(center_x, center_y)
                )

                screen.blit(text, text_rect)

    # thông báo kết quả
    if game_over:

        if winner == utils.HUMAN:
            msg = "PLAYER WIN! Press R"

        elif winner == utils.AI:
            msg = "AI WIN! Press R"

        else:
            msg = "DRAW! Press R"

        text = small_font.render(msg, True, (0, 0, 0))
        screen.blit(text, (20, HEIGHT - 35))


running = True

while running:

    draw_board()
    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # reset game
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                board = utils.create_board()
                game_over = False
                winner = None

        # đánh cờ
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mx, my = pygame.mouse.get_pos()

            col = round((mx - MARGIN) / CELL_SIZE)
            row = round((my - MARGIN) / CELL_SIZE)

            if utils.inside(row, col) and board[row][col] == utils.EMPTY:

                # người chơi
                board[row][col] = utils.HUMAN

                if utils.check_win(board, utils.HUMAN):

                    game_over = True
                    winner = utils.HUMAN
                    continue

                if utils.board_full(board):

                    game_over = True
                    winner = 0
                    continue

                # AI
                AI.ai_move(board)

                if utils.check_win(board, utils.AI):

                    game_over = True
                    winner = utils.AI

                elif utils.board_full(board):

                    game_over = True
                    winner = 0


pygame.quit()