from tkinter import *
import tkinter.messagebox
tk = Tk()
tk.title("Tic Tac Toe")
tk.configure(bg='yellow')
p1 = StringVar()
p2 = StringVar()
player1_name = Entry(textvariable=p1, bd=5, bg='white', width=40)
player1_name.grid(row=1, column=1, columnspan=8)
player2_name = Entry(tk, textvariable=p2, bd=5, bg='white', width=40)
player2_name.grid(row=2, column=1, columnspan=8)
bclick = True
flag = 0
current_player_name = p1.get() if p1.get() else 'X'
def disableButton():
    for i in range(3):
        for j in range(3):
            buttons[i][j].configure(state=DISABLED)
def checkForWin():
    for i in range(3):
        if buttons[i][0]["text"] == buttons[i][1]["text"] == buttons[i][2]["text"] != " ":
            buttons[i][0].config(bg="green")
            buttons[i][1].config(bg="green")
            buttons[i][2].config(bg="green")
            disableButton()
            winner_name = p1.get() if buttons[i][0]['text'] == 'X' else p2.get()
            if not winner_name:
                winner_name = 'Player 1' if buttons[i][0]['text'] == 'X' else 'Player 2'
            tkinter.messagebox.showinfo("Tic-Tac-Toe", f"{winner_name} wins!")
            return
        if buttons[0][i]["text"] == buttons[1][i]["text"] == buttons[2][i]["text"] != " ":
            buttons[0][i].config(bg="green")
            buttons[1][i].config(bg="green")
            buttons[2][i].config(bg="green")
            disableButton()
            winner_name = p1.get() if buttons[0][i]['text'] == 'X' else p2.get()
            if not winner_name:
                winner_name = 'Player 1' if buttons[0][i]['text'] == 'X' else 'Player 2'
            tkinter.messagebox.showinfo("Tic-Tac-Toe", f"{winner_name} wins!")
            return
    if buttons[0][0]["text"] == buttons[1][1]["text"] == buttons[2][2]["text"] != " ":
        buttons[0][0].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][2].config(bg="green")
        disableButton()
        winner_name = p1.get() if buttons[0][0]['text'] == 'X' else p2.get()
        if not winner_name:
            winner_name = 'Player 1' if buttons[0][0]['text'] == 'X' else 'Player 2'
        tkinter.messagebox.showinfo("Tic-Tac-Toe", f"{winner_name} wins!")
        return
    if buttons[0][2]["text"] == buttons[1][1]["text"] == buttons[2][0]["text"] != " ":
        buttons[0][2].config(bg="green")
        buttons[1][1].config(bg="green")
        buttons[2][0].config(bg="green")
        disableButton()
        winner_name = p1.get() if buttons[0][2]['text'] == 'X' else p2.get()
        if not winner_name:
            winner_name = 'Player 1' if buttons[0][2]['text'] == 'X' else 'Player 2'
        tkinter.messagebox.showinfo("Tic-Tac-Toe", f"{winner_name} wins!")
        return
    if flag == 8:
        tkinter.messagebox.showinfo("Tic-Tac-Toe", "It's a Tie")
def resetGame():
    global bclick, flag, current_player_name
    for i in range(3):
        for j in range(3):
            buttons[i][j]["text"] = " "
            buttons[i][j].config(bg='black', state=NORMAL)
    bclick = True
    flag = 0
    current_player_name = p1.get() if p1.get() else 'X'
Label(tk, text="Player 1:", font='Times 20 bold', bg='yellow', fg='black', height=1, width=8).grid(row=1, column=0)
Label(tk, text="Player 2:", font='Times 20 bold', bg='yellow', fg='black', height=1, width=8).grid(row=2, column=0)
buttons = [[Button(tk, text=' ', font='Times 20 bold', bg='black', fg='white', height=4, width=8) for _ in range(3)] for _ in range(3)]
def btnClick(button):
    global bclick, flag
    if button["text"] == " ":
        if bclick:
            button["text"] = "X"
        else:
            button["text"] = "O"
        bclick = not bclick
        flag += 1
        checkForWin()
    else:
        tkinter.messagebox.showinfo("Tic-Tac-Toe", "Button already Clicked!")
for i in range(3):
    for j in range(3):
        buttons[i][j].configure(command=lambda row=i, col=j: btnClick(buttons[row][col]))
        buttons[i][j].grid(row=i + 3, column=j)
reset_button = Button(tk, text="Reset Game", font='Times 16 bold', bg='white', fg='black', command=resetGame)
reset_button.grid(row=6, column=0, columnspan=3)
tk.mainloop()