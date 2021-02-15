import math
import json
import os
import random
import copy
import numpy as np
import matplotlib.pyplot as plt

# Global Variables
num_players = 5
use_given_community_cards = False
commmunity_cards_given = [
    {"rank": "10", "suit": "spades"},
    {"rank": "9", "suit": "spades"},
    {"rank": "King", "suit": "diamonds"},
    {"rank": "Queen", "suit": "hearts"},
    {"rank": "5", "suit": "spades"},
]

# creats a card deck from the json file
def create_card_deck():
    location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(location, "card_deck.json"),'r') as f:
        contents = f.read()
        deck = json.loads(contents)
        return deck["cards"]

# takes in the string rank and returns the integer equivalent
def convert_rank_to_number(rank, aces_are_1 = False):
    try:
        int_rank = int(rank)
        return int_rank
    except:
        if(rank == "Jack"):
            return 11
        if(rank == "Queen"):
            return 12
        if(rank == "King"):
            return 13
        if(rank == "Ace" and aces_are_1):
            return 1
        if(rank == "Ace" and not aces_are_1):
            return 14
        else:
            raise Exception

# converts a suit to a number
def convert_suit_to_number(suit):
    if(suit == "clubs"):
        return 0
    if(suit == "diamonds"):
        return 1
    if(suit == "hearts"):
        return 2
    if(suit == "spades"):
        return 3
    raise Exception

# shuffles the deck
def shuffle(deck):
    random.shuffle(deck)
    return deck

# deals out two cards to each player
def deal_out_cards(deck, num_players):
    players = [ [] for _ in range(0, num_players)]
    for _ in range(0, 2):
        for x in range(0, num_players):
            index = random.randint(0, len(deck) - 1)
            players[x].append(deck[index])
            del deck[index]
    return players

# deals out the community cards
def get_community_cards(deck):
    community_cards = []
    for _ in range(0, 5):
        index = random.randint(0, len(deck) - 1)
        community_cards.append(deck[index])
        del deck[index]
    return community_cards

# converts the deck from string to the integer equivalents
def convert_deck_to_numeric(deck):
    deck_num = []
    for x in deck:
        rank_num = convert_rank_to_number(x["rank"])
        deck_num = convert_suit_to_number(x["suit"])
        new_card = []
        new_card.append(rank_num)
        new_card.append(deck_num)
        deck_num.append(new_card)
    return deck_num

# takes in two lists of cards and returns two parralel arrays for the rank and suits in numeric form
def split_up_into_ranks_and_suits_numeric(hand, community_cards):
    cards_ranks = []
    cards_suits = []
    for x in hand:
        i = convert_rank_to_number(x["rank"])
        cards_ranks.append(i)
        i = convert_suit_to_number(x["suit"])
        cards_suits.append(i)
    for x in community_cards:
        i = convert_rank_to_number(x["rank"])
        cards_ranks.append(i)
        i = convert_suit_to_number(x["suit"])
        cards_suits.append(i)
    return (cards_ranks, cards_suits)

# determines if a royal flush can be played
def has_royal_flush(hand, community_cards):
    (cards_ranks, cards_suits) = split_up_into_ranks_and_suits_numeric(hand, community_cards)
    for i, x1 in enumerate(cards_ranks):
        if x1 == 14:
            suit = cards_suits[i]
            for i2, x2 in enumerate(cards_ranks):
                if x2 == 13 and cards_suits[i2] == suit:
                    for i3, x3 in enumerate(cards_ranks):
                        if x3 == 12 and cards_suits[i3] == suit:
                            for i4, x4 in enumerate(cards_ranks):
                                if x4 == 11 and cards_suits[i4] == suit:
                                    for i5, x5 in enumerate(cards_ranks):
                                        if x5 == 12 and cards_suits[i5] == suit:
                                            return True
    return False
 
# determines if a straight flush can be played
def has_straight_flush(hand, community_cards):
    (cards_ranks, cards_suits) = split_up_into_ranks_and_suits_numeric(hand, community_cards)
    for (i, x) in enumerate(cards_ranks):
        suit = cards_suits[i]
        for i2, x2 in enumerate(cards_ranks):
            if x2 == x-1 and cards_suits[i2] == suit:
                for i3, x3 in enumerate(cards_ranks):
                    if x3 == x-2 and cards_suits[i3] == suit:
                        for i4, x4 in enumerate(cards_ranks):
                            if x4 == x-3 and cards_suits[i4] == suit:
                                for i5, x5 in enumerate(cards_ranks):
                                    if (x5 == x-4 or (x4 == 2 and x5 == 14)) and cards_suits[i5] == suit: #checks for ace as the low as well
                                        return True
    return False

# determins if there is a four of a kind
def has_four_of_a_kind(hand, community_cards):
    (cards_ranks, cards_suits) = split_up_into_ranks_and_suits_numeric(hand, community_cards)
    count = [0 for _ in range(0, 15)]
    for x in cards_ranks:
        count[x] += 1
    for x in count:
        if x >= 4:
            return True
    return False

# determines if there is a full house
def has_full_house(hand, community_cards):
    (cards_ranks, cards_suits) = split_up_into_ranks_and_suits_numeric(hand, community_cards)
    count = [0 for _ in range(0, 15)]
    for x in cards_ranks:
        count[x] += 1
    first_max = max(count)
    del count[count.index(first_max)]
    second_max = max(count)
    if first_max >= 3 and second_max >= 2:
        return True
    return False

# determines if there is a flush
def has_flush(hand, community_cards):
    (cards_ranks, cards_suits) = split_up_into_ranks_and_suits_numeric(hand, community_cards)
    count = [0 for _ in range(0, 5)]
    for x in cards_suits:
        count[x] += 1
    if max(count) >= 5:
        return True
    return False

