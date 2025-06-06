import tkinter as tk
from tkinter import messagebox
import winsound  # Only works on Windows

class TicTacToePro:
    def __init__(self, root):
        self.root = root
        self.root.title("✨ Tic Tac Toe Pro")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)

        self.current_player = "X"
        self.score = {"X": 0, "O": 0}
        self.colors = {"X": "#ff4d4d", "O": "#4dd2ff"}

        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.create_ui()

    def create_ui(self):
        self.status_label = tk.Label(self.root, text="Player X's Turn", font=("Comic Sans MS", 16, "bold"),
                                     fg="white", bg="#1e1e1e", pady=10)
        self.status_label.grid(row=0, column=0, columnspan=3)

        self.score_label = tk.Label(self.root, text=self.get_score_text(),
                                    font=("Arial", 12), fg="lightgreen", bg="#1e1e1e")
        self.score_label.grid(row=1, column=0, columnspan=3)

        for row in range(3):
            for col in range(3):
                btn = tk.Button(self.root, text="", font=("Comic Sans MS", 32, "bold"),
                                width=5, height=2, bg="#2e2e2e", fg="#fff",
                                activebackground="#444",
                                command=lambda r=row, c=col: self.on_click(r, c))
                btn.grid(row=row+2, column=col, padx=5, pady=5)
                self.buttons[row][col] = btn

        self.restart_btn = tk.Button(self.root, text="🔁 Restart", font=("Arial", 12, "bold"),
                                     bg="#ffcc00", command=self.reset_board)
        self.restart_btn.grid(row=5, column=0, columnspan=1, pady=10)

        self.quit_btn = tk.Button(self.root, text="❌ Quit", font=("Arial", 12, "bold"),
                                  bg="#ff6666", command=self.root.quit)
        self.quit_btn.grid(row=5, column=2, columnspan=1, pady=10)

    def get_score_text(self):
        return f"Score - X: {self.score['X']}  |  O: {self.score['O']}"

    def on_click(self, row, col):
        btn = self.buttons[row][col]
        if btn["text"] == "":
            btn["text"] = self.current_player
            btn["fg"] = self.colors[self.current_player]
            self.play_sound("click")

            if self.check_winner(self.current_player):
                self.highlight_winner()
                self.score[self.current_player] += 1
                self.status_label.config(text=f"🎉 Player {self.current_player} Wins!")
                self.root.after(1500, lambda: self.show_result(f"Player {self.current_player} Wins!"))
            elif self.is_draw():
                self.status_label.config(text="🤝 It's a Draw!")
                self.root.after(1500, lambda: self.show_result("It's a Draw!"))
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.status_label.config(text=f"Player {self.current_player}'s Turn")

    def play_sound(self, sound_type):
        try:
            if sound_type == "click":
                winsound.MessageBeep()
            elif sound_type == "win":
                winsound.Beep(700, 300)
        except:
            pass  # Sound may not work on all platforms

    def check_winner(self, player):
        self.win_cells = []

        for i in range(3):
            if all(self.buttons[i][j]["text"] == player for j in range(3)):
                self.win_cells = [(i, j) for j in range(3)]
                return True
            if all(self.buttons[j][i]["text"] == player for j in range(3)):
                self.win_cells = [(j, i) for j in range(3)]
                return True
        if all(self.buttons[i][i]["text"] == player for i in range(3)):
            self.win_cells = [(i, i) for i in range(3)]
            return True
        if all(self.buttons[i][2 - i]["text"] == player for i in range(3)):
            self.win_cells = [(i, 2 - i) for i in range(3)]
            return True
        return False

    def is_draw(self):
        return all(self.buttons[i][j]["text"] != "" for i in range(3) for j in range(3))

    def highlight_winner(self):
        for r, c in self.win_cells:
            self.buttons[r][c].config(bg="#33cc33")
        self.play_sound("win")

    def show_result(self, msg):
        messagebox.showinfo("Game Over", msg)
        self.reset_board()

    def reset_board(self):
        for row in self.buttons:
            for btn in row:
                btn.config(text="", bg="#2e2e2e", fg="#fff")
        self.status_label.config(text="Player X's Turn")
        self.current_player = "X"
        self.score_label.config(text=self.get_score_text())

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToePro(root)
    root.mainloop()