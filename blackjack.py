# Problem Set 4
# Name: Shirin Amouei
# Collaborators: None
# Time Spent: 10:00
# Late Days Used: 1

import matplotlib.pyplot as plt
import numpy as np
from ps4_classes import BlackJackCard, CardDecks, Busted
import scipy.stats as stats


#############
# PROBLEM 1 #
#############
class BlackJackHand:
    """
    A class representing a game of Blackjack.   
    """
    
    hit = 'hit'
    stand = 'stand'

    def __init__(self, deck):
        """
        Parameters:
        deck - An instance of CardDeck that represents the starting shuffled
        card deck (this deck itself contains one or more standard card decks)

        Attributes:
        self.deck - CardDeck, represents the shuffled card deck for this game of BlackJack
        self.player - list, initialized with the first 2 cards dealt to the player
                      and updated as the player is dealt more cards from the deck
        self.dealer - list, initialized with the first 2 cards dealt to the dealer
                      and updated as the dealer is dealt more cards from the deck
                      
        Important: You MUST deal out the first four cards in the following order:
            player, dealer, player, dealer
        """
        
        self.deck = deck
        self.player = []
        self.dealer = []
        
        # Deal first four cards: p,d,p,d
        for card in range(2):
            self.player.append(self.deck.deal_card()) 
            self.dealer.append(self.deck.deal_card()) 

    # You can call the method below like this:
    #   BlackJackHand.best_value(cards)
    @staticmethod
    def best_value(cards):
        """
        Finds the total value of the cards. All cards must contribute to the
        best sum; however, an Ace may contribute a value of 1 or 11.
        
        The best sum is the highest point total not exceeding 21 if possible.
        If it is not possible to keep the total value from exceeding 21, then
        the best sum is the lowest total value of the cards.

        Hint: If you have one Ace, give it a value of 11 by default. If the sum
        point total exceeds 21, then give it a value of 1. What should you do
        if cards has more than one Ace?

        Parameters:
        cards - a list of BlackJackCard instances.

        Returns:
        int, best sum of point values of the cards  
        """
        
        # Get number of aces
        num_ace = len([card.get_rank() for card in cards if card.get_rank() == "A"])
        
        # Get total value of cards
        total_value = sum([card.get_val() for card in cards])
        
        # Calculate best value (reduce the value of ace if needed)
        while total_value > 21 and num_ace > 0:
            if num_ace >= 1:
                total_value -= 10
                num_ace -= 1
                
        return total_value
                
    def get_player_cards(self):
        """
        Returns:
        list, a copy of the player's cards 
        """
        
        # Return a copy of list
        return self.player.copy()

    def get_dealer_cards(self):
        """
        Returns:
        list, a copy of the dealer's cards 
        """
        
        # Return a copy of list
        return self.dealer.copy()

    def get_dealer_upcard(self):
        """
        Returns the dealer's face up card. We define the dealer's face up card
        as the first card in their hand.

        Returns:
        BlackJackCard instance, the dealer's face-up card 
        """
        
        # Get first card in dealer's list
        return self.dealer[0]

    def set_initial_cards(self, player_cards, dealer_cards):
        """
        Sets the initial cards of the game.
        player_cards - list, containing the inital player cards
        dealer_cards - list, containing the inital dealer cards

        used for testing, DO NOT MODIFY
        """
        self.player = player_cards[:]
        self.dealer = dealer_cards[:]

    # Strategy 1
    def dealer_strategy(self):
        """
        A playing strategy in which the player uses the same metric as the
        dealer to determine their next move.

        The player will:
            - hit if the best value of their cards is less than 17
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision  
        """
        
        # Hit
        if self.best_value(self.get_player_cards()) < 17: 
            return "hit"
        
        # Stand
        else:
            return "stand"
        

    # Strategy 2
    def peek_strategy(self):
        """
        A playing strategy in which the player knows the best value of the
        dealer's cards.

        The player will:
            - hit if the best value of their hand is less than that of the dealer's
            - stand otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision
        """
        
        # Hit
        if self.best_value(self.get_player_cards()) < self.best_value(self.get_dealer_cards()):    
            return "hit"
        
        # Stand
        else:
            return "stand"
        
        
    # Strategy 3
    def simple_strategy(self):
        """
        A playing strategy in which the player will
            - stand if one of the following is true:
                - the best value of player's hand is greater than or equal to 17
                - the best value of player's hand is between 12 and 16 (inclusive)
                  AND the dealer's up card is between 2 and 6 (inclusive)  
            - hit otherwise

        Returns:
        str, "hit" or "stand" representing the player's decision 
        """
        
        # Stand 
        if self.best_value(self.get_player_cards()) >= 17:
            return "stand"
        elif 12 <= self.best_value(self.get_player_cards()) <= 16 and 2 <= self.get_dealer_upcard().get_val() <= 6:
            return "stand" 
        
        # Hit
        else:
            return "hit"
        
    def play_player_turn(self, strategy):
        """
        Plays a full round of the player's turn and updates the player's hand
        to include new cards that have been dealt to the player. The player
        will be dealt a new card until they stand or bust.

        Parameter:
        strategy - function, one of the the 3 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.dealer_strategy)

        This function does not return anything. Instead, it:
            - Adds a new card to self.player each time the player hits.
            - Raises Busted exception (imported from ps4_classes.py) if the
              best value of the player's hand is greater than 21.
        """
        
        # Player gets a new card as long as their strategy is hit
        while strategy(self) == "hit": 
            self.player.append(self.deck.deal_card())  
            
            # Busted error if best value more than 21
            if self.best_value(self.get_player_cards()) > 21: 
                raise Busted
        
        
    def play_dealer_turn(self):
        """
        Plays a full round of the dealer's turn and updates the dealer's hand
        to include new cards that have been dealt to the dealer. The dealer
        will get a new card as long as the best value of their hand is less
        than 17, or they bust.

        This function does not return anything. Instead, it:
            - Adds a new card to self.dealer each time the dealer hits.
            - Raises Busted exception (imported from ps4_classes.py) if the
              best value of the dealer's hand is greater than 21.
        """
        
        # Dealer gets a new card as long as their best value is less than 17
        while self.best_value(self.get_dealer_cards()) < 17: 
            self.dealer.append(self.deck.deal_card())  
            
            # Busted error if best value more than 21
            if self.best_value(self.get_dealer_cards()) > 21: 
                raise Busted

    def __str__(self):
        """
        Returns:
        str, representation of the player and dealer and dealer hands.

        Useful for debugging. DO NOT MODIFY. 
        """
        result = 'Player: '
        for c in self.player:
            result += str(c) + ','
        result = result[:-1] + '    '
        result += '\n   Dealer '
        for c in self.dealer:
            result += str(c) + ','
        return result[:-1]

