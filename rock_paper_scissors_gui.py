import random
import tkinter as tk

# ---------- Colors ----------
BG = "#0B1020"
PANEL = "#141C32"
PANEL_LIGHT = "#1C2845"
TEXT = "#F4F7FF"
MUTED = "#9AA8C7"
CYAN = "#43E7E1"
PURPLE = "#A78BFA"
GREEN = "#4ADE80"
RED = "#FB7185"
GOLD = "#FBBF24"

CHOICES = {
    "rock": ("✊", "ROCK"),
    "paper": ("✋", "PAPER"),
    "scissors": ("✌", "SCISSORS"),
}


class RockPaperScissors:
    def __init__(self, root):
        self.root = root
        self.root.title("ROCK • PAPER • SCISSORS")
        self.root.geometry("900x700")
        self.root.minsize(760, 650)
        self.root.configure(bg=BG)

        self.player_score = 0
        self.computer_score = 0
        self.round_number = 0
        self.game_over_dialog = None

        self.build_ui()

    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill="x", padx=32, pady=(24, 12))

        tk.Label(
            header, text="ARCADE  /  CLASSIC GAME",
            font=("Arial", 9, "bold"), fg=CYAN, bg=BG
        ).pack()

        tk.Label(
            header, text="ROCK  PAPER  SCISSORS",
            font=("Arial", 25, "bold"), fg=TEXT, bg=BG
        ).pack(pady=(7, 3))

        tk.Label(
            header, text="MAKE YOUR MOVE. BEAT THE COMPUTER.",
            font=("Arial", 10), fg=MUTED, bg=BG
        ).pack()

        # Scoreboard
        score_frame = tk.Frame(self.root, bg=BG)
        score_frame.pack(fill="x", padx=32, pady=14)
        score_frame.columnconfigure(0, weight=1)
        score_frame.columnconfigure(1, weight=1)

        self.player_score_label = self.make_score_card(
            score_frame, 0, "YOU", "0", CYAN
        )
        self.computer_score_label = self.make_score_card(
            score_frame, 1, "COMPUTER", "0", PURPLE
        )

        # Battle arena
        arena = tk.Frame(
            self.root, bg=PANEL, highlightbackground="#263454",
            highlightthickness=1
        )
        arena.pack(fill="x", padx=32, pady=8)

        arena.grid_columnconfigure(0, weight=1)
        arena.grid_columnconfigure(1, weight=1)

        tk.Label(
            arena, text="YOUR MOVE", font=("Arial", 9, "bold"),
            fg=MUTED, bg=PANEL
        ).grid(row=0, column=0, pady=(20, 7))

        tk.Label(
            arena, text="COMPUTER'S MOVE", font=("Arial", 9, "bold"),
            fg=MUTED, bg=PANEL
        ).grid(row=0, column=1, pady=(20, 7))

        self.player_move = tk.Label(
            arena, text="❔", font=("Arial", 48), fg=CYAN, bg=PANEL
        )
        self.player_move.grid(row=1, column=0, pady=4)

        self.computer_move = tk.Label(
            arena, text="❔", font=("Arial", 48), fg=PURPLE, bg=PANEL
        )
        self.computer_move.grid(row=1, column=1, pady=4)

        self.status_label = tk.Label(
            arena, text="CHOOSE YOUR WEAPON",
            font=("Arial", 12, "bold"), fg=GOLD, bg=PANEL
        )
        self.status_label.grid(row=2, column=0, columnspan=2, pady=(8, 20))

        # Choice buttons
        tk.Label(
            self.root, text="SELECT YOUR MOVE",
            font=("Arial", 10, "bold"), fg=MUTED, bg=BG
        ).pack(pady=(16, 10))

        buttons = tk.Frame(self.root, bg=BG)
        buttons.pack(padx=32, fill="x")
        for col in range(3):
            buttons.columnconfigure(col, weight=1)

        button_data = [
            ("rock", "✊", "ROCK", CYAN),
            ("paper", "✋", "PAPER", PURPLE),
            ("scissors", "✌", "SCISSORS", GREEN),
        ]

        for col, (key, emoji, label, accent) in enumerate(button_data):
            btn = tk.Button(
                buttons,
                text=f"{emoji}\n{label}",
                command=lambda move=key: self.play_round(move),
                font=("Arial", 15, "bold"),
                fg=TEXT,
                bg=PANEL_LIGHT,
                activeforeground=BG,
                activebackground=accent,
                relief="flat",
                bd=0,
                cursor="hand2",
                pady=13,
                highlightthickness=1,
                highlightbackground=accent,
            )
            btn.grid(row=0, column=col, sticky="ew", padx=7, ipady=5)

        self.round_label = tk.Label(
            self.root, text="ROUND 01",
            font=("Arial", 9, "bold"), fg="#526282", bg=BG
        )
        self.round_label.pack(pady=(18, 8))

        tk.Label(
            self.root, text="GOOD LUCK • HAVE FUN",
            font=("Arial", 8), fg="#526282", bg=BG
        ).pack(pady=(0, 14))

    def make_score_card(self, parent, column, title, score, accent):
        card = tk.Frame(
            parent, bg=PANEL, highlightbackground="#263454",
            highlightthickness=1
        )
        card.grid(row=0, column=column, sticky="ew", padx=6)
        tk.Label(
            card, text=title, font=("Arial", 9, "bold"),
            fg=accent, bg=PANEL
        ).pack(pady=(12, 2))
        score_label = tk.Label(
            card, text=score, font=("Arial", 28, "bold"),
            fg=TEXT, bg=PANEL
        )
        score_label.pack(pady=(0, 10))
        return score_label

    def play_round(self, player_choice):
        # Prevent another round while the result dialog is open.
        if self.game_over_dialog is not None:
            return

        computer_choice = random.choice(list(CHOICES.keys()))
        self.round_number += 1

        self.player_move.config(text=CHOICES[player_choice][0])
        self.computer_move.config(text=CHOICES[computer_choice][0])
        self.round_label.config(text=f"ROUND {self.round_number:02d}")

        if player_choice == computer_choice:
            outcome = "draw"
            title = "IT'S A DRAW!"
            message = "Great minds think alike."
            accent = GOLD
        elif (
            (player_choice == "rock" and computer_choice == "scissors")
            or (player_choice == "paper" and computer_choice == "rock")
            or (player_choice == "scissors" and computer_choice == "paper")
        ):
            outcome = "win"
            self.player_score += 1
            title = "WINNER WINNER\nCHICKEN DINNER!"
            message = "You crushed that round!"
            accent = GREEN
        else:
            outcome = "lose"
            self.computer_score += 1
            title = "LOSER"
            message = "The computer got this one."
            accent = RED

        self.player_score_label.config(text=str(self.player_score))
        self.computer_score_label.config(text=str(self.computer_score))
        self.status_label.config(text=title.replace("\n", " "), fg=accent)

        self.show_result_dialog(
            outcome, title, message, accent, player_choice, computer_choice
        )

    def show_result_dialog(
        self, outcome, title, message, accent, player_choice, computer_choice
    ):
        dialog = tk.Toplevel(self.root)
        self.game_over_dialog = dialog
        dialog.title("Round Result")
        dialog.configure(bg=BG)
        dialog.resizable(False, False)
        dialog.transient(self.root)
        dialog.grab_set()

        # Center dialog over the main window.
        self.root.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - 440) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - 390) // 2
        dialog.geometry(f"440x390+{max(0, x)}+{max(0, y)}")

        top = tk.Frame(dialog, bg=accent, height=7)
        top.pack(fill="x")

        tk.Label(
            dialog, text="ROUND COMPLETE",
            font=("Arial", 9, "bold"), fg=accent, bg=BG
        ).pack(pady=(23, 9))

        tk.Label(
            dialog, text=title, font=("Arial", 23, "bold"),
            fg=TEXT if outcome == "draw" else accent, bg=BG,
            justify="center", wraplength=390
        ).pack(padx=20, pady=4)

        tk.Label(
            dialog, text=message, font=("Arial", 11),
            fg=MUTED, bg=BG
        ).pack(pady=(5, 17))

        moves = tk.Frame(dialog, bg=PANEL)
        moves.pack(fill="x", padx=28, pady=(0, 18))
        moves.columnconfigure(0, weight=1)
        moves.columnconfigure(1, weight=1)

        tk.Label(
            moves, text=f"YOU\n{CHOICES[player_choice][0]}  {CHOICES[player_choice][1]}",
            font=("Arial", 11, "bold"), fg=CYAN, bg=PANEL,
            justify="center"
        ).grid(row=0, column=0, padx=8, pady=13)

        tk.Label(
            moves,
            text=f"COMPUTER\n{CHOICES[computer_choice][0]}  {CHOICES[computer_choice][1]}",
            font=("Arial", 11, "bold"), fg=PURPLE, bg=PANEL,
            justify="center"
        ).grid(row=0, column=1, padx=8, pady=13)

        actions = tk.Frame(dialog, bg=BG)
        actions.pack(fill="x", padx=28)

        play_again = tk.Button(
            actions, text="PLAY AGAIN",
            command=self.close_result_dialog,
            font=("Arial", 10, "bold"), fg=BG, bg=accent,
            activebackground=TEXT, activeforeground=BG,
            relief="flat", cursor="hand2", pady=11
        )
        play_again.pack(side="left", fill="x", expand=True, padx=(0, 6))

        quit_button = tk.Button(
            actions, text="EXIT GAME",
            command=self.root.destroy,
            font=("Arial", 10, "bold"), fg=TEXT, bg=PANEL_LIGHT,
            activebackground="#2B3858", activeforeground=TEXT,
            relief="flat", cursor="hand2", pady=11
        )
        quit_button.pack(side="left", fill="x", expand=True, padx=(6, 0))

        dialog.protocol("WM_DELETE_WINDOW", self.close_result_dialog)
        dialog.bind("<Return>", lambda _event: self.close_result_dialog())
        dialog.bind("<Escape>", lambda _event: self.close_result_dialog())
        play_again.focus_set()

    def close_result_dialog(self):
        if self.game_over_dialog is not None:
            dialog = self.game_over_dialog
            self.game_over_dialog = None
            try:
                dialog.grab_release()
                dialog.destroy()
            except tk.TclError:
                pass


if __name__ == "__main__":
    root = tk.Tk()
    app = RockPaperScissors(root)
    root.mainloop()
