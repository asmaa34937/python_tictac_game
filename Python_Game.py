from tkinter import *

class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title("Tic-Tac-Toe (You vs AI)")

        # Game variables
        self.player = "You"
        self.board = [""] * 9
        self.games_played = 0
        self.You_win = 0
        self.ai_wins = 0
        self.Ties = 0

        # Create GUI components
        self.label = Label(self.window, text="Your Turn (You)", font=('Arial', 30, 'bold'))
        self.label.pack(side="top")

        self.restart_btn = Button(self.window, text="Play Again", font=('Arial', 20, 'bold'), bg="orange", fg="white",
                                  activebackground="darkorange", activeforeground="white", relief="raised",
                                  bd=5, command=self.start_new_game)

        self.btns_frame = Frame(self.window)
        self.btns_frame.pack()

        self.game_btns = [[None for _ in range(3)] for _ in range(3)]
        for row in range(3):
            for col in range(3):
                self.game_btns[row][col] = Button(self.btns_frame, text="", font=('Arial', 50, 'bold'), width=4, height=1,
                                                  command=lambda row=row, col=col: self.next_turn(row, col))
                self.game_btns[row][col].grid(row=row, column=col)

        self.stats_label = None
        self.window.mainloop()

    def check_winner(self):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for condition in win_conditions:
            if self.board[condition[0]] == self.board[condition[1]] == self.board[condition[2]] and self.board[condition[0]] != "":
                return self.board[condition[0]]
        return None

    def is_full(self):
        return all(cell != "" for cell in self.board)

    def minimax(self, is_maximizing, depth=0, max_depth=3):
        winner = self.check_winner()
        if winner == "AI":
            return 1
        if winner == "You":
            return -1
        if self.is_full() or depth >= max_depth:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "AI"
                    score = self.minimax(False, depth + 1, max_depth)
                    self.board[i] = ""
                    best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "You"
                    score = self.minimax(True, depth + 1, max_depth)
                    self.board[i] = ""
                    best_score = min(best_score, score)
            return best_score

    def find_best_move(self):
        best_score = -float('inf')
        best_move = None
        move_order = [4, 0, 2, 6, 8, 1, 3, 5, 7]
        for i in move_order:
            if self.board[i] == "":
                self.board[i] = "AI"
                score = self.minimax(False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def next_turn(self, row, col):
        if self.game_btns[row][col]["text"] == "" and self.check_winner() is None:
            index = row * 3 + col
            self.board[index] = "You"
            self.game_btns[row][col]["text"] = "X"
            self.game_btns[row][col].config(fg="blue")

            if self.check_winner() or self.is_full():
                self.end_game()
            else:
                self.ai_move()

    def ai_move(self):
        best_move = self.find_best_move()
        if best_move is not None:
            row, col = divmod(best_move, 3)
            self.board[best_move] = "AI"
            self.game_btns[row][col]["text"] = "O"
            self.game_btns[row][col].config(fg="black")

        if self.check_winner() or self.is_full():
            self.end_game()

    def end_game(self):
        self.games_played += 1
        winner = self.check_winner()

        if winner == "You":
            self.You_win += 1
            self.label.config(text="You Win!")
            self.window.config(bg="green")
        elif winner == "AI":
            self.ai_wins += 1
            self.label.config(text="AI Wins!")
            self.window.config(bg="red")
        else:
            self.Ties += 1
            self.label.config(text="It's a Tie!")
            self.window.config(bg="blue")

        self.restart_btn.pack(side="top")

        if self.games_played == 3:
            self.show_statistics()

    def show_statistics(self):
        self.stats_label = Label(self.window, text=f"Player Wins: {self.You_win} | AI Wins: {self.ai_wins} | Ties: {self.Ties}",
                                 font=('Arial', 20, 'bold'), fg="black")
        self.stats_label.pack(side="top")
        self.window.after(2500, self.hide_statistics)

    def hide_statistics(self):
        self.stats_label.destroy()
        self.reset_statistics()

    def reset_statistics(self):
        self.games_played = 0
        self.You_win_win = 0
        self.ai_wins = 0
        self.Ties = 0

    def start_new_game(self):
        self.player = "You"
        self.board = [""] * 9
        self.label.config(text="Your Turn (You)")
        self.window.config(bg="white")

        for row in range(3):
            for col in range(3):
                self.game_btns[row][col]["text"] = ""
                self.game_btns[row][col].config(fg="black")

        self.restart_btn.pack_forget()

if __name__ == "__main__":
    TicTacToe()
