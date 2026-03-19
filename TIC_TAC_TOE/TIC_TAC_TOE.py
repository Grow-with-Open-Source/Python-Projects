from tkinter import *
import tkinter.messagebox as messagebox

tk = Tk()
tk.title("Tic Tac Toe")
tk.configure(bg='yellow')

# Player names
p1 = StringVar()
p2 = StringVar()

player1_name = Entry(tk, textvariable=p1, bd=5, bg='white', width=40)
player1_name.grid(row=1, column=1, columnspan=8)

player2_name = Entry(tk, textvariable=p2, bd=5, bg='white', width=40)
player2_name.grid(row=2, column=1, columnspan=8)

# Score tracking
score_p1 = 0
score_p2 = 0

current_player = "X"
moves_count = 0


def update_scoreboard():
    score_label.config(
        text=f"{p1.get() or 'Player 1'} (X): {score_p1}   |   {p2.get() or 'Player 2'} (O): {score_p2}"
    )


def disable_buttons():
    for row in buttons:
        for button in row:
            button.config(state=DISABLED)


def check_winner():
    global score_p1, score_p2

    win_positions = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)]
    ]

    for combo in win_positions:
        if buttons[combo[0][0]][combo[0][1]]["text"] == \
           buttons[combo[1][0]][combo[1][1]]["text"] == \
           buttons[combo[2][0]][combo[2][1]]["text"] != " ":

            winner_symbol = buttons[combo[0][0]][combo[0][1]]["text"]

            if winner_symbol == "X":
                score_p1 += 1
                winner_name = p1.get() or "Player 1"
            else:
                score_p2 += 1
                winner_name = p2.get() or "Player 2"

            update_scoreboard()
            disable_buttons()
            messagebox.showinfo("Winner", f"{winner_name} wins!")
            return True

    return False


def button_click(row, col):
    global current_player, moves_count

    if buttons[row][col]["text"] == " ":
        buttons[row][col]["text"] = current_player
        moves_count += 1

        if check_winner():
            return

        if moves_count == 9:
            messagebox.showinfo("Tie", "It's a Tie!")
            return

        current_player = "O" if current_player == "X" else "X"
    else:
        messagebox.showinfo("Invalid Move", "Button already clicked!")


def reset_game():
    global current_player, moves_count
    current_player = "X"
    moves_count = 0

    for row in buttons:
        for button in row:
            button.config(text=" ", state=NORMAL)


Label(tk, text="Player 1:", font='Times 20 bold', bg='yellow').grid(row=1, column=0)
Label(tk, text="Player 2:", font='Times 20 bold', bg='yellow').grid(row=2, column=0)

buttons = [[Button(tk, text=" ", font='Times 20 bold', bg='black',
                   fg='white', height=4, width=8,
                   command=lambda r=i, c=j: button_click(r, c))
            for j in range(3)] for i in range(3)]

for i in range(3):
    for j in range(3):
        buttons[i][j].grid(row=i + 3, column=j)

score_label = Label(tk, text="", font='Times 14 bold', bg='yellow')
score_label.grid(row=6, column=0, columnspan=3)

update_scoreboard()

reset_btn = Button(tk, text="Reset Game", font='Times 16 bold',
                   command=reset_game)
reset_btn.grid(row=7, column=0, columnspan=3)

tk.mainloop()
