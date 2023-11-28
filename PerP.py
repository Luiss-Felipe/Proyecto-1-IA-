# Proyecto de primer parcial Juego de Gato 4x4 implementando el algoritmo de minimax con poda alfa-feta

#Alan Daniel Sigala Morales.
#Diego Fernando Badillo Vega.
#Luis Felipe Tarelo Ramírez.
#Irving Rodriguez Rodriguez.
#Raúl Alejandro Moreno Camargo.

# Version 2.0.1

# Librerias utilizadas para la implementacion del juego gato 
import math
import tkinter as tk
import random
from tkinter import messagebox

#/////////////////////////////////////////////////1314
#Comienzo del programa

#  imprimir el tablero del gato 4x4 en pantalla  
def Juego(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
        
# En esta parte se va a verificar si alguien ha ganado
def Ganador(board, player):
    for row in board:
        if row.count(player) == 4:
            return True

    for i in range(4):
        if [board[j][i] for j in range(4)].count(player) == 4:
            return True

    if [board[i][i] for i in range(4)].count(player) == 4 or [board[i][3 - i] for i in range(4)].count(player) == 4:
        return True

    return False

# Función para verificar si el tablero está lleno
def Juegocompleto(board):
    return all([cell != ' ' for row in board for cell in row])

# Función para obtener la lista de movimientos válidos
def movimientos(board):
    return [(i, j) for i in range(4) for j in range(4) if board[i][j] == ' ']

# Función para evaluar el tablero
def evaluate(board):
    if Ganador(board, 'X'):
        return 1
    elif Ganador(board, 'O'):
        return -1
    elif Juegocompleto(board):
        return 0
    else:
        return None
    
    # Función del algoritmo  Minimax con poda alfa-beta
def minimax(board, depth, maximizing_player, alpha, beta):
    if depth == 0 or evaluate(board) is not None:
        return evaluate(board) if evaluate(board) is not None else 0

    if maximizing_player:
        max_eval = -math.inf
        for move in movimientos(board):
            new_board = [row[:] for row in board]
            new_board[move[0]][move[1]] = 'X'
            eval = minimax(new_board, depth-1, False, alpha, beta)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in movimientos(board):
            new_board = [row[:] for row in board]
            new_board[move[0]][move[1]] = 'O'
            eval = minimax(new_board, depth-1, True, alpha, beta)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval
    
    # Función para obtener el mejor movimiento
def best_move(board):
    moves = movimientos(board)
    random.shuffle(moves)  # Barajar la lista de movimientos
    max_eval = -math.inf
    best_move = None
    for current_move in moves:
        new_board = [row[:] for row in board]
        new_board[current_move[0]][current_move[1]] = 'X'
        eval = minimax(new_board, 4, False, -math.inf, math.inf)
        if eval > max_eval:
            max_eval = eval
            best_move = current_move
    return best_move
    # Función para actualizar la interfaz gráfica con el estado actual del tablero
def edoactual(board_buttons, board):
    for i in range(4):
        for j in range(4):
            board_buttons[i][j].config(text=board[i][j])
            
            # Función para manejar el clic en una celda
def cell_click(board_buttons, board, row, col, player_label):
    if board[row][col] == ' ':
        board[row][col] = 'X'
        edoactual(board_buttons, board)
        winner = evaluate(board)
        if winner is not None:
            if winner == 1:
                messagebox.showinfo("Felicitaciones","¡ganaste amigo!")
            elif winner == -1:
                messagebox.showinfo("Lo lamento","Has perdido amigo :( ")
            else:
                messagebox.showinfo("Vaya", "Has empatado con la IA")
            root.quit()
        else:
            move = best_move(board)
            board[move[0]][move[1]] = 'O'
            edoactual(board_buttons, board)
            winner = evaluate(board)
            if winner is not None:
                if winner == 1:
                    messagebox.showinfo("¡Ganaste!", "¡Ganaste!")
                elif winner == -1:
                    messagebox.showinfo("Lo lamento","Has perdido amigo :( ")
                else:
                    messagebox.showinfo("Vaya", "Has empatado con la IA")
                root.quit()
                
 # Crear la ventana principal
root = tk.Tk()
root.title("Proyecto Primer Parcial")

# Establecer el tamaño de los botones
button_size = 100

# Creacion de botones de la interfaz del juego
board_buttons = [[tk.Button(root, text=' ', font=('Arial', 24), width=6, height=3,
                           command=lambda i=i, j=j: cell_click(board_buttons, board, i, j, player_label),
                           bg='#D7FCB8', fg='#FF3B33') 
                 for j in range(4)] for i in range(4)]

# Configuracion del posicionamiento de  los botones en la ventana
for i in range(4):
    for j in range(4):
        board_buttons[i][j].grid(row=i+1, column=j, padx=5, pady=5)

# Estilizar etiqueta de turno del jugador
player_label = tk.Label(root, text="Gato 4x4 (X)", font=("Helvetica", 16), bg='#ffffff', fg='#000000')
player_label.grid(row=0, column=0, columnspan=4, pady=(0, 10))

# Iniciar el juego
board = [[' ' for _ in range(4)] for _ in range(4)]
player = 'X'
edoactual(board_buttons, board)
root.mainloop()