#############
# PROBLEM 2 #
#############


def play_hand(deck, strategy, bet=1.0):
    """
    Plays a hand of Blackjack and determines the amount of money the player
    gets back based on their inital bet.

    The player will get:

        - 2.5 times their original bet if the player's first two cards equal 21,
          and the dealer's first two cards do not equal 21.
        - 2 times their original bet if the player wins after getting more
          cards or the dealer busts.
        - the original amount they bet if the game ends in a tie. If the
          player and dealer both get blackjack from their first two cards, this
          is also a tie.
        - 0 if the dealer wins or the player busts.

    Parameters:

        deck - an instance of CardDeck
        strategy - function, one of the the 3 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.dealer_strategy)
        bet - float, the amount that the player bets (default=1.0)

    Returns:

        float, the amount the player gets back
    
    Reminder of how the game works:
        1. Deal cards to player, dealer, player, dealer.
        2. Check for blackjacks from either player. If at least one person has 
            blackjack, the game is over. Calculate how much the player receives.
        3. If no one has blackjack, then deal the player until they stand or bust.
            If the player busts, the game is over. Calculate how much the player receives.
        4. If the player has not bust, then deal the dealer until they stand or bust.
            If the dealer busts, the game is over. Calculate how much the player receives.
        5. If no one has bust, determine the outcome of the game based on the
            best value of the player's cards and the dealer's cards.
    """
    
    set_of_cards = BlackJackHand(deck)

    # If only player has 21
    if set_of_cards.best_value(set_of_cards.get_player_cards()) == 21 and set_of_cards.best_value(set_of_cards.get_dealer_cards()) != 21:
        return bet * 2.5  
    
    # If only dealer has 21
    if set_of_cards.best_value(set_of_cards.get_dealer_cards()) == 21 and set_of_cards.best_value(set_of_cards.get_player_cards()) != 21:
        return 0
    
    # Tie, both get 21
    if set_of_cards.best_value(set_of_cards.get_player_cards()) == 21 and set_of_cards.best_value(set_of_cards.get_dealer_cards()) == 21:
        return bet
    
    # Deal player
    try:
        set_of_cards.play_player_turn(strategy)
    # When game is over
    except Busted: 
        return 0 
    
    # Deal dealer
    try:
        set_of_cards.play_dealer_turn()
    # When game is over   
    except Busted: 
        return 2 * bet 
    
    # Player has more points than dealer
    if set_of_cards.best_value(set_of_cards.get_player_cards()) > set_of_cards.best_value(set_of_cards.get_dealer_cards()):
        return 2 * bet
    
    # Player has less points than dealer
    if set_of_cards.best_value(set_of_cards.get_player_cards()) < set_of_cards.best_value(set_of_cards.get_dealer_cards()):
        return 0
    
    # Equal points
    if set_of_cards.best_value(set_of_cards.get_player_cards()) == set_of_cards.best_value(set_of_cards.get_dealer_cards()):
        return bet
    
    