# determines of there is a straight
def has_straight(hand, community_cards):
    (cards_ranks, cards_suits) = split_up_into_ranks_and_suits_numeric(hand, community_cards)
    for x in cards_ranks:
        for x2 in cards_ranks:
            if x2 == x-1:
                for x3 in cards_ranks:
                    if x3 == x-2:
                        for x4 in cards_ranks:
                            if x4 == x-3:
                                for x5 in cards_ranks:
                                    if x5 == x-4 or (x4 == 2 and x5 == 14): #checks for ace as the low as well
                                        return True
    return False

# determines if there are three of a kind
def has_three_of_a_kind(hand, community_cards):
    (cards_ranks, cards_suits) = split_up_into_ranks_and_suits_numeric(hand, community_cards)
    count = [0 for _ in range(0, 15)]
    for x in cards_ranks:
        count[x] += 1
    if max(count) >= 3:
        return True
    return False

# determines if there are two pair
def has_two_pair(hand, community_cards):
    (cards_ranks, cards_suits) = split_up_into_ranks_and_suits_numeric(hand, community_cards)
    count = [0 for _ in range(0, 15)]
    for x in cards_ranks:
        count[x] += 1
    first_max = max(count)
    del count[count.index(first_max)]
    second_max = max(count)
    if first_max >= 2 and second_max >= 2:
        return True
    return False

# determines if there is a pair
def has_pair(hand, community_cards):
    (cards_ranks, cards_suits) = split_up_into_ranks_and_suits_numeric(hand, community_cards)
    count = [0 for _ in range(0, 15)]
    for x in cards_ranks:
        count[x] += 1
    if max(count) >= 2:
        return True
    return False

# plays out a single round
def play_out_round(deck, num_players, community_cards = []):
    deck = shuffle(deck)
    num_players
    if community_cards == []:
        community_cards = get_community_cards(deck)
    else:
        for x in community_cards:
            del deck[deck.index(x)]
    players = deal_out_cards(deck, num_players)

    royal_flush = 0
    straight_flush = 0
    four_of_a_kind = 0
    full_house = 0
    flush = 0
    straight = 0
    three_of_a_kind = 0
    two_pair = 0
    pair = 0
    high_card = 0

    for x in players:
        if has_royal_flush(x, community_cards):
            royal_flush += 1
        elif has_straight_flush(x, community_cards):
            straight_flush += 1
        elif has_four_of_a_kind(x, community_cards):
            four_of_a_kind += 1
        elif has_full_house(x, community_cards):
            full_house += 1
        elif has_flush(x, community_cards):
            flush += 1
        elif has_straight(x, community_cards):
            straight += 1
        elif has_three_of_a_kind(x, community_cards):
            three_of_a_kind += 1
        elif has_two_pair(x, community_cards):
            two_pair += 1
        elif has_pair(x, community_cards):
            pair += 1
        else:
            high_card += 1

    # for x in players:
    #     print(x)
    # print(community_cards)

    # print("royal flush: ", royal_flush)
    # print("straight flush: ", straight_flush)
    # print("four of a kind: ", four_of_a_kind)
    # print("full house: ", full_house)
    # print("flush: ", flush)
    # print("straight: ", straight)
    # print("three of a kind: ", three_of_a_kind)
    # print("two pair: ", two_pair)
    # print("pair: ", pair)
    # print("high card: ", high_card)
    return {
        "royal flush": royal_flush,
        "straight flush": straight_flush,
        "four of a kind": four_of_a_kind,
        "full house": full_house,
        "flush": flush,
        "straight": straight,
        "three of a kind": three_of_a_kind,
        "two pair": two_pair,
        "pair": pair,
        "high card: ": high_card,
    }

# global variable for the bar width
bar_width = .10

# plots a bar graph
def plot_bar(array, label, offset):
    ind = np.arange(num_players+1)  # the x locations for the groups
    array = [x / 10 for x in array]
    plt.bar(ind + offset, array, bar_width, label=label)


# iterates over the rounds and saves the data and then displays the data
def main():
    card_deck = create_card_deck()

    overall_data = {
        "royal flush": [ 0 for _ in range(0, num_players+1)],
        "straight flush": [ 0 for _ in range(0, num_players+1)],
        "four of a kind": [ 0 for _ in range(0, num_players+1)],
        "full house": [ 0 for _ in range(0, num_players+1)],
        "flush": [ 0 for _ in range(0, num_players+1)],
        "straight": [ 0 for _ in range(0, num_players+1)],
        "three of a kind": [ 0 for _ in range(0, num_players+1)],
        "two pair": [ 0 for _ in range(0, num_players+1)],
        "pair": [ 0 for _ in range(0, num_players+1)],
        "high card: ": [ 0 for _ in range(0, num_players+1)],
    }

    for _ in range(0, 1000):  
        new_deck = copy.deepcopy(card_deck)
        if use_given_community_cards:
            data = play_out_round(new_deck, num_players, commmunity_cards_given)
        else:
            data = play_out_round(new_deck, num_players)
        for x in data:
            overall_data[x][data[x]] += 1

    for i, x in enumerate(overall_data):
        plot_bar(overall_data[x], x, bar_width*i)
    plot_bar([0 for _ in range(0, num_players+1)], "", bar_width*num_players*2)
    
    plt.xlabel('People')
    plt.ylabel('Percentage')
    plt.title('chances of each type of hand')
    plt.legend()
    plt.show()









if __name__ == "__main__":
    main()