import tkinter as tk  # Importiamo la libreria tkinter per creare la GUI
from random import randint  # Importiamo randint per generare posizioni casuali
from PIL import Image, ImageTk  # Importiamo Image e ImageTk per caricare immagini

# Classe principale per il gioco Snake
class SnakeGame:
    def __init__(self, root):
        # Configurazione della finestra principale
        self.root = root
        self.root.title("Snake Game")  # Titolo della finestra
        
        # Carica l'immagine di sfondo
        self.background_image = Image.open("img/grass.jpg")  # Sostituisci con il path dell'immagine
        self.background_image = self.background_image.resize((600, 300))  # Ridimensiona l'immagine a 600x300
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Canvas (area di gioco): 600x300 pixel, sfondo nero
        self.canvas = tk.Canvas(root, width=600, height=300, bg="black")
        self.canvas.pack()
        
         # Aggiungi l'immagine come sfondo
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)


        # Stato iniziale del gioco
        self.snake = [[15, 13], [15, 12], [15, 11]]  # Coordinate iniziali del serpente
        self.food = [randint(1, 29), randint(1, 59)]  # Posizione iniziale del cibo (casuale)
        self.direction = "Right"  # Direzione iniziale del serpente
        self.running = True  # Indica se il gioco è in esecuzione
        self.points = 0  # Punteggio iniziale

        # Disegniamo il serpente sulla canvas
        self.snake_parts = []  # Contiene i riferimenti ai segmenti del serpente
        for segment in self.snake:
            self.snake_parts.append(
                self.canvas.create_rectangle(
                    segment[1]*10, segment[0]*10,  # Coordinate del rettangolo
                    segment[1]*10+10, segment[0]*10+10,  # Misura del rettangolo (10x10 pixel)
                    fill="green"  # Colore del serpente
                )
            )

        # Disegniamo il cibo sulla canvas
        self.food_item = self.canvas.create_oval(
            self.food[1]*10, self.food[0]*10,  # Coordinate dell'ellisse (cibo)
            self.food[1]*10+10, self.food[0]*10+10,  # Misura del cibo (10x10 pixel)
            fill="red"  # Colore del cibo
        )

        # Mostriamo il punteggio iniziale sulla canvas
        self.score_text = self.canvas.create_text(
            300, 10,  # Posizione del punteggio
            fill="white",  # Colore del testo
            text=f"Score: {self.points}"  # Testo mostrato
        )

        # Associare i tasti direzionali alla funzione per cambiare direzione
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))

        # Avvia il ciclo di aggiornamento del gioco
        self.update_game()

    def change_direction(self, new_direction):
        """
        Cambia la direzione del serpente, evitando movimenti opposti (es: su -> giù).
        """
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_direction != opposites.get(self.direction, ""):
            self.direction = new_direction

    def update_game(self):
        """
        Aggiorna lo stato del gioco:
        - Muove il serpente
        - Controlla collisioni (bordo, corpo, cibo)
        - Aggiorna la GUI
        """
        if not self.running:  # Se il gioco è finito, non fare nulla
            return

        # Calcola la nuova posizione della testa del serpente
        head = self.snake[0].copy()  # Copia della testa corrente
        if self.direction == "Up":
            head[0] -= 1  # Muovi la testa verso l'alto
        elif self.direction == "Down":
            head[0] += 1  # Muovi la testa verso il basso
        elif self.direction == "Left":
            head[1] -= 1  # Muovi la testa verso sinistra
        elif self.direction == "Right":
            head[1] += 1  # Muovi la testa verso destra

        # Controllo collisioni: Bordo o corpo del serpente
        if (
            head[0] < 0 or head[0] >= 30 or  # Fuori dai limiti superiori/inferiori
            head[1] < 0 or head[1] >= 60 or  # Fuori dai limiti sinistro/destro
            head in self.snake  # Collisione con sé stesso
        ):
            self.running = False  # Fine del gioco
            self.canvas.create_text(
                300, 150, fill="white", 
                text="Game Over!", font=("Arial", 24)
            )  # Mostra "Game Over" al centro
            return

        # Aggiungi la nuova testa al serpente
        self.snake.insert(0, head)  # La nuova testa diventa il primo elemento
        self.snake_parts.insert(
            0, 
            self.canvas.create_rectangle(
                head[1]*10, head[0]*10,  # Coordinate della nuova testa
                head[1]*10+10, head[0]*10+10,  # Dimensioni
                fill="green"  # Colore della testa
            )
        )

        # Controllo se il serpente mangia il cibo
        if head == self.food:
            self.points += 1  # Incrementa il punteggio
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.points}")  # Aggiorna il punteggio
            # Genera una nuova posizione casuale per il cibo
            self.food = [randint(1, 29), randint(1, 59)]
            self.canvas.coords(
                self.food_item, 
                self.food[1]*10, self.food[0]*10, 
                self.food[1]*10+10, self.food[0]*10+10
            )
        else:
            # Rimuovi l'ultimo segmento del serpente (se non mangia il cibo)
            tail = self.snake.pop()  # Rimuove l'ultimo elemento dalla lista
            self.canvas.delete(self.snake_parts.pop())  # Rimuove l'ultimo segmento dalla canvas

        # Richiama questa funzione ogni 100 ms per continuare il ciclo del gioco
        self.root.after(100, self.update_game)

# Creazione della finestra principale e avvio del gioco
root = tk.Tk()  # Finestra principale di tkinter
game = SnakeGame(root)  # Crea un'istanza del gioco
root.mainloop()  # Avvia il loop principale dell'applicazione
