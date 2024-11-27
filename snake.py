import tkinter as tk  # Importiamo la libreria tkinter per creare la GUI
from random import randint  # Importiamo randint per generare posizioni casuali
from PIL import Image, ImageTk  # Importiamo Image e ImageTk per caricare immagini
import pygame  # Aggiungiamo pygame per la gestione dell'audio


# Classe principale per il gioco Snake
class SnakeGame:
    def __init__(self, root):
        # Configurazione della finestra principale
        self.root = root
        self.root.title("Snake Game")  # Titolo della finestra
        # Inizializza pygame per gestire l'audio
        pygame.mixer.init()
        # Variabile per la pausa
        self.paused = False  # Indica se il gioco è in pausa
        # Associa il tasto P per mettere in pausa
        self.root.bind("<p>", self.toggle_pause)
        # Configura il menu
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        # Aggiungi un menu per il gioco
        game_menu = tk.Menu(self.menu, tearoff=0)
        game_menu.add_command(label="Pause", command=self.pause_game)
        game_menu.add_command(label="Resume", command=self.resume_game)
        self.menu.add_cascade(label="Game", menu=game_menu)
        # Carica l'effetto sonoro (modifica con il path del tuo file audio)
        self.eat_sound = pygame.mixer.Sound(
            "music/mouse_s.wav"
        )  # Sostituisci con il percorso del file audio
        self.main_theme = pygame.mixer.Sound(
            "music/main_theme.wav"
        )  # Sostituisci con il percorso del file audio
        self.main_theme.play(-1)
        # Carica l'immagine di sfondo
        self.background_image = Image.open(
            "img/grass.jpg"
        )  # Sostituisci con il path dell'immagine
        self.background_image = self.background_image.resize(
            (600, 300)
        )  # Ridimensiona l'immagine a 600x300
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        # Canvas (area di gioco): 600x300 pixel
        self.canvas = tk.Canvas(root, width=600, height=300)
        self.canvas.pack()
        # Aggiungi l'immagine come sfondo
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)
        # Carica l'immagine del serpente
        self.snake_image = Image.open(
            "img/snake.png"
        )  # Sostituisci con il path dell'immagine
        self.snake_image = self.snake_image.resize(
            (10, 10)
        )  # Ridimensiona l'immagine a 10x10 pixel
        self.snake_photo = ImageTk.PhotoImage(self.snake_image)
        # Carica l'immagine del cibo
        self.food_image = Image.open(
            "img/mouse-.png"
        )  # Sostituisci con il path dell'immagine del cibo
        self.food_image = self.food_image.resize(
            (10, 10)
        )  # Ridimensiona l'immagine a 10x10 pixel
        self.food_photo = ImageTk.PhotoImage(self.food_image)
        # Stato iniziale del gioco
        self.snake = [[15, 13], [15, 12], [15, 11]]  # Coordinate iniziali del serpente
        self.food = [
            randint(1, 29),
            randint(1, 59),
        ]  # Posizione iniziale del cibo (casuale)
        self.direction = "Right"  # Direzione iniziale del serpente
        self.running = True  # Indica se il gioco è in esecuzione
        self.points = 0  # Punteggio iniziale
        # Disegniamo il serpente sulla canvas con l'immagine
        self.snake_parts = []  # Contiene i riferimenti ai segmenti del serpente
        for segment in self.snake:
            self.snake_parts.append(
                self.canvas.create_image(
                    segment[1] * 10,
                    segment[0] * 10,  # Coordinate dell'immagine del serpente
                    anchor="nw",  # Ancoraggio per la posizione
                    image=self.snake_photo,  # Usa l'immagine del serpente
                )
            )
        # Disegniamo il cibo sulla canvas con l'immagine
        self.food_item = self.canvas.create_image(
            self.food[1] * 10,
            self.food[0] * 10,  # Coordinate x e y
            anchor="nw",  # L'ancoraggio in alto a sinistra
            image=self.food_photo,  # L'immagine del cibo
        )
        # Mostriamo il punteggio iniziale sulla canvas
        self.score_text = self.canvas.create_text(
            30,
            10,  # Posizione del punteggio
            fill="white",  # Colore del testo
            text=f"Score: {self.points}",  # Testo mostrato
        )
        # Associare i tasti direzionali alla funzione per cambiare direzione
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        # Aggiungere il tasto per riavviare il gioco
        self.root.bind("r", self.restart_game)
        # Avvia il ciclo di aggiornamento del gioco
        self.update_game()

    def change_direction(self, new_direction):
        """
        Cambia la direzione del serpente, evitando movimenti opposti (es: su -> giù).
        """
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_direction != opposites.get(self.direction, ""):
            self.direction = new_direction

    def toggle_pause(self, event=None):
        """
        Alterna tra pausa e ripresa del gioco premendo il tasto P.
        """
        if not self.paused:
            self.pause_game()
        else:
            self.resume_game()

    def pause_game(self):
        """
        Mette in pausa il gioco e mostra una finestra al centro dello schermo.
        """
        if not self.paused:
            self.paused = True  # Metti in pausa il gioco
            # Mostra una finestra di pausa
            self.pause_window = tk.Toplevel(self.root)
            self.pause_window.title("Pause")
            # Ottieni le dimensioni e la posizione della finestra principale
            window_width = self.root.winfo_width()
            window_height = self.root.winfo_height()
            window_x = self.root.winfo_x()
            window_y = self.root.winfo_y()
    
            # Calcola la posizione centrale della finestra di pausa
            pause_width = 300  # Larghezza della finestra di pausa
            pause_height = 150  # Altezza della finestra di pausa
            center_x = window_x + (window_width // 2) - (pause_width // 2)
            center_y = window_y + (window_height // 2) - (pause_height // 2)
            self.pause_window.transient(self.root)  # Modalità finestra figlia
            self.pause_window.grab_set()  # Blocca il focus sulla finestra di pausa
            # Aggiungi un messaggio o altri widget nella finestra
            tk.Label(self.pause_window, text="Game Paused", font=("Arial", 18)).pack(
                pady=20
            )
            # Bottone per chiudere la finestra di pausa
            tk.Button(self.pause_window, text="Resume", command=self.resume_game).pack(
                pady=10
            )

    def resume_game(self):
        """
        Riprende il gioco dalla pausa.
        """
        if self.paused:
            self.paused = False  # Riprendi il gioco
            # Chiudi la finestra di pausa, se esiste
            if hasattr(self, "pause_window"):
                self.pause_window.destroy()
            # Avvia il ciclo di aggiornamento se necessario
            self.update_game()

    def update_game(self):
        """
        Aggiorna lo stato del gioco:
        - Muove il serpente
        - Controlla collisioni (bordo, corpo, cibo)
        - Aggiorna la GUI
        """
        if not self.running or self.paused:  # Se il gioco è finito, non fare nulla
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
            head[0] < 0
            or head[0] >= 30  # Fuori dai limiti superiori/inferiori
            or head[1] < 0
            or head[1] >= 60  # Fuori dai limiti sinistro/destro
            or head in self.snake  # Collisione con sé stesso
        ):
            self.running = False  # Fine del gioco
            self.canvas.create_text(
                300, 150, fill="white", text="Game Over!", font=("Arial", 24)
            )  # Mostra "Game Over" al centro
            return
        # Aggiungi la nuova testa al serpente
        self.snake.insert(0, head)  # La nuova testa diventa il primo elemento
        self.snake_parts.insert(
            0,
            self.canvas.create_image(
                head[1] * 10,
                head[0] * 10,  # Coordinate della nuova testa
                anchor="nw",  # Ancoraggio
                image=self.snake_photo,  # Usa l'immagine per il segmento
            ),
        )
        # Controllo se il serpente mangia il cibo
        if head == self.food:
            self.points += 1  # Incrementa il punteggio
            self.canvas.itemconfig(
                self.score_text, text=f"Score: {self.points}"
            )  # Aggiorna il punteggio
            # Genera una nuova posizione casuale per il cibo
            self.food = [randint(1, 29), randint(1, 59)]
            # Riproduci il suono quando il serpente mangia il cibo
            self.eat_sound.play()  # Suona l'effetto sonoro
            # Usa solo 2 coordinate per l'immagine del cibo
            self.canvas.coords(
                self.food_item, self.food[1] * 10, self.food[0] * 10
            )  # x, y
        else:
            # Rimuovi l'ultimo segmento del serpente (se non mangia il cibo)
            tail = self.snake.pop()  # Rimuove l'ultimo elemento dalla lista
            self.canvas.delete(
                self.snake_parts.pop()
            )  # Rimuove l'ultimo segmento dalla canvas
        # Richiama questa funzione ogni 100 ms per continuare il ciclo del gioco
        self.root.after(100, self.update_game)

    def restart_game(self, event=None):
        """
        Resetta il gioco per farlo ripartire.
        """
        # Cancella tutti gli oggetti dalla canvas
        self.canvas.delete("all")
        # Re-inizializza lo stato del gioco
        self.snake = [[15, 13], [15, 12], [15, 11]]
        self.food = [randint(1, 29), randint(1, 59)]
        self.direction = "Right"
        self.running = True
        self.points = 0
        # Ripristina lo sfondo e il punteggio
        self.canvas.create_image(0, 0, anchor="nw", image=self.background_photo)
        self.score_text = self.canvas.create_text(
            30, 10, fill="white", text=f"Score: {self.points}"
        )
        # Ricrea il serpente e il cibo
        self.snake_parts = []
        for segment in self.snake:
            self.snake_parts.append(
                self.canvas.create_image(
                    segment[1] * 10,
                    segment[0] * 10,
                    anchor="nw",
                    image=self.snake_photo,
                )
            )
        self.food_item = self.canvas.create_image(
            self.food[1] * 10, self.food[0] * 10, anchor="nw", image=self.food_photo
        )
        # Avvia di nuovo il ciclo di gioco
        self.update_game()


# Creazione della finestra principale e avvio del gioco
root = tk.Tk()  # Finestra principale di tkinter
game = SnakeGame(root)  # Crea un'istanza del gioco
root.mainloop()  # Avvia il loop principale dell'applicazione
