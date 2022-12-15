
# Importer les bibliothèques
import random
import math

# Créer la classe Othello
class Othello:
    # Initialiser le jeu
    def __init__(self):
        self.game_state = [[' '] * 8 for _ in range(8)]  # initialise la grille de jeu
        self.game_state[3][3] = 'W'  # place le pion blanc en (3,3)
        self.game_state[3][4] = 'B'  # place le pion noir en (3,4)
        self.game_state[4][3] = 'B'  # place le pion noir en (4,3)
        self.game_state[4][4] = 'W'  # place le pion blanc en (4,4)

        self.current_player = 'B'  # initialise le joueur courant

        self.valid_moves = self.get_valid_moves()  # initialise les mouvements valides

    # Trouver les mouvements valides
    def get_valid_moves(self):
        valid_moves = []
        for row in range(8):
            for col in range(8):
                if self.game_state[row][col] == ' ':  # si la case est vide
                    # Vérifier si le mouvement est valide
                    if self.is_valid_move(row, col):
                        valid_moves.append((row, col))
        return valid_moves

    # Vérifier si le mouvement est valide
    def is_valid_move(self, row, col):
        # Vérifier s'il existe des pions adjacents de l'autre couleur
        if not self.has_adjacent_opponent_pieces(row, col):
            return False

        # Vérifier s'il existe des pions de la même couleur à capturer
        if not self.has_capturable_pieces(row, col):
            return False

        return True

    # Vérifier s'il existe des pions adjacents de l'autre couleur
    def has_adjacent_opponent_pieces(self, row, col):
        # Vérifier les cases adjacentes
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Ne pas vérifier la case elle-même
                if i == 0 and j == 0:
                    continue

                # Vérifier si la case existe
                if not self.is_in_board(row + i, col + j):
                    continue

                # Vérifier si la case est occupée par un pion de l'autre couleur
                if self.game_state[row + i][col + j] == self.get_opponent_player():
                    return True

        return False

    # Vérifier s'il existe des pions de la même couleur à capturer
    def has_capturable_pieces(self, row, col):
        # Vérifier les cases adjacentes
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Ne pas vérifier la case elle-même
                if i == 0 and j == 0:
                    continue

                # Vérifier si la case existe
                if not self.is_in_board(row + i, col + j):
                    continue

                # Vérifier si la case est occupée par un pion de la même couleur
                if self.game_state[row + i][col + j] == self.current_player:
                    # Vérifier si les pions peuvent être capturés
                    if self.can_capture_pieces(row, col, row + i, col + j):
                        return True

        return False

    # Vérifier si la case est dans le plateau
    def is_in_board(self, row, col):
        if row < 0 or row >= 8 or col < 0 or col >= 8:
            return False
        return True

    # Obtenir le joueur opposé
    def get_opponent_player(self):
        if self.current_player == 'B':
            return 'W'
        else:
            return 'B'

    # Vérifier si les pions peuvent être capturés
    def can_capture_pieces(self, row1, col1, row2, col2):
        # Calcule le vecteur entre les deux cases
        dir_row = row2 - row1
        dir_col = col2 - col1

        # Vérifier si le vecteur reste dans le plateau
        if not self.is_in_board(row2 + dir_row, col2 + dir_col):
            return False

        # Vérifier si la case suivante est occupée par un pion de l'autre couleur
        if self.game_state[row2 + dir_row][col2 + dir_col] != self.get_opponent_player():
            return False

        # Vérifier si la case suivante est vide
        if self.game_state[row2 + dir_row][col2 + dir_col] != ' ':
            return False

        # Les pions peuvent être capturés
        return True

    # Jouer un mouvement
    def play_move(self, row, col):
        # Met à jour le jeu
        self.update_game_state(row, col)

        # Met à jour le joueur courant
        self.current_player = self.get_opponent_player()

        # Met à jour les mouvements valides
        self.valid_moves = self.get_valid_moves()

    # Met à jour le jeu
    def update_game_state(self, row, col):
        # Placer le pion du joueur courant
        self.game_state[row][col] = self.current_player

        # Capturer les pions
        self.capture_pieces(row, col)

    # Capturer les pions
    def capture_pieces(self, row, col):
        # Vérifier les cases adjacentes
        for i in range(-1, 2):
            for j in range(-1, 2):
                # Ne pas vérifier la case elle-même
                if i == 0 and j == 0:
                    continue

                # Vérifier si la case existe
                if not self.is_in_board(row + i, col + j):
                    continue

                # Vérifier si la case est occupée par un pion de l'autre couleur
                if self.game_state[row + i][col + j] == self.get_opponent_player():
                    # Vérifier si les pions peuvent être capturés
                    if self.can_capture_pieces(row, col, row + i, col + j):
                        # Capturer les pions
                        self.capture_pieces(row + i, col + j)

                        # Placer le pion du joueur courant
                        self.game_state[row + i][col + j] = self.current_player

    # Afficher le jeu
    def print_game_state(self):
        for row in self.game_state:
            for col in row:
                print(col, end=' ')
            print()
        print()

# Créer la classe MCTS
class MCTS:
    # Initialiser l'algorithme
    def __init__(self):
        self.visit_count = {}  # compte les visites
        self.win_count = {}  # compte les gains

    # Choisir le meilleur mouvement
    def choose_best_move(self, othello):
        valid_moves = othello.valid_moves

        # Initialiser le compte des visites et des gains
        for move in valid_moves:
            self.visit_count[move] = 0
            self.win_count[move] = 0

        # Simuler le jeu
        for _ in range(1000):
            self.simulate_random_game(othello)

        # Obtenir le meilleur mouvement
        best_move = None
        best_win_ratio = -1
        for move in valid_moves:
            win_ratio = self.win_count[move] / self.visit_count[move]
            if win_ratio > best_win_ratio:
                best_move = move
                best_win_ratio = win_ratio

        return best_move

    # Simuler un jeu aléatoire
    def simulate_random_game(self, othello):
        # Copier l'état du jeu
        cur_game_state = [[col for col in row] for row in othello.game_state]
        cur_player = othello.current_player
        cur_valid_moves = list(othello.valid_moves)

        # Simuler le jeu
        while cur_valid_moves:
            # Choisir un mouvement aléatoire
            move = random.choice(cur_valid_moves)

            # Mettre à jour le compte des visites
            self.visit_count[move] += 1

            # Jouer le mouvement
            othello.play_move(move[0], move[1])

            # Vérifier si le joueur courant a gagné
            if othello.valid_moves == []:
                if othello.current_player == cur_player:
                    # Mettre à jour le compte des gains
                    self.win_count[move] += 1
                break

            # Réinitialiser l'état du jeu
            othello.game_state = cur_game_state
            othello.current_player = cur_player
            othello.valid_moves = cur_valid_moves

# Créer une partie d'othello
othello = Othello()

# Créer un algorithme MCTS
mcts = MCTS()

# Boucle de jeu
while othello.valid_moves:
    # Afficher l'état du jeu
    othello.print_game_state()

    if othello.current_player == 'B':
        # Choisir le meilleur mouvement
        row, col = mcts.choose_best_move(othello)
        print('MCTS joue ({},{})'.format(row, col))
    else:
        # Demander à l'utilisateur de jouer
        row = int(input('Entrez la ligne : '))
        col = int(input('Entrez la colonne : '))

    # Jouer le mouvement
    othello.play_move(row, col)

# Afficher le jeu
othello.print_game_state()

# Afficher le gagnant
if othello.valid_moves == []:
    if othello.current_player == 'B':
        print('MCTS a gagné!')
    else:
        print('Vous avez gagné!')