import tkinter as tk
from random import randint

# Configurazione della finestra di gioco
class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        self.canvas = tk.Canvas(root, width=600, height=300, bg="black")
        self.canvas.pack()
        
        self.snake = [[15, 13], [15, 12], [15, 11]]  # Coordinate iniziali del serpente
        self.food = [randint(1, 29), randint(1, 59)]  # Coordinate iniziali del cibo
        self.direction = "Right"  # Direzione iniziale
        self.running = True  # Stato del gioco
        self.points = 0  # Punteggio iniziale
        
        # Disegna il serpente e il cibo
        self.snake_parts = []
        for segment in self.snake:
            self.snake_parts.append(
                self.canvas.create_rectangle(
                    segment[1]*10, segment[0]*10, 
                    segment[1]*10+10, segment[0]*10+10, 
                    fill="green"
                )
            )
        self.food_item = self.canvas.create_oval(
            self.food[1]*10, self.food[0]*10, 
            self.food[1]*10+10, self.food[0]*10+10, 
            fill="red"
        )
        
        # Mostra il punteggio
        self.score_text = self.canvas.create_text(300, 10, fill="white", text=f"Score: {self.points}")
        
        # Bind dei controlli
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        
        self.update_game()
    
    def change_direction(self, new_direction):
        # Cambia direzione se non opposta
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_direction != opposites.get(self.direction, ""):
            self.direction = new_direction

    def update_game(self):
        if not self.running:
            return
        
        # Calcola la nuova posizione della testa del serpente
        head = self.snake[0].copy()
        if self.direction == "Up":
            head[0] -= 1
        elif self.direction == "Down":
            head[0] += 1
        elif self.direction == "Left":
            head[1] -= 1
        elif self.direction == "Right":
            head[1] += 1
        
        # Controlla collisioni con il bordo o con il corpo
        if (
            head[0] < 0 or head[0] >= 30 or 
            head[1] < 0 or head[1] >= 60 or 
            head in self.snake
        ):
            self.running = False
            self.canvas.create_text(300, 150, fill="white", text="Game Over!", font=("Arial", 24))
            return
        
        # Aggiungi la nuova testa al serpente
        self.snake.insert(0, head)
        self.snake_parts.insert(
            0, 
            self.canvas.create_rectangle(
                head[1]*10, head[0]*10, 
                head[1]*10+10, head[0]*10+10, 
                fill="green"
            )
        )
        
        # Controlla se il serpente ha mangiato il cibo
        if head == self.food:
            self.points += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.points}")
            # Genera un nuovo cibo
            self.food = [randint(1, 29), randint(1, 59)]
            self.canvas.coords(
                self.food_item, 
                self.food[1]*10, self.food[0]*10, 
                self.food[1]*10+10, self.food[0]*10+10
            )
        else:
            # Rimuovi l'ultimo segmento del serpente
            tail = self.snake.pop()
            self.canvas.delete(self.snake_parts.pop())
        
        # Richiama questa funzione dopo un breve intervallo
        self.root.after(100, self.update_game)

# Crea la finestra principale
root = tk.Tk()
game = SnakeGame(root)
root.mainloop()
