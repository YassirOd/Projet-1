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
        self.streak = 0
        self.en_attente = False

        self.canvas = tk.Canvas(root, width=600, height=600, bg="#f0ede9")
        self.canvas.pack()

        #zone réponse
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
        #zone question
        self.zone_question = self.canvas.create_rectangle(150, 250, 450, 350, fill="lightgrey")

        #Tous les textes
        self.texte_question = self.canvas.create_text(300, 300, text="", font=("Arial", 14, "bold"), width=250)
        self.texte_feedback = self.canvas.create_text(300, 370, text="", font=("Arial", 12, "italic"))
        self.texte_suivant = self.canvas.create_text(300, 420, text="", font=("Arial", 9, "italic"), fill="grey")
        self.balle = self.canvas.create_oval(280, 280, 320, 320, fill="#031d40")
        self.flame = self.canvas.create_text(300, 500, text="", font=("Arial", 35), fill="orange")
        self.texte_streak = self.canvas.create_text(320, 520, text="", font=("Impact", 11, "italic"),fill="orange")


        #Hauteur
        self.canvas.tag_lower(self.zone_question)
        self.canvas.tag_raise(self.texte_question)
        self.canvas.tag_raise(self.balle)
        self.canvas.tag_lower(self.flame)


        self.root.bind("<Left>", self.gauche)
        self.root.bind("<Right>", self.droite)
        self.root.bind("<Up>", self.haut)
        self.root.bind("<Down>", self.bas)
        self.root.bind("<a>", self.gauche)
        self.root.bind("<d>", self.droite)
        self.root.bind("<w>", self.haut)
        self.root.bind("<s>", self.bas)
        self.root.bind("<Return>", self.question_suivante)
        self.root.bind("<space>", self.question_suivante)


        # Zone score
        self.texte_score = self.canvas.create_text(
            300, 100,
            text=f"SCORE",
            font=("Impact", 15, "italic", ),
            fill="Black"
        )
        self.canvas.tag_lower(self.texte_score)

        # Appel de la méthode
        self.afficher_question()

    #Méthode pour afficher les questions
    def afficher_question(self):
        q = self.questions[self.index_question]
        self.canvas.itemconfig(self.texte_question, text=q["question"])
        self.canvas.itemconfig(self.texte_feedback, text="")
        self.canvas.itemconfig(self.texte_suivant, text="")
        reponses = [q["reponse1"], q["reponse2"], q["reponse3"], q["reponse4"]]
        for bloc, texte in zip(self.texte_reponses.keys(), reponses):
            self.canvas.itemconfig(self.texte_reponses[bloc], text=texte)
        self.en_attente = False


    #Méthodes pour gérer le déplacement de la balle
    def gauche(self, event):
        if not self.en_attente: self.deplacer(-35, 0)
    def droite(self, event):
        if not self.en_attente: self.deplacer(35, 0)
    def haut(self, event):
        if not self.en_attente: self.deplacer(0, -35)
    def bas(self, event):
        if not self.en_attente: self.deplacer(0, 35)

    def deplacer(self, dx, dy):
        self.canvas.move(self.balle, dx, dy)
        self.check_collision()

    # Méthode pour vérifier si la balle est rentrer en contact avec les rectangles(bloc)
    def check_collision(self):
        balle_coords = self.canvas.bbox(self.balle)
        for nom, bloc in self.blocs.items():
            if self.collision(balle_coords, self.canvas.bbox(bloc)):
                self.verifier_reponse(nom)

    def collision(self, bbox1, bbox2):
        return not (bbox1[2] < bbox2[0] or bbox1[0] > bbox2[2] or
                    bbox1[3] < bbox2[1] or bbox1[1] > bbox2[3])

    #Méthode pour vérifier les réponses
    def verifier_reponse(self, bloc_nom):
        q = self.questions[self.index_question]
        if bloc_nom == q["bonne"]:
            self.streak += 1
            # streak actif seulement à partir de 2 bonnes réponses consécutives
            points = 5
            if self.streak == 2:
                points = 6
            elif self.streak == 3:
                self.canvas.itemconfig(self.texte_streak, text="+2")
                points = 7
            elif self.streak == 4:
                self.canvas.itemconfig(self.texte_streak, text="+3")
                points = 8
            elif self.streak == 5:
                self.canvas.itemconfig(self.texte_streak, text="+4")
                points = 9
            elif self.streak >= 6:
                self.canvas.itemconfig(self.texte_streak, text="+5")
                self.canvas.itemconfig(self.balle, fill="orange")
                points = 10

            if self.streak >= 2:
                self.canvas.itemconfig(self.flame, text="🔥")
            else:
                self.canvas.itemconfig(self.flame, text="")
            self.score += points
            self.canvas.itemconfig(self.texte_feedback, text=f"Bonne réponse ! +{points} pts", fill="green")

        else:
            # mauvaise réponse
            message = "Mauvaise réponse"
            if self.streak >= 2:
                message += ", fin du streak"
            self.canvas.itemconfig(self.texte_feedback, text=message, fill="red")
            self.streak = 0
            self.canvas.itemconfig(self.flame, text="")  # enlève flamme
            self.canvas.itemconfig(self.balle, fill="#031d40")
            self.canvas.itemconfig(self.texte_streak, text="")

        self.canvas.itemconfig(self.texte_suivant,
                               text=f"Appuyez sur ESPACE ou ENTRÉE pour passer à la question suivante.")
        self.en_attente = True
        self.canvas.itemconfig(self.texte_score, text=f"{self.score} points")

    # Méthode pour rejouer
    def rejouer(self):
        self.root.destroy()
        root_new = tk.Tk()
        app_new = QuizJeu(root_new, self.questions, self.pseudo)
        root_new.mainloop()

    # Méthode pour passer à la question suivante et pour mettre fin au quiz
    def question_suivante(self, event=None):
        if not self.en_attente:
            return
        self.index_question += 1
        if self.index_question < len(self.questions):
            self.canvas.coords(self.balle, 280, 280, 320, 320)
            self.afficher_question()
        else:
            self.canvas.itemconfig(self.texte_question, text=f"{self.pseudo}\nScore final: {self.score} points",font=("Impact", 18, "italic"), fill="red")
            for bloc in self.texte_reponses.values():
                self.canvas.itemconfig(bloc, text="")
            self.canvas.itemconfig(self.texte_feedback, text="")
            self.canvas.itemconfig(self.flame, text="")
            self.canvas.itemconfig(self.texte_suivant, text="")
            self.canvas.itemconfig(self.texte_streak, text="")

            self.bouton_menu = tk.Button(self.root, text="Menu", font=("Arial", 12, "bold"), bg="#01045e", fg="white", command=self.retour_menu)
            self.canvas.create_window(100, 400, window=self.bouton_menu, width=120, height=40)

            self.bouton_rejouer = tk.Button(self.root, text="Rejouer",font=("Arial", 12, "bold"),bg="#4CAF50", fg="white",command=lambda: self.rejouer())
            self.canvas.create_window(300, 400, window=self.bouton_rejouer, width=120, height=40)

            self.bouton_quitter = tk.Button(self.root, text="Quitter", font=("Arial", 12, "bold"), bg="#F44336", fg="white", command=self.root.destroy)
            self.canvas.create_window(500, 400, window=self.bouton_quitter, width=120, height=40)
            for bloc in self.blocs.values():
                self.canvas.itemconfig(bloc, fill="grey")

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
    # Par défaut lance le quiz facile si on ne passe pas par le menu
    questions = charger_questions("qst_facile.csv")
    root = tk.Tk()
    app = QuizJeu(root, questions)
    root.mainloop()
