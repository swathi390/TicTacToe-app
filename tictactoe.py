import tkinter as tk
from tkinter import messagebox
import random
import winsound  # Use only on Windows. For cross-platform, ask to use pygame.

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.theme = "Light"
        self.mode = "AI"
        self.difficulty = "Medium"
        self.player_score = 0
        self.ai_score = 0
        self.current_player = "X"
        self.board = [""] * 9
        self.buttons = []

        self.colors = {
            "Light": {"bg": "#f0f0f0", "fg": "black", "btn_bg": "white", "highlight": "#add8e6"},
            "Dark": {"bg": "#222222", "fg": "white", "btn_bg": "#444444", "highlight": "#777777"}
        }

        self.create_widgets()
        self.apply_theme()

    def create_widgets(self):
        self.title = tk.Label(self.root, text="Tic-Tac-Toe", font=('Arial', 20, 'bold'))
        self.title.pack(pady=10)

        self.score_label = tk.Label(self.root, text="Player X: 0    Player O: 0", font=('Arial', 14))
        self.score_label.pack()

        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=5)

        self.mode_var = tk.StringVar(value="AI")
        tk.Radiobutton(mode_frame, text="Vs AI", variable=self.mode_var, value="AI", command=self.set_mode).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="2 Player", variable=self.mode_var, value="2P", command=self.set_mode).pack(side=tk.LEFT, padx=10)

        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack()
        self.difficulty_var = tk.StringVar(value="Medium")
        tk.Label(difficulty_frame, text="Difficulty:").pack(side=tk.LEFT)
        for level in ["Easy", "Medium", "Hard"]:
            tk.Radiobutton(difficulty_frame, text=level, variable=self.difficulty_var, value=level).pack(side=tk.LEFT)

        theme_frame = tk.Frame(self.root)
        theme_frame.pack(pady=5)
        tk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT)
        tk.Button(theme_frame, text="Light", command=lambda: self.set_theme("Light")).pack(side=tk.LEFT, padx=5)
        tk.Button(theme_frame, text="Dark", command=lambda: self.set_theme("Dark")).pack(side=tk.LEFT, padx=5)

        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(9):
            button = tk.Button(frame, text="", font=('Arial', 24), width=5, height=2,
                               command=lambda i=i: self.player_move(i))
            button.grid(row=i // 3, column=i % 3)
            self.buttons.append(button)

        tk.Button(self.root, text="Reset Game", font=('Arial', 12), command=self.reset_game).pack(pady=10)

    def apply_theme(self):
        theme = self.colors[self.theme]
        self.root.configure(bg=theme["bg"])
        self.title.config(bg=theme["bg"], fg=theme["fg"])
        self.score_label.config(bg=theme["bg"], fg=theme["fg"])

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=theme["bg"])
                for child in widget.winfo_children():
                    try:
                        child.config(bg=theme["bg"], fg=theme["fg"], selectcolor=theme["bg"])
                    except:
                        pass

        for btn in self.buttons:
            btn.config(bg=theme["btn_bg"], activebackground=theme["highlight"])

    def set_theme(self, theme_choice):
        self.theme = theme_choice
        self.apply_theme()

    def set_mode(self):
        self.mode = self.mode_var.get()
        self.reset_game()

    def player_move(self, index):
        if self.board[index] == "" and self.buttons[index]["state"] == tk.NORMAL:
            self.play_sound()
            self.animate_button(self.buttons[index])
            self.board[index] = self.current_player
            self.buttons[index].config(text=self.current_player)

            if self.check_winner(self.current_player):
                self.update_scores(self.current_player)
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.play_sound(win=True)
                self.disable_buttons()
                return
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.disable_buttons()
                return

            if self.mode == "2P":
                self.current_player = "O" if self.current_player == "X" else "X"
            else:
                self.current_player = "O"
                self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.difficulty_var.get() == "Easy":
            index = random.choice([i for i, v in enumerate(self.board) if v == ""])
        elif self.difficulty_var.get() == "Medium":
            index = self.find_medium_move()
        else:
            index = self.find_best_move()

        if index is not None:
            self.play_sound()
            self.animate_button(self.buttons[index])
            self.board[index] = "O"
            self.buttons[index].config(text="O")

            if self.check_winner("O"):
                self.update_scores("O")
                messagebox.showinfo("Game Over", "Computer wins!")
                self.play_sound(win=True)
                self.disable_buttons()
            elif "" not in self.board:
                messagebox.showinfo("Game Over", "It's a Draw!")
                self.disable_buttons()
            else:
                self.current_player = "X"

    def find_medium_move(self):
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                if self.check_winner("O"):
                    self.board[i] = ""
                    return i
                self.board[i] = ""
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "X"
                if self.check_winner("X"):
                    self.board[i] = ""
                    return i
                self.board[i] = ""
        return random.choice([i for i, v in enumerate(self.board) if v == ""])

    def find_best_move(self):
        best_score = -float('inf')
        best_move = None
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = "O"
                score = self.minimax(False)
                self.board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        return best_move

    def minimax(self, is_maximizing):
        winner = self.get_winner()
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif "" not in self.board:
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "O"
                    score = self.minimax(False)
                    self.board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if self.board[i] == "":
                    self.board[i] = "X"
                    score = self.minimax(True)
                    self.board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def get_winner(self):
        for i, j, k in [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)]:
            if self.board[i] == self.board[j] == self.board[k] != "":
                return self.board[i]
        return None

    def check_winner(self, player):
        win_conditions = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        return any(self.board[i] == self.board[j] == self.board[k] == player for i, j, k in win_conditions)

    def update_scores(self, winner):
        if winner == "X":
            self.player_score += 1
        else:
            self.ai_score += 1
        self.score_label.config(text=f"Player X: {self.player_score}    Player O: {self.ai_score}")

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def reset_game(self):
        self.board = [""] * 9
        self.current_player = "X"
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)

    def play_sound(self, win=False):
        try:
            if win:
                winsound.Beep(1000, 200)
            else:
                winsound.Beep(500, 100)
        except:
            pass  # Skip sound on unsupported systems

    def animate_button(self, button):
        original_color = button.cget("bg")
        button.config(bg="yellow")
        self.root.after(100, lambda: button.config(bg=original_color))

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
