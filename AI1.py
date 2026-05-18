import math
import copy
import utils1 as utils


# =========================
# CHẤM ĐIỂM BÀN CỜ
# =========================
def evaluate_board(board_state):

    if utils.check_win(board_state, utils.AI):
        return 100000

    if utils.check_win(board_state, utils.HUMAN):
        return -100000

    score = 0

    directions = [
        (0, 1),
        (1, 0),
        (1, 1),
        (1, -1)
    ]

    for r in range(utils.BOARD_SIZE):
        for c in range(utils.BOARD_SIZE):

            for dr, dc in directions:

                line = []

                for i in range(4):

                    nr = r + dr * i
                    nc = c + dc * i

                    if not utils.inside(nr, nc):
                        break

                    line.append(board_state[nr][nc])

                if len(line) != 4:
                    continue

                ai_count = line.count(utils.AI)
                human_count = line.count(utils.HUMAN)
                empty_count = line.count(utils.EMPTY)

                # cả 2 bên cùng xuất hiện
                if ai_count > 0 and human_count > 0:
                    continue

                # HUMAN threat
                if human_count == 3 and empty_count == 1:
                    score -= 50000

                elif human_count == 2 and empty_count == 2:
                    score -= 5000

                # AI attack
                if ai_count == 3 and empty_count == 1:
                    score += 10000

                elif ai_count == 2 and empty_count == 2:
                    score += 1000

    return score


# =========================
# SẮP XẾP NƯỚC ĐI
# giống childNodes của Gomoku
# =========================
def sort_moves(board_state):

    moves = utils.get_empty_cells_near(board_state)

    scored_moves = []

    for r, c in moves:

        board_state[r][c] = utils.AI
        score = evaluate_board(board_state)
        board_state[r][c] = utils.EMPTY

        scored_moves.append((score, (r, c)))

    scored_moves.sort(reverse=True)

    return [move for score, move in scored_moves]


# =========================
# MINIMAX + ALPHA BETA
# =========================
def minimax(board_state, depth, alpha, beta, maximizing):

    score = evaluate_board(board_state)

    if depth == 0 \
            or abs(score) >= 100000 \
            or utils.board_full(board_state):

        return score, None

    # thay vì get_empty_cells_near
    moves = sort_moves(board_state)

    if maximizing:

        best_score = -math.inf
        best_move = None

        for r, c in moves:

            board_state[r][c] = utils.AI

            eval_score, _ = minimax(
                board_state,
                depth - 1,
                alpha,
                beta,
                False
            )

            board_state[r][c] = utils.EMPTY

            if eval_score > best_score:

                best_score = eval_score
                best_move = (r, c)

            alpha = max(alpha, best_score)

            # alpha-beta pruning
            if beta <= alpha:
                break

        return best_score, best_move

    else:

        best_score = math.inf
        best_move = None

        for r, c in moves:

            board_state[r][c] = utils.HUMAN

            eval_score, _ = minimax(
                board_state,
                depth - 1,
                alpha,
                beta,
                True
            )

            board_state[r][c] = utils.EMPTY

            if eval_score < best_score:

                best_score = eval_score
                best_move = (r, c)

            beta = min(beta, best_score)

            # alpha-beta pruning
            if beta <= alpha:
                break

        return best_score, best_move


# =========================
# AI MOVE
# =========================
def ai_move(board_state, depth):

    _, move = minimax(
        board_state,
        depth,
        -math.inf,
        math.inf,
        True
    )

    return move