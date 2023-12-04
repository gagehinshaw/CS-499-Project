import tkinter as tk

# Initialize the board
board = [' ' for _ in range(9)]
player = 'X'

# Function to check if the game is over
def game_over():
    # Check rows for a match
    for i in range(0, 9, 3):
        if board[i] == board[i + 1] == board[i + 2] != ' ':
            return True
    # Check columns for a match
    for i in range(3):
        if board[i] == board[i + 3] == board[i + 6] != ' ':
            return True
    # Check diagonals for a match
    if board[0] == board[4] == board[8] != ' ':
        return True
    if board[2] == board[4] == board[6] != ' ':
        return True
    return False

# Function to handle a button click (player move)
def on_click(button_id):
    global player
    if board[button_id] == ' ':
        board[button_id] = player
        buttons[button_id].config(text=player)
        if game_over():
            show_result()
        if not game_over() and ' ' not in board:
            show_result()
        else:
            player = 'O' if player == 'X' else 'X'

# Function to show the result of the game
def show_result():
    global player
    # Declare player as local variable
    if game_over():
        winner = 'X' if player == 'X' else 'O'
        result_label.config(text=f"Player {winner} wins!")
        # Changes the text on the result label to announce a winner
    else:
        result_label.config(text="It's a tie!")
        # Likewise with this for a tie^

# Create the main application window
root = tk.Tk()
root.title("Tic-Tac-Toe")

# Create and place the buttons for the game board
buttons = []
for i in range(9):
    button = tk.Button(root, text=' ', width=6, height=3, command=lambda id=i: on_click(id))
    # Makes the actual clickable buttons, determines their qualities
    button.grid(row=i // 3, column=i % 3)
    # Puts the buttons into an easy grid shape
    buttons.append(button)

# Create a label to display the result
result_label = tk.Label(root, text="", font=("Helvetica", 16))
result_label.grid(row=3, columnspan=3)

# Start the GUI event loop
root.mainloop()
