import tkinter as tk
import csv

class QuizJeu:
    def __init__(self, root, questions, pseudo="Joueur"):
        self.root = root
        self.root.title(f"Quiz - {pseudo}")

        self.pseudo = pseudo
        self.questions = questions
        self.index_question = 0
        self.score = 0
        self.en_attente = False

        self.canvas = tk.Canvas(root, width=600, height=600, bg="white")
        self.canvas.pack()

        self.blocs = {
            "Haut-Gauche": self.canvas.create_rectangle(50, 50, 200, 150, fill="lightgreen"),
            "Haut-Droite": self.canvas.create_rectangle(400, 50, 550, 150, fill="lightcoral"),
            "Bas-Gauche": self.canvas.create_rectangle(50, 450, 200, 550, fill="lightblue"),
            "Bas-Droite": self.canvas.create_rectangle(400, 450, 550, 550, fill="khaki"),
        }

        self.texte_reponses = {
            "Haut-Gauche": self.canvas.create_text(125, 100, text="", font=("Arial", 12, "bold")),
            "Haut-Droite": self.canvas.create_text(475, 100, text="", font=("Arial", 12, "bold")),
            "Bas-Gauche": self.canvas.create_text(125, 500, text="", font=("Arial", 12, "bold")),
            "Bas-Droite": self.canvas.create_text(475, 500, text="", font=("Arial", 12, "bold")),
        }

        self.zone_question = self.canvas.create_rectangle(150, 250, 450, 350, fill="lightgrey")
        self.texte_question = self.canvas.create_text(300, 300, text="", font=("Arial", 14, "bold"), width=250)
        self.texte_feedback = self.canvas.create_text(300, 370, text="", font=("Arial", 12, "italic"), fill="darkblue")
        self.balle = self.canvas.create_oval(280, 280, 320, 320, fill="blue")

        self.canvas.tag_lower(self.zone_question)
        self.canvas.tag_raise(self.texte_question)
        self.canvas.tag_raise(self.balle)

        self.afficher_question()

        self.root.bind("<Left>", self.gauche)
        self.root.bind("<Right>", self.droite)
        self.root.bind("<Up>", self.haut)
        self.root.bind("<Down>", self.bas)
        self.root.bind("<Return>", self.question_suivante)
        self.root.bind("<space>", self.question_suivante)

    def afficher_question(self):
        q = self.questions[self.index_question]
        self.canvas.itemconfig(self.texte_question, text=q["question"])
        self.canvas.itemconfig(self.texte_feedback, text="")
        reponses = [q["reponse1"], q["reponse2"], q["reponse3"], q["reponse4"]]
        for bloc, texte in zip(self.texte_reponses.keys(), reponses):
            self.canvas.itemconfig(self.texte_reponses[bloc], text=texte)
        self.en_attente = False

    def gauche(self, event):
        if not self.en_attente: self.deplacer(-20, 0)
    def droite(self, event):
        if not self.en_attente: self.deplacer(20, 0)
    def haut(self, event):
        if not self.en_attente: self.deplacer(0, -20)
    def bas(self, event):
        if not self.en_attente: self.deplacer(0, 20)

    def deplacer(self, dx, dy):
        self.canvas.move(self.balle, dx, dy)
        self.check_collision()

    def check_collision(self):
        balle_coords = self.canvas.bbox(self.balle)
        for nom, bloc in self.blocs.items():
            if self.collision(balle_coords, self.canvas.bbox(bloc)):
                self.verifier_reponse(nom)

    def collision(self, bbox1, bbox2):
        return not (bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or
                    bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3])

    def verifier_reponse(self, bloc_nom):
        q = self.questions[self.index_question]
        if bloc_nom == q["bonne"]:
            self.score += 1
            self.canvas.itemconfig(self.texte_feedback, text="Bonne réponse", fill="green")
        else:
            self.canvas.itemconfig(self.texte_feedback, text="Mauvaise réponse", fill="red")
        self.en_attente = True

    def question_suivante(self, event=None):
        if not self.en_attente:
            return
        self.index_question += 1
        if self.index_question < len(self.questions):
            self.canvas.coords(self.balle, 280, 280, 320, 320)
            self.afficher_question()
        else:
            self.canvas.itemconfig(self.texte_question, text=f"{self.pseudo} - Score final: {self.score}/{len(self.questions)}")
            for bloc in self.texte_reponses.values():
                self.canvas.itemconfig(bloc, text="")
            self.canvas.itemconfig(self.texte_feedback, text="")

            self.bouton_menu = tk.Button(self.root, text="Menu", font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", command=self.retour_menu)
            self.canvas.create_window(200, 400, window=self.bouton_menu, width=150, height=60)

            self.bouton_quitter = tk.Button(self.root, text="Quitter", font=("Arial", 12, "bold"), bg="#F44336", fg="white", command=self.root.destroy)
            self.canvas.create_window(400, 400, window=self.bouton_quitter, width=150, height=60)

    def retour_menu(self):
        import menu
        self.root.destroy()
        root_menu = tk.Tk()
        app_menu = menu.Menu(root_menu, self.pseudo, self.score)
        root_menu.mainloop()

def charger_questions(fichier_csv):
    questions = []
    with open(fichier_csv, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            questions.append(row)
    return questions

if __name__ == "__main__":
    questions = charger_questions("questions.csv")
    root = tk.Tk()
    app = QuizJeu(root, questions)
    root.mainloop()
