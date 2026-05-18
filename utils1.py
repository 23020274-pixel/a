BOARD_SIZE = 9
WIN_LENGTH = 4

EMPTY = 0
HUMAN = 1
AI = -1


# =========================
# BOARD
# =========================
def create_board():
    return [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def inside(r, c):
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE


def board_full(board):
    for row in board:
        if EMPTY in row:
            return False
    return True


# =========================
# MOVE GENERATOR
# =========================
def get_empty_cells_near(board):

    candidates = set()
    has_piece = False

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):

            if board[r][c] != EMPTY:

                has_piece = True

                for dr in range(-1, 2):
                    for dc in range(-1, 2):

                        nr = r + dr
                        nc = c + dc

                        if inside(nr, nc) and board[nr][nc] == EMPTY:
                            candidates.add((nr, nc))

    if not has_piece:
        return [(BOARD_SIZE // 2, BOARD_SIZE // 2)]

    return list(candidates)


# =========================
# WIN CHECK
# =========================
def check_win(board, player):

    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):

            if board[r][c] != player:
                continue

            for dr, dc in directions:

                count = 0

                for i in range(WIN_LENGTH):

                    nr = r + dr * i
                    nc = c + dc * i

                    if inside(nr, nc) and board[nr][nc] == player:
                        count += 1
                    else:
                        break

                if count >= WIN_LENGTH:
                    return True

    return False


# =========================
# SCORE
# =========================
def create_pattern_dict():

    patterns = {

        (AI, AI, AI, AI): 100000,
        (HUMAN, HUMAN, HUMAN, HUMAN): -100000,

        (EMPTY,AI, AI, AI, EMPTY): 100000,
        (EMPTY, AI, AI, AI, EMPTY): 100000,

        (EMPTY, HUMAN, HUMAN, HUMAN, EMPTY): -100000,
        (EMPTY, HUMAN, HUMAN, HUMAN, EMPTY): -100000,

        (HUMAN,AI, AI, AI, EMPTY): 10000,
        (EMPTY, AI, AI, AI, HUMAN): 10000,

        (AI, HUMAN, HUMAN, HUMAN, EMPTY): -10000,
        (EMPTY, HUMAN, HUMAN, HUMAN, AI): -10000,

        (EMPTY, AI, AI, EMPTY): 10000,
        (EMPTY, HUMAN, HUMAN, EMPTY): -10000,

        (HUMAN, AI, AI, EMPTY): 700,
        (EMPTY, AI, AI, HUMAN): 700,

        (AI, HUMAN, HUMAN, EMPTY): -700,
        (EMPTY, HUMAN, HUMAN, AI): -700,


        (AI, EMPTY, AI, EMPTY): 300,
        (HUMAN, EMPTY, HUMAN, EMPTY): -300,
    }

    return patterns


PATTERN_SCORES = create_pattern_dict()


def evaluate_line(line):

    line = tuple(line)

    if line in PATTERN_SCORES:
        return PATTERN_SCORES[line]

    return 0


def evaluate_board(board):

    if check_win(board, AI):
        return 100000

    if check_win(board, HUMAN):
        return -100000

    score = 0

    directions = [
        (0,1),
        (1,0),
        (1,1),
        (1,-1)
    ]

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):

            for dr, dc in directions:

                # ===================
                # QUÉT 4 Ô
                # ===================

                line4 = []

                for i in range(4):

                    nr = r + dr*i
                    nc = c + dc*i

                    if not inside(nr,nc):
                        break

                    line4.append(
                        board[nr][nc]
                    )

                if len(line4)==4:

                    score += PATTERN_SCORES.get(
                        tuple(line4),
                        0
                    )


                # ===================
                # QUÉT 5 Ô
                # ===================

                line5 = []

                for i in range(5):

                    nr = r + dr*i
                    nc = c + dc*i

                    if not inside(nr,nc):
                        break

                    line5.append(
                        board[nr][nc]
                    )

                if len(line5)==5:

                    score += PATTERN_SCORES.get(
                        tuple(line5),
                        0
                    )

    return score