import chess
import chess.svg


class ChessGame:
    def __init__(self) -> None:
        self.board = chess.Board()
        self.white_turn = True

    def make_move(self, move):
        try:
            self.board.push_san(move)
            self.white_turn = not self.white_turn
            return True
        except:
            return False

    def display_board(self):
        return self.board

    def display_legal_moves(self):
        return self.board.legal_moves


game = ChessGame()

print(game.display_board())
print(game.display_legal_moves())
game.make_move("e5")
print(game.display_board())
