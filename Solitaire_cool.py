# Assignment COMPSCI130
# Section 5 - Creative Extension
# Name: Lee-Anne Morris
# UPI: lmor867

class Solitaire:
    def __init__(self, cards):
        self.piles = []
        self.num_cards = len(cards)
        self.num_piles = (self.num_cards // 8) + 3
        self.max_num_moves = self.num_cards * 2
        self.past_scores = []
        self.move_history = []
        self.round_counter = 1
        self.hints = 0
        self.highscore = 0
        self.spaces = sum(len(str(card)) for card in cards)
        for i in range(self.num_piles):
            self.piles.append(CardPile())
        for i in range(self.num_cards):
            self.piles[0].add_bottom(cards[i])

    def introduction(self):
        stylised_letters = "𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳𝐀𝐁𝐂𝐃𝐄𝐅𝐆𝐇𝐈𝐉𝐊𝐋𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙𝐚𝐛𝐜𝐝𝐞𝐟𝐠𝐡𝐢𝐣𝐤𝐥𝐦𝐧𝐨𝐩𝐪𝐫𝐬𝐭𝐮𝐯𝐰𝐱𝐲𝐳@#$%^&*()-+=_[]{}\/?~`';:|<>,.! 123456789"
        alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%^&*()-+=_[]{}\/?~`';:|<>,.! 123456789"
        if self.round_counter == 1:
            name = str(input("Enter your name: "))
            stylised_name = ""
            for letter in name:
                index = alphabet.find(letter)
                stylised_name += stylised_letters[index]   
            print(f"✩░▒▓▆▅▃▂▁𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐒𝐨𝐥𝐢𝐭𝐚𝐫𝐞 {stylised_name}!▁▂▃▅▆▓▒░✩")
            print()
            rules = str(input("Read rules (y/n)? "))
            
            while not self.check_valid(rules):
                rules = input(f"'{rules}' is not y or n. Please enter either (y/n): ")
            if rules == "y":
                print()
                print("The goal is to arrange all cards in decending order in one pile.")
                print("Move a card to an empty pile or...")
                print("To another pile if the destination's top card is one value higher.")
                print("Pile 0 is the stock pile.")
                print("Activate the undo function if desired.")
                print("The game ends when cards are ordered or no moves remain.")
                print("Unplaceable stock cards can be moved to the bottom with '0'.")
                print("Score is calculated based on cards and moves after each round.")
                print("If stuck, enter 'h' to use a hint.")

    def display(self):
        # calculate spaces for each pile
        pile_spaces = []
        
        for i in range(self.num_piles):
            length = 0
            pile = self.piles[i].get_items()
            if i == 0 and pile:
                length += (len(str(pile[0])))
                for _ in range(1, len(pile)):
                    length += 1
            else:
                for card in pile:
                    for j in str(card):
                        length += 1
            length += self.piles[i].size()
            pile_spaces.append(length)
            
        top_border = "╔" + "═" * (((self.spaces) + self.num_cards) + 5) + "╗"
        bottom_border = "╚" + "═" * (((self.spaces) + self.num_cards) + 5) + "╝"
        print(top_border)
        
        # printing out piles
        for i in range(self.num_piles):
            pile = self.piles[i].get_items()
            if i == 0 and pile:
                print(f"║ 0: {pile[0]}", end=" ")
                for _ in range(1, len(pile)):
                    print("*", end=" ")
            else:
                print(f"║ {i}:", end=" ")
                for card in pile:
                    print(card, end=" ")
                    
            # calulating space for the right side of box to be aligned
            print(" " * (len(top_border) - (pile_spaces[i] + 5 + len(str(i)))) + "║")
        print(bottom_border)
  
    def move(self, p1, p2):
        if p1 == 0 and p2 == 0:
            if self.piles[p1].size() != 0:
                top_card = self.piles[p1].remove_top()
                self.piles[p1].add_bottom(top_card)
                
        elif p1 == 0 and p2 > 0:
            if self.piles[p1].size() != 0 and self.piles[p2].size() != 0:
                top_card = self.piles[p1].peek_top()
                bottom_card = self.piles[p2].peek_bottom()
                if top_card == bottom_card - 1:
                    moving_card = self.piles[p1].remove_top()
                    self.piles[p2].add_bottom(moving_card)     
            if self.piles[p1].size() != 0 and self.piles[p2].size() == 0:
                moving_card = self.piles[p1].remove_top()
                self.piles[p2].add_bottom(moving_card)
                
        elif p1 > 0 and p2 > 0:
            while self.piles[p1].size() != 0 and self.piles[p2].size() != 0:
                top_card = self.piles[p1].peek_top()
                bottom_card = self.piles[p2].peek_bottom()
                if top_card == bottom_card - 1:
                    self.piles[p2].add_bottom(self.piles[p1].remove_top())
                else:
                    break
        self.move_history.append((p1, p2))
        
    def check_valid(self, inputs):
        if inputs.lower() == "y" or inputs.lower() == "n":
            return True
        else:
            return False
        
    def undo(self):
        if len(self.move_history) == 0:
            print("No moves to undo.")
            print()
            return
            
        undo_confirm = input("Undo your last move? (y/n): ")
        
        while not self.check_valid(undo_confirm):
            undo_confirm = input("Please enter (y/n): ")
        p1, p2 = self.move_history.pop()
        
        if undo_confirm.lower() == "y":
            moving_card = self.piles[p2].remove_bottom()
            self.piles[p1].add_top(moving_card)
            
    def valid_move(self):
        # Check if user inputs for piles are valid
        while True:
            try:
                pile_1 = int(input("Move from pile no.: "))
                if pile_1 not in range(0, self.num_piles):
                    print("That is not a valid pile no. Try again: ")
                    print()
                    continue
                elif self.piles[pile_1].size() == 0:
                    print(f"Pile {pile_1} is empty. Please choose a non empty pile.")
                    print()
                    continue
            except ValueError:
                print("Please enter a valid integer for the pile number.")
                print()
                continue
                
            while True:
                try:
                    pile_2 = int(input("Move to pile no.: "))
                    if pile_2 not in range(0, self.num_piles):
                        print("That is not a valid pile no. Try again: ")
                        print()
                        continue  
                    break
                except ValueError:
                    print("Please enter a valid integer for pile number.")
                    print()
                    continue
                
            if pile_1 == pile_2:
                if pile_1 == 0 and pile_2 == 0:
                    break
                else:
                    print("Invalid move. Piles must be different. \n")
            else:
                break
        self.move(pile_1, pile_2)
        self.move_history.append((pile_1, pile_2))
        
    def hint(self):
        print("Hint: ", end = "")
        non_empty_piles = [i for i in range(0, self.num_piles) if self.piles[i].size() > 0]
        self.hints += 1
        
        # Check possible moves ensuring destination isnt stock pile
        for i in range(self.num_piles):
            for j in non_empty_piles:
                if j > 0 and self.piles[i].size() > 0 and self.piles[j].size() > 0:
                    top_card = self.piles[i].peek_top()
                    bottom_card = self.piles[j].peek_bottom()
                    if top_card == bottom_card - 1 and j != 0:
                        print(f"Move a card from pile {i} to pile {j}. \n")
                        return
                    
        # Check for empty piles and move stock card          
        if len(non_empty_piles) < self.num_piles:
            for i in range(1, self.num_piles):
                if self.piles[i].size() == 0:
                    print(f"Move a card from pile 0 to an empty pile {i}. \n")
                    return
                
        # Exhaust options - replace a stock card in pile 0
        print("Replace stock card in pile 0. \n")
                        
    def is_complete(self):
        if self.piles[0].size() != 0:
            return False

        pile_number = None
        for i in range(1, len(self.piles)):
            if self.piles[i].size() == self.num_cards:
                pile_number = i

        if pile_number is None:
            return False
        
        # Cards are ordered
        prev_card = float('inf')
        for card in self.piles[pile_number].get_items():
            if card >= prev_card:
                return False
            prev_card = card
        return True

    def play_again(self, custom_cards=None):
        # start a new game with custom cards
        while not custom_cards or not self.validate_custom_cards(custom_cards):
            print("Ensure the cards randomised, consecutive and begin from 0 or 1.")
            custom_cards = input("Enter a list of card values separated by spaces (e.g. 3 2 1): ")

        previous_highscore = self.highscore
        game = Solitaire(list(map(int, custom_cards.split())))
        game.round_counter = self.round_counter
        game.hints = self.hints
        game.highscore = previous_highscore
        game.play()

    def validate_custom_cards(self, custom_cards):
        card_values = custom_cards.split()

        try:
            card_values = [int(card) for card in card_values]
        except:
            print("Invalid input. Please enter numbers separated by spaces.")
            print()
            return False
        
        expected_values_0 = set(range(0, len(card_values)))
        expected_values_1 = set(range(1, len(card_values)+1))
        
        if set(card_values) == expected_values_1 or set(card_values) == expected_values_0:
            return True
        else:
            print("Invalid input.")
            print()
            return False
        
    def play(self):
        # main game
        self.introduction()
        print()
        toggle_undo = input("Activate undo function this round (y/n)? ")
        
        while not self.check_valid(toggle_undo):
            toggle_undo = input(f"'{toggle_undo}' is not y or n. Please enter either (y/n): ")
        print()
        print(f"----- ROUND {self.round_counter} -----")
        move_number = 1
        score = 0
        display_counter = 0
        
        while move_number <= self.max_num_moves and not self.is_complete():
            if display_counter == 0:
                self.display()
                print()
                print(f"----- Move {move_number} out of {self.max_num_moves} -----")
                
            if toggle_undo.lower() == "y":
                undo_activated = True
            else:
                undo_activated = False
                
            if undo_activated:
                user_input = input("Enter 'm' to make a move, 'u' to undo a move, or 'h' for a hint: ").lower()
            else:
                user_input = input("Enter 'm' to make a move or 'h' for a hint: ").lower()
                
            while user_input not in ['m', 'u', 'h']:
                if undo_activated:
                    user_input = input("Invalid input. Enter 'm' to make a move, 'u' to undo a move, or 'h' for a hint: ").lower()
                else:
                    user_input = input("Invalid input. Enter 'm' to make a move or 'h' for a hint: ").lower()
                    
            if user_input == 'm':
                pile_1 = None
                pile_2 = None
                self.valid_move()
                move_number += 1
                display_counter = 0
            elif user_input == 'u' and undo_activated:
                self.undo()
                display_counter = 0
            elif user_input == 'h':
                self.hint()
                display_counter += 1
                    
        print()
        if self.is_complete():
            print("You Win in", move_number - 1, "steps and", self.hints, "hints!\n")
        else:
            print("Out of Moves!\n")
        
        score = round(150 - ((move_number - 1) / self.max_num_moves) * 100)
        
        if self.round_counter > 1 and score > self.highscore:
            print("Congratulations! You beat your highscore!")
        if score > self.highscore:
            self.highscore = score
        print(f"Current score: {score}")
        print(f"Highscore: {self.highscore}\n")
        self.round_counter += 1
        play_again_input = input("Do you want to play again? (y/n): ")
        
        while not self.check_valid(play_again_input):
            play_again_input = input(f"'{play_again_input}' is not y or n. Please enter either (y/n): ")
            
        if play_again_input.lower() == 'y':
            print()
            self.play_again()
        else:
            print()
            print("--------------------------")
            print(f"Thank you for playing!")
            print(f"Your highscore was {self.highscore}.")

                         
class CardPile:
    def __init__(self):
        self.item = []

    def add_top(self, item):
        self.item.insert(0, item)

    def add_bottom(self, item):
        if len(self.item) == 0:
            self.item.insert(0, item)
        else:
            self.item.insert(self.size(), item)

    def remove_top(self):
        return self.item.pop(0)

    def remove_bottom(self):
        return self.item.pop(self.size() - 1)

    def size(self):
        return len(self.item)

    def peek_top(self):
        return self.item[0]

    def peek_bottom(self):
        return self.item[self.size() - 1]
    
    def get_items(self):
        return self.item
    
# Example Game
# cards = [3, 2, 1]
# game = Solitaire(cards)
# game.play()
cards = [3, 2, 1]
game = Solitaire(cards)
game.play()

