import math
import utils1 as utils
import time  
DEPTH = 6

# Biến cấu hình toàn cục điều khiển trạng thái cắt tỉa, được thay đổi từ file play1.py
USE_ALPHA_BETA = True  

# BIẾN TOÀN CỤC ĐỂ ĐẾM SỐ TRẠNG THÁI ĐÃ DUYỆT
state_count = 0


def minimax(board, depth, alpha, beta, maximizing, current_score=None):
    global state_count
    state_count += 1  # Tăng số trạng thái mỗi khi hàm minimax được gọi

    if current_score is None:
        score = utils.evaluate_board(board)
    else:
        score = current_score

    if depth == 0 or abs(score) >= 900000 or utils.board_full(board):
        return score, None

    moves = utils.get_empty_cells_near(board)

    if maximizing:
        best_score = -math.inf
        best_move = None

        scored_moves = []
        for r, c in moves:
            board[r][c] = utils.AI
            if utils.check_win(board, utils.AI):
                board[r][c] = utils.EMPTY
                return 1000000, (r, c)
            board[r][c] = utils.EMPTY

            board[r][c] = utils.HUMAN
            if utils.check_win(board, utils.HUMAN):
                board[r][c] = utils.EMPTY
                urgency = 10000000
            else:
                board[r][c] = utils.EMPTY
                ai_score = utils.evaluate_move(board, r, c, utils.AI, score)
                human_score = utils.evaluate_move(board, r, c, utils.HUMAN, score)
                urgency = ai_score - human_score

            scored_moves.append((urgency, (r, c)))
        
        scored_moves.sort(key=lambda x: x[0], reverse=True)

        for _, (r, c) in scored_moves:
            next_score = utils.evaluate_move(board, r, c, utils.AI, score)
            board[r][c] = utils.AI

            eval_score, _ = minimax(board, depth - 1, alpha, beta, False, next_score)

            board[r][c] = utils.EMPTY

            if eval_score > best_score:
                best_score = eval_score
                best_move = (r, c)

            alpha = max(alpha, best_score)
            
            # KIỂM TRA ĐIỀU KIỆN CẮT TỈA (Chỉ thực hiện nếu USE_ALPHA_BETA = True)
            if USE_ALPHA_BETA and beta <= alpha:
                break

        return best_score, best_move

    else:
        best_score = math.inf
        best_move = None

        scored_moves = []
        for r, c in moves:
            board[r][c] = utils.HUMAN
            if utils.check_win(board, utils.HUMAN):
                board[r][c] = utils.EMPTY
                return -1000000, (r, c)
            board[r][c] = utils.EMPTY

            board[r][c] = utils.AI
            if utils.check_win(board, utils.AI):
                board[r][c] = utils.EMPTY
                urgency = -10000000
            else:
                board[r][c] = utils.EMPTY
                human_score = utils.evaluate_move(board, r, c, utils.HUMAN, score)
                ai_score = utils.evaluate_move(board, r, c, utils.AI, score)
                urgency = human_score - ai_score

            scored_moves.append((urgency, (r, c)))
        
        scored_moves.sort(key=lambda x: x[0], reverse=False)

        for _, (r, c) in scored_moves:
            next_score = utils.evaluate_move(board, r, c, utils.HUMAN, score)
            board[r][c] = utils.HUMAN

            eval_score, _ = minimax(board, depth - 1, alpha, beta, True, next_score)

            board[r][c] = utils.EMPTY

            if eval_score < best_score:
                best_score = eval_score
                best_move = (r, c)

            beta = min(beta, best_score)
            
            # KIỂM TRA ĐIỀU KIỆN CẮT TỈA (Chỉ thực hiện nếu USE_ALPHA_BETA = True)
            if USE_ALPHA_BETA and beta <= alpha:
                break

        return best_score, best_move


def ai_move(board):
    global state_count
    state_count = 0  # Reset bộ đếm trạng thái trước khi AI tính toán
    
    # BẮT ĐẦU ĐO THỜI GIAN
    start_time = time.time()
    
    _, move = minimax(board, DEPTH, -math.inf, math.inf, True)
    
    # KẾT THÚC ĐO THỜI GIAN
    end_time = time.time()
    execution_time = end_time - start_time
    
    # In kết quả chi tiết ra Terminal
    algo_name = "Minimax + Alpha-Beta" if USE_ALPHA_BETA else "Minimax Thuần"
    print(f"\n=== LƯỢT ĐI CỦA AI ===")
    print(f"[*] Thuật toán sử dụng : {algo_name}")
    print(f"[*] Độ sâu cấu hình   : DEPTH = {DEPTH}")
    print(f"[*] Số trạng thái duyệt: {state_count} trạng thái")
    print(f"[*] Thời gian xử lý    : {execution_time:.4f} giây")
    print(f"=======================")
    
    if move:
        board[move[0]][move[1]] = utils.AI