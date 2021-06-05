import random
import time
import math
import pyinputplus as pyip
from os import system


class Deck:

    def __init__(self, number=2, penetration=0.60):  # defaults to a double-deck game
        self.number = number
        self.penetration = penetration
        self.cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        self.card_deck = (self.cards * 4) * self.number

        self.card_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                            '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

        self.count_values = {'2': 1, '3': 1, '4': 1, '5': 1, '6': 1, '7': 0,
                             '8': 0, '9': 0, '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1}

        self.discard_deck = []
        self.running_count = 0
        # self.true_count = self.running_count // (len(self.card_deck) // 52)
        self.true_count = math.floor(self.running_count // (len(self.card_deck) // 52))

    def __repr__(self):
        return self.cards

    def shuffle(self):
        self.card_deck = self.discard_deck + self.card_deck
        self.discard_deck.clear()
        self.running_count = 0
        random.shuffle(self.card_deck)
        print("\nDeck is being shuffled...\n")
        # Represents deck being cut.
        mid_idx = len(self.card_deck) // 2
        self.card_deck[:mid_idx], self.card_deck[mid_idx +
                                                 1:] = self.card_deck[mid_idx + 1:], self.card_deck[:mid_idx]
        print("Deck has been cut.\n")
        # Represents burning top card.
        burn_card = self.card_deck.pop()
        self.discard_deck.append(burn_card)
        print("Top card burned. Ready to deal.\n")
        return self.card_deck

    def hit(self, target):
        hit_card = self.card_deck.pop()
        target.hand.append(hit_card)
        self.running_count += self.count_values.get(hit_card)
        return hit_card

    def count_cards(self):
        if self.true_count > 2:
            print("The deck is pretty rich. Consider betting more.")
        elif self.true_count < -2:
            print("The deck is pretty thin. Consider betting less.")
        else:
            pass


class Hand(list):

    def __init__(self):
        self.hand = self

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
        self.hand = Hand()
        self.is_busted = False
        self.ask_insurance = False

    def __repr__(self):
        return self.name


class Player:

    def __init__(self, name, bankroll=10000):
        self.name = name.title()
        self.bankroll = bankroll
        self.hand = Hand()
        self.is_busted = False
        self.insurance = False

    def __repr__(self):
        return self.name, self.bankroll

# Helper functions


def play_again(player, deck, dealer=Dealer()):
    choice = pyip.inputYesNo(prompt="Would you like to play another hand? Y/N\n")
    if choice == "yes":
        play_blackjack(player, deck)
    else:
        quit()


def cleanup(player, deck, dealer=Dealer()):
    player.is_busted = False
    dealer.is_busted = False
    dealer.ask_insurance = False
    player.insurance = False
    print("Clearing the layout...\n")
    deck.discard_deck.extend(player.hand)
    deck.discard_deck.extend(dealer.hand)
    player.hand.clear()
    dealer.hand.clear()
    play_again(player, deck)

# def resolve_bankroll(player, dealer=Dealer()):
#     if dealer.is_busted == True:
#         player.bankroll = player.bankroll + wager
#     elif player.hand.total_hand() > dealer.hand.total_hand():
#         print(f"{dealer.name.title()} stands with {dealer.hand.total_hand()}.\n")
#         print(f"You beat {dealer.name} and win ${wager}.\n")
#         player.bankroll = player.bankroll + wager
#     elif dealer.hand.total_hand() > player.hand.total_hand():
#         print(f"{dealer.name.title()} stands with {dealer.hand.total_hand()}.\n")
#         print(f"{dealer.name.title()} beats you. You lose your wager of ${wager}.\n")
#         player.bankroll = player.bankroll - wager
#     else:
#         print("It's a push.\n")

# Main game function


def play_blackjack(player, deck, dealer=Dealer()):
    system('clear')

    print(len(deck.card_deck))  # This just for testing purposes
    print(deck.true_count)   # This is just for testing purposes

    if len(deck.discard_deck) >= (len(deck.card_deck) * deck.penetration) or not deck.discard_deck:
        deck.shuffle()

    print(len(deck.card_deck))  # This just here for testing purposes
    print(len(deck.discard_deck))  # This just here for testing purposes

    deck.count_cards()
    wager = pyip.inputNum(
        prompt=f"You have ${player.bankroll:,.2f}. Table minimum is $50. How much would you like to bet? ", max=player.bankroll, min=50)

    # Draws and removes top cards from deck, 2 for player and 2 for dealer
    player_card1, dealer_card1 = deck.hit(player), deck.hit(dealer)
    player_card2, dealer_card2 = deck.hit(player), deck.hit(dealer)

    # Appends cards to player's/dealer's hand.
    print("\nBets are placed. Cards are out...\n")
    time.sleep(0.5)
    # player.hand.append(player_card1)
    print(f"Your first card is {player_card1}...\n")
    time.sleep(0.5)
    # dealer.hand.append(dealer_card1)

    # player.hand.append(player_card2)
    print(f"...your second card is {player_card2}.\n")
    time.sleep(0.5)
    # dealer.hand.append(dealer_card2)
    print(f"The dealer is showing {dealer_card1}.\n")
    time.sleep(0.5)
    # Print
    print(f"You have {player.hand.total_hand()}.\n")

    # Control flow for dealer Ace Up (insurance)
    if dealer_card1 == 'A':
        dealer.ask_insurance = True

        while dealer.ask_insurance:
            insurance = pyip.inputYesNo(prompt="Would you like to take insurance? Y/N \n")

            if insurance == 'yes':
                player.insurance = True
                insurance_amount = pyip.inputNum(
                    prompt=f"How much would you like to wager? You can take up to ${(wager/2): .2f} \n", max=(wager / 2))

                if deck.card_values.get(dealer_card2) == 10:
                    # print(f"{dealer.name.title()} has blackjack. You lose the hand but win your insurance bet.\n")
                    player.bankroll = player.bankroll - wager
                    player.bankroll = player.bankroll + (insurance_amount * 2)
                    break
                else:
                    print(f"{dealer.name.title()} does not have blackjack. You are still in action, but lose your insurance bet. You have {player.hand.total_hand()}.\n")
                    player.bankroll = player.bankroll - insurance_amount  # need to get this to go-to next block
                    break
            else:
                player.insurance = False
                if deck.card_values.get(dealer_card2) == 10:
                    # print(f"{dealer.name.title()} has blackjack. You lose the hand but win your insurance bet.\n")
                    player.bankroll = player.bankroll - wager
                    break
                else:
                    print(f"Nobody home. You have {player.hand.total_hand()}.\n")
                    break

    # Control flow for pat blackjacks.
    if dealer.hand.total_hand() == 21 and player.hand.total_hand() < 21:
        if player.insurance:
            print(f"{dealer.name.title()} has blackjack. You lose the hand but win your insurance bet.\n")
        else:
            print(f"{dealer.name.title()} has blackjack. You lose the hand.\n")

        player.bankroll = player.bankroll - wager

    elif player.hand.total_hand() == 21 and dealer.hand.total_hand() < 21:
        print(f"You have blackjack! You win {wager * 1.5: .2f}!\n")
        player.bankroll = player.bankroll + (wager * 1.5)

    elif dealer.hand.total_hand() == 21 and player.total_hand() == 21:
        print(f"You and {dealer.name} push. You both have blackjack.\n")

    else:  # Control flow to resolve non-blackjack hands
        while player.hand.total_hand() <= 21 and not player.is_busted:
            if len(player.hand) == 2:
                choice = pyip.inputChoice(
                    choices=['H', 'S', 'D'], prompt="What would you like to do? (H)it, (S)tand, or (D)ouble?").lower()
            else:
                choice = pyip.inputChoice(
                    choices=['H', 'S'], prompt="What would you like to do? (H)it or (S)tand?").lower()

            if choice == "h":
                # pl_hit_card = deck.hit(player)
                # player.hand.append(pl_hit_card)
                print(
                    f"\nYou get a {deck.hit(player)}. You now have {player.hand.total_hand()}.\n")
                if player.hand.total_hand() > 21:
                    print("You busted.\n")
                    player.is_busted = True
                    player.bankroll = player.bankroll - wager
                    break

            elif choice == "d":
                wager += wager
                dd_card = deck.hit(player)
                # player.hand.append(pl_hit_card)
                if player.hand.total_hand() > 21:
                    print(f"You get a {dd_card}. You busted.\n")
                    player.is_busted = True
                    player.bankroll = player.bankroll - wager
                    break
                else:
                    print(
                        f"\nYour double down card is a {dd_card}. You now have {player.hand.total_hand()}.\n")
                    break

            else:
                print(f"\nPlayer stands with {player.hand.total_hand()}.\n")
                break

        # Control flow to resolve dealer hand.
        if not player.is_busted and not dealer.is_busted:
            # dlr_hit_card = deck.card_deck.pop()
            print(
                f"{dealer.name.title()} opens a {dealer_card2}, for a total of {dealer.hand.total_hand()}.\n")
            time.sleep(0.5)
            while dealer.hand.total_hand() < 17:
                # deck.hit(dealer)
                print(
                    f"{dealer.name.title()} draws a {deck.hit(dealer)} and now has {dealer.hand.total_hand()}.\n")
                time.sleep(0.5)
                if dealer.hand.total_hand() > 21:
                    dealer.is_busted = True
                    print(
                        f"{dealer.name.title()} busts with {dealer.hand.total_hand()}! You win {wager}!\n")
                    time.sleep(0.5)
                    break

            # Resolves win/loss and credits/debits player bankroll
            if dealer.is_busted:
                player.bankroll = player.bankroll + wager
            elif player.hand.total_hand() > dealer.hand.total_hand():
                print(f"{dealer.name.title()} stands with {dealer.hand.total_hand()}.\n")
                print(f"You beat {dealer.name} and win ${wager}.\n")
                player.bankroll = player.bankroll + wager
            elif dealer.hand.total_hand() > player.hand.total_hand():
                print(f"{dealer.name.title()} stands with {dealer.hand.total_hand()}.\n")
                print(f"{dealer.name.title()} beats you. You lose your wager of ${wager}.\n")
                player.bankroll = player.bankroll - wager
            else:
                print("It's a push.\n")

    # Final cleanup steps
    player.is_busted = False  # Resets is_busted status
    dealer.is_busted = False
    dealer.ask_insurance = False  # Resets dealer ace up trigger
    player.insurance = False
    print("Clearing the layout...\n")
    deck.discard_deck.extend(player.hand)  # Adds player/dealer cards to discard
    deck.discard_deck.extend(dealer.hand)
    player.hand.clear()  # Empties player/dealer hands
    dealer.hand.clear()
    # cleanup(player, deck)
    play_again(player, deck)


deck = Deck()
ned = Player("Ned")

if __name__ == '__main__':
    play_blackjack(ned, deck)
