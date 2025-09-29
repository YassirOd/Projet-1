import tkinter as tk
from quiz import QuizJeu, charger_questions

class Menu:
    def __init__(self, root, pseudo=None, score=None):
        self.root = root
        self.root.title("Quiz")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(0, 0, 800, 600, fill="#4C5B61", outline="")

        # Titre
        self.canvas.create_text(400, 80, text="Bienvenue au Quiz",
                                font=("Arial", 36, "bold"), fill="white")

        # Affichage du dernier score
        if pseudo and score is not None:
            self.canvas.create_text(400, 140,
                text=f"Dernier score de {pseudo} : {score} points",
                font=("Arial", 20, "bold"), fill="red")

        # Pseudo
        self.canvas.create_text(400, 180, text="Entrez votre pseudo :",
                                font=("Arial", 20), fill="white")
        self.pseudo_entry = tk.Entry(root, font=("Arial", 18), justify="center")
        self.canvas.create_window(400, 220, window=self.pseudo_entry, width=300)

        # Niveau de difficulté
        self.canvas.create_text(400, 270, text="Choisissez le niveau de difficulté :",
                                font=("Arial", 16), fill="white")
        self.difficulty_var = tk.StringVar(value="facile")
        niveaux = [("Facile", "facile"), ("Moyen", "moyen"), ("Difficile", "difficile")]
        y = 300
        for texte, valeur in niveaux:
            rb = tk.Radiobutton(root, text=texte, variable=self.difficulty_var,
                                value=valeur, font=("Arial", 14),
                                bg="#4C5B61", fg="white", selectcolor="#FF6F61",
                                activebackground="#4C5B61", activeforeground="white")
            self.canvas.create_window(400, y, window=rb)
            y += 30

        # Bouton Lancer quiz
        start_btn = tk.Button(root, text="Lancer le Quiz",
                              font=("Arial", 18, "bold"),
                              bg="#FF6F61", fg="white",
                              activebackground="#FF856D",
                              activeforeground="white",
                              command=self.lancer_quiz,
                              relief="raised", bd=4)
        self.canvas.create_window(400, 440, window=start_btn, width=250, height=70)

        # Bouton Quitter
        quit_btn = tk.Button(root, text="Quitter",
                             font=("Arial", 16, "bold"),
                             bg="#555555", fg="white",
                             activebackground="#777777",
                             activeforeground="white",
                             command=root.destroy,
                             relief="raised", bd=3)
        self.canvas.create_window(400, 520, window=quit_btn, width=180, height=60)

    def lancer_quiz(self):
        pseudo = self.pseudo_entry.get().strip()
        if not pseudo:
            pseudo = "Joueur"

        # choisir le fichier csv en fonction du niveau
        niveau = self.difficulty_var.get()
        if niveau == "facile":
            fichier = "qst_facile.csv"
        elif niveau == "moyen":
            fichier = "qst_moyen.csv"
        else:
            fichier = "qst_difficile.csv"

        questions = charger_questions(fichier)

        self.root.destroy()
        root_quiz = tk.Tk()
        app = QuizJeu(root_quiz, questions, pseudo)
        root_quiz.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    menu = Menu(root)
    root.mainloop()
