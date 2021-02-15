import tkinter as tk


def start_game():

    def select(row, column):
        old_button = boxes[row][column]
        new_box = tk.Label(text=symbols[current_player - 1])
        if current_player == 1:
            new_box.config(fg="red")
        if current_player == 2:
            new_box.config(fg="blue")
        boxes[row][column] = new_box
        old_button.destroy()
        new_box.grid(row=row+1, column=column)
        var.set(1)
    start.destroy()
    boxes = []
    for r in range(1, 4):
        row = []
        for c in range(3):
            box = tk.Button(text="", width=5, height=5, bg="white",
                            command=lambda r_index=r-1, c_index=c: select(r_index, c_index))
            box.grid(row=r, column=c)
            row.append(box)
        boxes.append(row)
    num_turns = 0
    winner, full = None, False
    symbols = ["X", "O"]
    var = tk.IntVar()
    while not winner and not full:
        current_player = num_turns % 2 + 1
        current_turn = tk.Label(text="Player " + str(current_player) + "'s turn")
        current_turn.grid(row=4, columnspan=3)
        window.wait_variable(var)
        if is_winner(boxes):
            winner = current_player
            convert_remaining_buttons(boxes)
            current_turn.config(text="Player " + str(winner) + " has won the game!")
        elif is_full(boxes):
            full = True
            current_turn.config(text="Neither player has won the game.")
        num_turns += 1


def is_winner(boxes):
    '''Checks if there is a winner based on the state of the board'''
    for row in range(len(boxes)):
        if all([val.cget("text") == boxes[row][0].cget("text") and val.cget("text") for val in boxes[row]]):
            for val in boxes[row]:
                val.config(bg="yellow")
            return True
    for column in range(len(boxes[0])):
        if all([boxes[row][column].cget("text") == boxes[0][column].cget("text") and boxes[row][column].cget("text") for row in range(len(boxes))]):
            for row in range(len(boxes)):
                boxes[row][column].config(bg="yellow")
            return True
    if boxes[1][1].cget("text"):
        if boxes[0][2].cget("text") == boxes[1][1].cget("text") and boxes[1][1].cget("text") == boxes[2][0].cget("text"):
            boxes[0][2].config(bg="yellow")
            boxes[1][1].config(bg="yellow")
            boxes[2][0].config(bg="yellow")
            return True
        if boxes[0][0].cget("text") == boxes[1][1].cget("text") and boxes[1][1].cget("text") == boxes[2][2].cget("text"):
            boxes[0][0].config(bg="yellow")
            boxes[1][1].config(bg="yellow")
            boxes[2][2].config(bg="yellow")
            return True
    return False


def is_full(boxes):
    '''Checks if all spaces on the board have already been selected'''
    for row in range(len(boxes)):
        for column in range(len(boxes[row])):
            if not boxes[row][column].cget("text"):
                return False
    return True


def convert_remaining_buttons(boxes):
    for row in range(len(boxes)):
        for box in boxes[row]:
            if type(box) == tk.Button:
                old_button = box
                box = tk.Label(text="")
                old_button.destroy()


window = tk.Tk()
title = tk.Label(text="TicTacToe")
title.grid(columnspan=3)
start = tk.Button(text="Start Game", width=8, height=2, bg="white", command=start_game)
start.grid(row=1, columnspan=3)
window.mainloop()
