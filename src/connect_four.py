import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel, Label, Button, Menu, colorchooser

# Constants for the game
ROWS = 6
COLUMNS = 7
EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2


class ConnectFour:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.default_colors = {PLAYER_X: 'red', PLAYER_O: 'yellow', EMPTY: 'white'}
        self.colors = self.default_colors.copy()
        self.player = PLAYER_X
        self.board = [[EMPTY] * COLUMNS for _ in range(ROWS)]
        self.create_widgets()
        self.create_menu()

    def create_widgets(self):
        self.buttons = []
        for col in range(COLUMNS):
            button = tk.Button(self.master, text=f"Col {col + 1}", command=lambda c=col: self.make_move(c))
            button.grid(row=0, column=col, sticky="ew", padx=2, pady=2)
            self.buttons.append(button)

        self.labels = [[tk.Label(self.master, width=8, height=3, bg='white', relief="raised")
                        for _ in range(COLUMNS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLUMNS):
                self.labels[r][c].grid(row=r + 1, column=c, padx=2, pady=2)

    def create_menu(self):
        menu_bar = Menu(self.master)
        self.master.config(menu=menu_bar)

        game_menu = Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Settings", menu=game_menu)
        game_menu.add_command(label="Player Color Setup", command=self.setup_players)
        game_menu.add_command(label="Restart Game", command=self.restart_game)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=self.master.quit)

    def setup_players(self):
        setup_window = Toplevel(self.master)
        setup_window.title("Player Setup")

        Label(setup_window, text="Choose method for setting colors:").grid(row=0, column=0, columnspan=2)

        Button(setup_window, text="Text Input", command=lambda: self.setup_players_text(setup_window)).grid(row=1,
                                                                                                            column=0,
                                                                                                            padx=10,
                                                                                                            pady=10)
        Button(setup_window, text="Color Picker", command=lambda: self.setup_players_color_picker(setup_window)).grid(
            row=1, column=1, padx=10, pady=10)

    def setup_players_text(self, parent_window):
        parent_window.destroy()

        setup_window = Toplevel(self.master)
        setup_window.title("Player Setup")

        Label(setup_window, text="Player 1 Color:").grid(row=0, column=0)
        player1_color = tk.Entry(setup_window)
        player1_color.insert(0, self.default_colors[PLAYER_X])
        player1_color.grid(row=0, column=1)

        Label(setup_window, text="Player 2 Color:").grid(row=1, column=0)
        player2_color = tk.Entry(setup_window)
        player2_color.insert(0, self.default_colors[PLAYER_O])
        player2_color.grid(row=1, column=1)

        def save_colors():
            self.colors[PLAYER_X] = player1_color.get()
            self.colors[PLAYER_O] = player2_color.get()
            setup_window.destroy()

        Button(setup_window, text="Start Game", command=save_colors).grid(row=2, column=0, columnspan=2)

    def setup_players_color_picker(self, parent_window):
        parent_window.destroy()

        setup_window = Toplevel(self.master)
        setup_window.title("Player Setup")

        def choose_color(player):
            color = colorchooser.askcolor()[1]
            if player == PLAYER_X:
                player1_color.configure(bg=color)
                self.colors[PLAYER_X] = color
            else:
                player2_color.configure(bg=color)
                self.colors[PLAYER_O] = color

        Label(setup_window, text="Player 1 Color:").grid(row=0, column=0)
        player1_color = tk.Label(setup_window, text="       ", bg=self.default_colors[PLAYER_X], relief="raised")
        player1_color.grid(row=0, column=1)
        Button(setup_window, text="Choose Color", command=lambda: choose_color(PLAYER_X)).grid(row=0, column=2)

        Label(setup_window, text="Player 2 Color:").grid(row=1, column=0)
        player2_color = tk.Label(setup_window, text="       ", bg=self.default_colors[PLAYER_O], relief="raised")
        player2_color.grid(row=1, column=1)
        Button(setup_window, text="Choose Color", command=lambda: choose_color(PLAYER_O)).grid(row=1, column=2)

        Button(setup_window, text="Start Game", command=setup_window.destroy).grid(row=2, column=0, columnspan=3)

    def animate_drop(self, col, row_end):
        for row in range(row_end + 1):
            if row > 0:
                self.labels[row - 1][col].configure(bg='white')
            self.labels[row][col].configure(bg=self.colors[self.player])
            self.master.update()
            self.master.after(50)  # Animation speed in milliseconds

    def make_move(self, col):
        self.disable_buttons()
        row = self.find_row(col)
        if row is not None:
            self.animate_drop(col, row)
            self.board[row][col] = self.player
            if self.check_winner(row, col):
                self.update_board_colors()
                messagebox.showinfo("Game Over", f"Player {self.colors[self.player]} wins!")
                if messagebox.askyesno("Game Over", "Would you like to restart the game?"):
                    self.restart_game()
                else:
                    self.master.quit()
            elif self.is_board_full():
                self.update_board_colors()
                messagebox.showinfo("Game Over", "The game ends in a draw!")
                if messagebox.askyesno("Game Over", "Would you like to restart the game?"):
                    self.restart_game()
                else:
                    self.master.quit()
            else:
                self.player = PLAYER_X if self.player == PLAYER_O else PLAYER_O
        else:
            messagebox.showwarning("Invalid Move", "This column is full. Choose another column.")
        self.enable_buttons()

    def find_row(self, col):
        for row in range(ROWS - 1, -1, -1):
            if self.board[row][col] == EMPTY:
                return row
        return None

    def check_winner(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            count += self.count_discs(row, col, dr, dc)
            count += self.count_discs(row, col, -dr, -dc)
            if count >= 4:
                return True
        return False

    def count_discs(self, row, col, dr, dc):
        r, c = row + dr, col + dc
        count = 0
        while 0 <= r < ROWS and 0 <= c < COLUMNS and self.board[r][c] == self.player:
            count += 1
            r += dr
            c += dc
        return count

    def is_board_full(self):
        for row in self.board:
            if EMPTY in row:
                return False
        return True

    def restart_game(self):
        self.board = [[EMPTY] * COLUMNS for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLUMNS):
                self.labels[row][col].configure(bg='white')
        self.player = PLAYER_X

    def disable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def enable_buttons(self):
        for button in self.buttons:
            button.config(state=tk.NORMAL)

    def update_board_colors(self):
        for r in range(ROWS):
            for c in range(COLUMNS):
                if self.board[r][c] == PLAYER_X:
                    self.labels[r][c].configure(bg=self.colors[PLAYER_X])
                elif self.board[r][c] == PLAYER_O:
                    self.labels[r][c].configure(bg=self.colors[PLAYER_O])


if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFour(root)
    root.mainloop()
