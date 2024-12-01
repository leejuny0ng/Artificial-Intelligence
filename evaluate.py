    def evaluate(self, board):
        if self.if_win(board):
            print(f"[EVALUATE] Winning board detected.")
            return 1  # 승리하는 상태
        if not np.any(board == -1):  # 빈칸 없음 (무승부)
            print(f"[EVALUATE] Draw board detected.")
            return 0
        
        # 전략적 상태 평가 (가중치 계산)
        score = 0
        for row in range(4):
            score += self.evaluate_line(board[row, :])  # 가로 라인
        for col in range(4):
            score += self.evaluate_line(board[:, col])  # 세로 라인
        score += self.evaluate_line(np.diag(board))    # 주대각선
        score += self.evaluate_line(np.diag(np.fliplr(board)))  # 부대각선

        # 중앙 2x2 영역 추가 점수
        center_positions = [(1, 1), (1, 2), (2, 1), (2, 2)]
        center_score = 1
        for row, col in center_positions:
            if board[row, col] != -1:  # 중앙에 놓인 말이 있으면 점수 추가
                score += center_score
        score += center_score

        print(f"[EVALUATE] Board ({(row, col)}) score: {score} (includes center score: {center_score})")
        return score

    def evaluate_line(self, line):
        # 라인에서 남은 빈칸의 개수와 비슷한 특징이 몇 개 포함되었는지 평가
        if -1 in line:  # 비어 있는 칸이 있는 경우
            traits = [set(p & (1 << i) for p in line if p != -1) for i in range(4)]
            return sum(len(trait) == 1 for trait in traits)  # 같은 특징이 있는 경우 점수 추가
        return 0  # 빈칸이 없으면 해당 라인은 점수 없음


    def if_win(self, board: np.ndarray) -> bool:
        for i in range(4):
            if self.def_win(board[i, :]) or self.def_win(board[:, i]):
                return True
        if self.def_win(np.diag(board)) or self.def_win(np.diag(np.fliplr(board))):
            return True

        for i in range(3):
            for j in range(3):
                subgrid = board[i:i + 2, j:j + 2]
                if self.def_win(subgrid.ravel()):
                    return True
        return False

    def def_win(self, line: np.ndarray) -> bool:
        if -1 in line:
            return False
        for i in range(4):
            if len(set(x & (1 << i) for x in line)) == 1:
                return True
        return False
