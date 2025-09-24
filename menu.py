import tkinter as tk
from quiz import QuizJeu, charger_questions

class Menu:
    def __init__(self, root, pseudo=None, score=None):
        self.root = root
        self.root.title("Quiz")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Canvas pour le fond
        self.canvas = tk.Canvas(root, width=500, height=400)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_rectangle(0, 0, 500, 400, fill="#4C5B61", outline="")

        # Titre
        self.canvas.create_text(250, 50, text="Bienvenue au Quiz", font=("Arial", 24, "bold"), fill="white")

        # Affichage du dernier score si disponible
        if pseudo and score is not None:
            self.canvas.create_text(250, 90,
                text=f"Dernier score de {pseudo} : {score}",
                font=("Arial", 14), fill="red")

        # Pseudo
        self.canvas.create_text(250, 130, text="Entrez votre pseudo :", font=("Arial", 14), fill="white")
        self.pseudo_entry = tk.Entry(root, font=("Arial", 14), justify="center")
        self.canvas.create_window(250, 160, window=self.pseudo_entry, width=200)

        # Bouton Lancer le quiz
        start_btn = tk.Button(root, text="Lancer le Quiz", font=("Arial", 14, "bold"),
                              bg="#FF6F61", fg="white", activebackground="#FF856D",
                              activeforeground="white", command=self.lancer_quiz, relief="raised", bd=3)
        self.canvas.create_window(250, 250, window=start_btn, width=200, height=50)

        # Bouton Quitter
        quit_btn = tk.Button(root, text="Quitter", font=("Arial", 12, "bold"),
                             bg="#555555", fg="white", activebackground="#777777",
                             activeforeground="white", command=root.destroy, relief="raised", bd=2)
        self.canvas.create_window(250, 320, window=quit_btn, width=120, height=40)

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
