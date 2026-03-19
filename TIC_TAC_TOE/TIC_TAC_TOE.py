from tkinter import *
import tkinter.messagebox as messagebox

tk = Tk()
tk.title("Tic Tac Toe")
tk.configure(bg='yellow')

# Player names
p1 = StringVar()
p2 = StringVar()

Entry(tk, textvariable=p1, bd=5, bg='white', width=40).grid(row=1, column=1, columnspan=3)
Entry(tk, textvariable=p2, bd=5, bg='white', width=40).grid(row=2, column=1, columnspan=3)

Label(tk, text="Player 1:", font='Times 20 bold', bg='yellow').grid(row=1, column=0)
Label(tk, text="Player 2:", font='Times 20 bold', bg='yellow').grid(row=2, column=0)

# Game state
current_player = "X"
moves_count = 0
score_p1 = 0
score_p2 = 0
move_number = 1

# Buttons
buttons = [[None for _ in range(3)] for _ in range(3)]

def update_scoreboard():
    score_label.config(
        text=f"{p1.get() or 'Player 1'} (X): {score_p1} | {p2.get() or 'Player 2'} (O): {score_p2}"
    )

def disable_buttons():
    for row in buttons:
        for b in row:
            b.config(state=DISABLED)

def check_winner():
    global score_p1, score_p2

    win_positions = [
        [(0,0),(0,1),(0,2)],
        [(1,0),(1,1),(1,2)],
        [(2,0),(2,1),(2,2)],
        [(0,0),(1,0),(2,0)],
        [(0,1),(1,1),(2,1)],
        [(0,2),(1,2),(2,2)],
        [(0,0),(1,1),(2,2)],
        [(0,2),(1,1),(2,0)]
    ]

    for combo in win_positions:
        if buttons[combo[0][0]][combo[0][1]]["text"] == \
           buttons[combo[1][0]][combo[1][1]]["text"] == \
           buttons[combo[2][0]][combo[2][1]]["text"] != " ":

            # ✅ Highlight winning cells
            for pos in combo:
                buttons[pos[0]][pos[1]].config(bg="green")

            winner_symbol = buttons[combo[0][0]][combo[0][1]]["text"]

            if winner_symbol == "X":
                score_p1 += 1
                winner = p1.get() or "Player 1"
            else:
                score_p2 += 1
                winner = p2.get() or "Player 2"

            update_scoreboard()
            messagebox.showinfo("Winner", f"{winner} wins!")
            disable_buttons()
            return True
    return False

def button_click(row, col):
    global current_player, moves_count, move_number

    if buttons[row][col]["text"] == " ":
        buttons[row][col]["text"] = current_player

        # ✅ Move History
        player = p1.get() if current_player == "X" else p2.get()
        player = player or ("Player 1" if current_player == "X" else "Player 2")

        move = f"{move_number}. {player} -> ({row+1},{col+1})"
        history_box.insert(END, move + "\n")

        move_number += 1
        moves_count += 1

        if check_winner():
            return

        if moves_count == 9:
            messagebox.showinfo("Tie", "It's a Tie!")
            disable_buttons()  # ✅ prevent extra clicks
            return

        current_player = "O" if current_player == "X" else "X"

    else:
        messagebox.showinfo("Invalid Move", "Button already clicked!")

def reset_game():
    global current_player, moves_count, move_number

    current_player = "X"
    moves_count = 0
    move_number = 1

    history_box.delete(1.0, END)

    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", bg="black", state=NORMAL)

# Create buttons (safe version)
for i in range(3):
    for j in range(3):
        buttons[i][j] = Button(
            tk, text=" ", font='Times 20 bold', bg='black', fg='white',
            height=4, width=8,
            command=lambda r=i, c=j: button_click(r, c)
        )
        buttons[i][j].grid(row=i+3, column=j)

# Scoreboard
score_label = Label(tk, text="", font='Times 14 bold', bg='yellow')
score_label.grid(row=6, column=0, columnspan=3)
update_scoreboard()

# Reset button
Button(tk, text="Reset Game", font='Times 16 bold',
       command=reset_game).grid(row=7, column=0, columnspan=3)

# Move history UI
Label(tk, text="Move History", font='Times 16 bold', bg='yellow').grid(row=0, column=5)

history_box = Text(tk, height=18, width=28, font=("Consolas", 11))
history_box.grid(row=1, column=5, rowspan=6)

tk.mainloop()