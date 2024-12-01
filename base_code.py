import numpy as np
import random
from itertools import product
import time

class P1:
    def __init__(self, board, available_pieces):
        self.pieces = [(i, j, k, l) for i in range(2) for j in range(2) for k in range(2) for l in range(2)]
        self.board = board
        self.available_pieces = available_pieces

    def select_piece(self):
        # 기본적으로 랜덤 선택을 유지 (변경 가능)
        '''
        1. 휴리스틱 써서 available_pieces에 대해 위험도 예측 -> 상대에게 불리한 조합 선택가능  =>  이건 시간이 너무 많이 걸려서 별로
        2. 자리를 보는 것 : 가로, 세로, 대각선, 2x2를 보면서 그 자리에 남은 특성이 없는 것을 주는 것
        3. 피스를 줄 때 다양하게 줄 수 있도록 함
        '''
        return random.choice(self.available_pieces)

    def place_piece(self, selected_piece):
        best_move = None
        best_score = -float('inf')
        
        for row, col in product(range(4), range(4)):
            if self.board[row][col] == 0:
                self.board[row][col] = self.pieces.index(selected_piece) + 1
                score = self.minimax(depth=3, alpha=-float('inf'), beta=float('inf'), maximizing_player=False)
                self.board[row][col] = 0
                
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

        return best_move

    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal():
            return self.evaluate()

        if maximizing_player:
            max_eval = -float('inf')
            for row, col in product(range(4), range(4)):
                if self.board[row][col] == 0:
                    self.board[row][col] = 1  # 임의의 값으로 시뮬레이션
                    eval = self.minimax(depth - 1, alpha, beta, False)
                    self.board[row][col] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for row, col in product(range(4), range(4)):
                if self.board[row][col] == 0:
                    self.board[row][col] = 1  # 임의의 값으로 시뮬레이션
                    eval = self.minimax(depth - 1, alpha, beta, True)
                    self.board[row][col] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def evaluate(self):
        # 평가 함수 : 수정
        score = 0
        #임의로 하나 설정 각 라인의 동일 특성 개수에 비례하여 점수 부여
        for row in range(4):
            line = [self.board[row][col] for col in range(4) if self.board[row][col] != 0]
            if len(line) == 4:
                score += 10
        return score

    def is_terminal(self):
        # 승리 조건 또는 게임 종료 상태를 확인하는 함수
        return self.check_win() or np.all(self.board)

    def check_win(self):
        # 기존의 승리 조건 확인 로직을 여기에 추가
        return False
