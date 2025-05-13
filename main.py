import tkinter as tk
from tkinter import messagebox
import random

# Define the deck of cards sorted from A to K for each suit
SUITS = ['♠️', '♥️', '♣️', '♦️']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
DECK = [f"{rank}{suit}" for suit in SUITS for rank in RANKS]

class PokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Texas Hold'em Odds Calculator")
        
        self.players = 0
        self.user_cards = []
        self.community_cards = []
        self.player_odds = 0

        self.create_widgets()

    def create_widgets(self):
        # Number of Players
        self.num_players_label = tk.Label(self.root, text="Select number of players:")
        self.num_players_label.pack(pady=10)
        
        self.num_players_var = tk.StringVar(value='2')  # Default value
        self.num_players_dropdown = tk.OptionMenu(self.root, self.num_players_var, *[str(i) for i in range(2, 11)])
        self.num_players_dropdown.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.ask_user_cards)
        self.next_button.pack(pady=10)

    def ask_user_cards(self):
        self.players = int(self.num_players_var.get())  # Get the number of players

        # Ask the user for their cards
        self.num_players_label.pack_forget()
        self.num_players_dropdown.pack_forget()
        self.next_button.pack_forget()

        self.user_cards_label = tk.Label(self.root, text="Select your two cards:")
        self.user_cards_label.pack(pady=10)

        # Create dropdown for the user's first card
        self.user_card1_var = tk.StringVar(value=DECK[0])  # Default value for card 1
        self.user_card1_dropdown = tk.OptionMenu(self.root, self.user_card1_var, *DECK)
        self.user_card1_dropdown.pack(pady=10)

        # Create dropdown for the user's second card
        self.user_card2_var = tk.StringVar(value=DECK[1])  # Default value for card 2
        self.user_card2_dropdown = tk.OptionMenu(self.root, self.user_card2_var, *DECK)
        self.user_card2_dropdown.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.display_user_cards)
        self.next_button.pack(pady=10)

    def display_user_cards(self):
        card1 = self.user_card1_var.get()
        card2 = self.user_card2_var.get()
        self.user_cards = [card1, card2]

        # Display the user-selected cards
        self.user_cards_label.pack_forget()
        self.user_card1_dropdown.pack_forget()
        self.user_card2_dropdown.pack_forget()

        self.selected_user_cards_label = tk.Label(self.root, text=f"Your Cards: {self.user_cards[0]} {self.user_cards[1]}")
        self.selected_user_cards_label.pack(pady=10)

        # Ask for the first community card
        self.ask_first_community_card()

    def ask_first_community_card(self):
        # Ask for first community card
        self.first_community_card_label = tk.Label(self.root, text="Select the first community card:")
        self.first_community_card_label.pack(pady=10)

        self.first_community_card_var = tk.StringVar(value=DECK[0])  # Default value for first community card
        available_cards = self.get_available_cards()  # Get cards that haven't been chosen yet
        self.first_community_card_dropdown = tk.OptionMenu(self.root, self.first_community_card_var, *available_cards)
        self.first_community_card_dropdown.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.display_first_community_card)
        self.next_button.pack(pady=10)

    def display_first_community_card(self):
        # Get the first community card
        first_community_card = self.first_community_card_var.get()
        self.community_cards = [first_community_card]

        # Display the community card
        self.first_community_card_label.pack_forget()
        self.first_community_card_dropdown.pack_forget()

        self.selected_community_cards_label = tk.Label(self.root, text=f"Community Cards: {', '.join(self.community_cards)}")
        self.selected_community_cards_label.pack(pady=10)

        # Calculate odds
        self.calculate_odds()

        # Ask for the second community card
        self.ask_second_community_card()

    def ask_second_community_card(self):
        # Ask for second community card
        self.second_community_card_label = tk.Label(self.root, text="Select the second community card:")
        self.second_community_card_label.pack(pady=10)

        available_cards = self.get_available_cards()  # Get cards that haven't been chosen yet
        self.second_community_card_var = tk.StringVar(value=DECK[0])  # Default value for second community card
        self.second_community_card_dropdown = tk.OptionMenu(self.root, self.second_community_card_var, *available_cards)
        self.second_community_card_dropdown.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Next", command=self.display_second_community_card)
        self.next_button.pack(pady=10)

    def display_second_community_card(self):
        # Get the second community card
        second_community_card = self.second_community_card_var.get()
        self.community_cards.append(second_community_card)

        # Display the community card
        self.second_community_card_label.pack_forget()
        self.second_community_card_dropdown.pack_forget()

        self.selected_community_cards_label.config(text=f"Community Cards: {', '.join(self.community_cards)}")
        
        # Calculate odds
        self.calculate_odds()

        # Ask for the third community card
        self.ask_third_community_card()

    def ask_third_community_card(self):
        # Ask for third community card
        self.third_community_card_label = tk.Label(self.root, text="Select the third community card:")
        self.third_community_card_label.pack(pady=10)

        available_cards = self.get_available_cards()  # Get cards that haven't been chosen yet
        self.third_community_card_var = tk.StringVar(value=DECK[0])  # Default value for third community card
        self.third_community_card_dropdown = tk.OptionMenu(self.root, self.third_community_card_var, *available_cards)
        self.third_community_card_dropdown.pack(pady=10)

        self.next_button = tk.Button(self.root, text="Finish", command=self.display_third_community_card)
        self.next_button.pack(pady=10)

    def display_third_community_card(self):
        # Get the third community card
        third_community_card = self.third_community_card_var.get()
        self.community_cards.append(third_community_card)

        # Display the community card
        self.third_community_card_label.pack_forget()
        self.third_community_card_dropdown.pack_forget()

        self.selected_community_cards_label.config(text=f"Community Cards: {', '.join(self.community_cards)}")

        # Calculate odds
        self.calculate_odds()

        # Finish and show results
        messagebox.showinfo("Game Over", f"Final Odds: {self.player_odds}%")

        self.root.quit()

    def calculate_odds(self):
        # Example of a placeholder for actual odds calculation
        # This is a very simple mock-up that just generates random odds based on the number of players
        self.player_odds = random.randint(0, 100)

        # Show the odds
        odds_label = tk.Label(self.root, text=f"Your odds of winning: {self.player_odds}%")
        odds_label.pack(pady=10)

    def get_available_cards(self):
        # Return a list of cards that are not already chosen by the user or as community cards
        all_cards = set(DECK)
        chosen_cards = set(self.user_cards + self.community_cards)
        available_cards = list(all_cards - chosen_cards)
        return available_cards

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    app = PokerApp(root)
    root.mainloop()
