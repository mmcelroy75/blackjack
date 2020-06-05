import random

class Deck:

    def __init__(self, number=2):
        self.number = number
        self.cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'K', 'Q', 'A']
        self.card_deck = (self.cards * 4) * self.number

        self.card_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 1}

        self.count_values = {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0, '8': 0, '9': 0, '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}

        self.discard_deck = []
        self.running_count = 0
        self.true_count = self.running_count // self.number
    
    def __repr__(self):
        return self.cards
    
    def shuffle(self):
        self.card_deck = self.discard_deck + self.card_deck
        self.running_count = 0
        random.shuffle(self.card_deck)    
        print("\nDeck is being shuffled...\n")
        # Represents deck being cut.
        mid_idx = len(self.card_deck) // 2
        self.card_deck[:mid_idx], self.card_deck[mid_idx + 1:] = self.card_deck[mid_idx + 1:], self.card_deck[:mid_idx]
        print("Deck has been cut.\n")
        # Represents burning top card.
        self.discard_deck.append(self.card_deck.pop())
        print("Top card burned. Ready to deal.\n")
        return self.card_deck

class Hand(list):
    
    def __init__(self):
        self.hand = []

    def __repr__(self):
        return self.hand
    
    def total_hand(self):
        total = 0
        has_ace = False
        for card in self.hand:
            total += deck.card_values.get(card)
            if card == 'A':
                has_ace = True
        if has_ace and total <= 11:
            total += 10
        return total

class Dealer:

    def __init__(self, name="the Dealer"):
        self.name = name
        self.dealer_hand = Hand()

    def __repr__(self):
        return self.name

class Player:
    
    def __init__(self, name, bankroll=10000):
        self.name = name.title()
        self.bankroll = bankroll
        self.player_hand = Hand()

    def __repr__(self):
        return self.name, self.bankroll


def play_blackjack(player, deck, dealer=Dealer()):
    if len(deck.discard_deck) >= (len(deck.card_deck) * .60) or not deck.discard_deck:
        deck.shuffle()

    # Draws and removes top cards from deck, 2 for player and 2 for dealer
    player_card1, player_card2 = deck.card_deck.pop(), deck.card_deck.pop()
    dealer_card1, dealer_card2 = deck.card_deck.pop(), deck.card_deck.pop()

    # Appends cards to player's/dealer's hand.
    player.player_hand.append(player_card1)
    print(f"Your first card is {player_card1}...")

    dealer.dealer_hand.append(dealer_card1)

    player.player_hand.append(player_card2)
    print(f"...your second card is {player_card2}.")

    dealer.dealer_hand.append(dealer_card2)
    print(f"The dealer is showing {dealer_card1}.\n")

    print(f"You have {player.player_hand.total_hand()}.")
        

deck = Deck()
ned = Player("Ned")

play_blackjack(ned, deck)
