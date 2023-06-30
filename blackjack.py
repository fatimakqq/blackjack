import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card: #() not necessary cus no inheritance
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank.capitalize()
        self.value = values[rank.capitalize()]
        
    def __str__(self):
        return (f"{self.rank} of {self.suit}")

class Deck:
    def __init__(self):
        self.all_cards = []
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.all_cards.append(created_card)

    def __str__(self):

        deckstr = ""
        for card in self.all_cards:
            deckstr += card.__str__()
            deckstr+="\n"
        return deckstr

    def shuffle(self):
        random.shuffle(self.all_cards) #acts in place, doesnt return anything
    
    def deal_one(self):
        return self.all_cards.pop()

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
    
    def add_card(self,card):
        self.cards.append(card)
        if card.rank == "Ace":
            self.adjust_for_ace()
        else:
            self.value += card.value
    
    def adjust_for_ace(self):
        if abs(21-(self.value+1)) > abs(21-(self.value+11)):
            self.value += 11
        else:
            self.value += 1

class Chips:
    
    def __init__(self):
        self.total = 100  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(player_chips):
    while True:
        try:
            player_chips.bet = int(input('Enter a bet amount: '))
        except:    
            pass
        else:
            if player_chips.bet > player_chips.total:
                print("You can't bet more than you have")
            else:
                break
        print('Incorrect input, try again')
    
def hit(deck,hand):
    print("hittin")
    hand.add_card(deck.deal_one())

def hit_or_stand(deck,hand):
    global playing
    choice = "wrong"
    while choice.capitalize() != "Hit" and choice.capitalize() != "Stand":
        choice = input("What do you want to do? 'Hit' or 'Stand'?: ")
    if choice.capitalize() == "Hit":
        
        hit(deck, hand)
    else:
        playing = False

def show_some(player,dealer):
    print(f"Dealer's first card: {dealer.cards[0]}")
    print(f"Dealer's second card: HIDDEN")

    print(f"\nPlayer's first card: {player.cards[0]}")
    print(f"Player's second card: {player.cards[-1]}")

def show_all(player,dealer):
    print(f"Dealer's first card: {dealer.cards[0]}")
    print(f"Dealer's second card: {dealer.cards[-1]}")
    
    print(f"\nPlayer's first card: {player.cards[0]}")
    print(f"Player's second card: {player.cards[-1]}")
    
def player_busts(player, chips ): #hand, chips
    print(f"Game over! Player busted with {player.value}")
    chips.lose_bet()
    print(f"Player loses money, total is now {chips.total}")
    playing = False

def player_wins(player, chips):
    print(f"Game over! Player wins with {player.value}")
    chips.win_bet()
    print(f"Player gains money, total is now {chips.total}")
    playing = False
    

def dealer_busts(dealer, chips):
    print(f"Game over! Dealer busted with {dealer.value}")
    chips.win_bet()
    print(f"Player gains money, total is now {chips.total}")
    playing = False
    
def dealer_wins(dealer, chips):
    print(f"Game over! Dealer wins with {dealer.value}")
    chips.lose_bet()
    print(f"Player loses money, total is now {chips.total}")
    playing = False
    
def push():
    pass


while True:
    # Print an opening statement
    print("Welcome to Blackjack!")
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player = Hand()
    dealer = Hand()

    player.add_card(deck.deal_one())
    player.add_card(deck.deal_one())
    dealer.add_card(deck.deal_one())
    dealer.add_card(deck.deal_one())

    # Set up the Player's chips
    chips = Chips()

    # Prompt the Player for their bet
    take_bet(chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player, dealer)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player, dealer)
 
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player.value > 21:
            player_busts(player, chips)
            break
        

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player.value < 21:
        while dealer.value <= 17:
            dealer.add_card(deck.deal_one())
    
        # Show all cards
        show_all(player,dealer)
    
        # Run different winning scenarios
        if player.value > 21:
            player_busts(player, chips)
        elif dealer.value > 21:
            dealer_busts(dealer, chips)     
        elif dealer.value > player.value:
            dealer_wins(dealer, chips)
        else:
            player_wins(player, chips)

    replay_choice = "wrong"
    while replay_choice.capitalize() != "Y" and replay_choice.capitalize() != "N":
        replay_choice = input("Would you like to play again? Y or N: ")
    
    if replay_choice.capitalize() == "Y":
        playing = True
    else:
        playing = False
 