#############
# PROBLEM 3 #
#############


def run_simulation(strategy, bet=2.0, num_decks=8, num_hands=20, num_trials=100, show_plot=False):
    """
    Runs a simulation and generates a normal distribution reflecting 
    the distribution of player's rates of return across all trials.

    The normal distribution is based on the mean and standard deviation of 
    the player's rates of return across all trials. 
    You should also plot the histogram of player's rates of return that 
    underlies the normal distribution. 
    For hints on how to do this, consider looking at 
        matplotlib.pyplot
        scipy.stats.norm.pdf

    For each trial:

        - instantiate a new CardDeck with the num_decks and type BlackJackCard
        - for each hand in the trial, call play_hand and keep track of how
          much money the player receives across all the hands in the trial
        - calculate the player's rate of return, which is
            100*(total money received-total money bet)/(total money bet)

    Parameters:

        strategy - function, one of the the 3 playing strategies defined in BlackJackHand
                   (e.g. BlackJackHand.dealer_strategy)
        bet - float, the amount that the player bets each hand. (default=2)
        num_decks - int, the number of standard card decks in the CardDeck. (default=8)
        num_hands - int, the number of hands the player plays in each trial. (default=20)
        num_trials - int, the total number of trials in the simulation. (default=100)
        show_plot - bool, True if the plot should be displayed, False otherwise. (default=False)

    Returns:

        tuple, containing the following 3 elements:
            - list of the player's rate of return for each trial
            - float, the average rate of return across all the trials
            - float, the standard deviation of rates of return across all trials
    """
    
    # Create a list to store roi values
    list_of_roi = []
    
    # Run num_trials number of trials
    for t in range(num_trials):
        money_received = 0
        deck = CardDecks(num_decks, BlackJackCard)
        for h in range(num_hands):
            money_received += play_hand(deck, strategy, bet)
        
        # Calculate ROI
        roi = 100 * (money_received - (bet * num_hands)) / (bet * num_hands)
        list_of_roi.append(roi)
    
    # Calculate average and standard deviation
    avg_roi = sum(list_of_roi) / num_trials
    std = np.std(np.array(list_of_roi))
        
    # Plot   
    if show_plot:
        plt.figure()
        plt.title("Player's ROI on Playing " + str(num_hands) + " hands (" + strategy.__name__ + ")\n" "Mean= " + str(avg_roi) + ", SD= "+ str(std))
        plt.hist(list_of_roi, density = True) 
        plt.xlabel("% Return")
        list_of_roi.sort()
        plt.plot(list_of_roi, stats.norm.pdf(list_of_roi, avg_roi, std))
        
        # Show plot
        plt.show()
        
    return (list_of_roi, avg_roi, std)
        

def run_all_simulations(strategies):
    """
    Runs the simulation for each strategy in strategies and generates a single
    graph with normal distribution plot for each strategy. 
    No need to graph the underlying histogram. 
    Each guassian (another name for normal) distribution should reflect the
    distribution of rates of return for each strategy.

    Make sure to label each plot with the name of the strategy.

    Parameters:

        strategies - list of strategies to simulate
    """
    
    plt.figure()
    
    # Get values for each strategy
    for strategy in strategies:
        list_of_roi, avg_roi, std = run_simulation(strategy, bet=2.0, num_decks=8, num_hands=20, num_trials=100, show_plot=False)
        
        # Plot
        plt.title("Player's ROI Using Different Strategies ")
        plt.xlabel("% Return")
        list_of_roi.sort()
        plt.plot(list_of_roi, stats.norm.pdf(list_of_roi, avg_roi, std), label = strategy.__name__)
        plt.legend(loc = 'best')
    
    # Show plot
    plt.show()
    


if __name__ == '__main__':
    # uncomment to test each strategy separately
#    run_simulation(BlackJackHand.dealer_strategy, show_plot=True)
#    run_simulation(BlackJackHand.peek_strategy, show_plot=True)
#    run_simulation(BlackJackHand.simple_strategy, show_plot=True)

    # uncomment to run all simulations
#    run_all_simulations([BlackJackHand.dealer_strategy,
#                         BlackJackHand.peek_strategy, BlackJackHand.simple_strategy])
    pass
