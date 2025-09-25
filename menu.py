import tkinter as tk
from quiz import QuizJeu, charger_questions

class Menu:
    def __init__(self, root, pseudo=None, score=None):
        self.root = root
        self.root.title("Quiz")
        self.root.geometry("800x600")
        self.root.resizable(False, False)


        # Canvas pour le fond
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(0, 0, 800, 600, fill="#4C5B61", outline="")

        # Titre
        self.canvas.create_text(400, 80, text="Bienvenue au Quiz",
                                font=("Arial", 36, "bold"), fill="white")


        # Affichage du dernier score si disponible
        if pseudo and score is not None:
            self.canvas.create_text(400, 140,
                text=f"Dernier score de {pseudo} : {score} points",
                font=("Arial", 20, "bold"), fill="red")

        # Pseudo
        self.canvas.create_text(400, 220, text="Entrez votre pseudo :",
                                font=("Arial", 20), fill="white")
        self.pseudo_entry = tk.Entry(root, font=("Arial", 18), justify="center")
        self.canvas.create_window(400, 260, window=self.pseudo_entry, width=300)

        # Bouton Lancer le quiz
        start_btn = tk.Button(root, text="Lancer le Quiz",
                              font=("Arial", 18, "bold"),
                              bg="#FF6F61", fg="white",
                              activebackground="#FF856D",
                              activeforeground="white",
                              command=self.lancer_quiz,
                              relief="raised", bd=4)
        self.canvas.create_window(400, 360, window=start_btn, width=250, height=70)

        # Bouton Quitter
        quit_btn = tk.Button(root, text="Quitter",
                             font=("Arial", 16, "bold"),
                             bg="#555555", fg="white",
                             activebackground="#777777",
                             activeforeground="white",
                             command=root.destroy,
                             relief="raised", bd=3)
        self.canvas.create_window(400, 460, window=quit_btn, width=180, height=60)

    def lancer_quiz(self):
        pseudo = self.pseudo_entry.get().strip()
        if not pseudo:
            pseudo = "Joueur"

        questions = charger_questions("questions.csv")

        self.root.destroy()
        root_quiz = tk.Tk()
        app = QuizJeu(root_quiz, questions, pseudo)
        root_quiz.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()
