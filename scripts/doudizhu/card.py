# -*- coding: utf-8 -*-

from doudizhu.compat import is_py3, cmp_to_key


class Card(object):
    """
    https://github.com/worldveil/deuces
    Static class that handles cards. We represent cards as 8-bit integers, so
    there is no object instantiation - they are just ints. Most of the bits are
    used, and have a specific meaning. See below:

                    Card:

                    suit rank
                    +--------+
                    |cdhsrrrr|
                    +--------+

        1) r = rank of card (trey=0,four=1,five=2,...,ace=11,deuce=12,
                             Black-Joker=13,Colored-Joker=14)
        2) cdhs = suit of card (bit turned on based on suit of card)
    """

    # the basics
    STR_JOKERS = ['BJ', 'CJ']
    STR_RANKS = '3-4-5-6-7-8-9-10-J-Q-K-A-2-BJ-CJ'.split('-')
    INT_RANKS = range(15)

    # converstion from string => int
    CHAR_RANK_TO_INT_RANK = dict(zip(STR_RANKS, INT_RANKS))
    CHAR_SUIT_TO_INT_SUIT = {
        's': 1,  # spades
        'h': 2,  # hearts
        'd': 4,  # diamonds
        'c': 8,  # clubs
    }
    INT_SUIT_TO_CHAR_SUIT = ' shxdxxxc'

    # for pretty printing
    PRETTY_SUITS = {
        0: '',
        1: '\u2660',  # spades
        2: '\u2764',  # hearts
        4: '\u2666',  # diamonds
        8: '\u2663',   # clubs
    }

    CORLOR_TO_INT_SUIT = {
        0: 1,     # 'b' ---> 'spades'
        1: 2,     # 'r' ---> 'hearts',
        2: 8,     # 'q' ---> 'clubs',
        3: 4,     # 'd' ---> 'diamonds',
        4: 0,     # ''  ---> '',
    }  #  原编码： COLORS = ("b", "r", "q", "d", "")

    CORLOR_FROM_INT_SUIT = dict([(v,k) for (k,v) in CORLOR_TO_INT_SUIT.items()])

    # hearts and diamonds
    PRETTY_REDS = [2, 4]

    @staticmethod
    def new(string):
        if Card.is_joker(string):
            return Card.CHAR_RANK_TO_INT_RANK[string]

        rank_char = string[:-1]
        suit_char = string[-1]
        rank_int = Card.CHAR_RANK_TO_INT_RANK[rank_char]
        suit_int = Card.CHAR_SUIT_TO_INT_SUIT[suit_char]

        suit = suit_int << 4
        return suit | rank_int

    @staticmethod
    def card_from_other_code(card_id):
        '''2018-12-26新增，用于从之前的扑克编码转换为现在的扑克编码'''
        rank_int = card_id % 13
        color_int = card_id // 13
        if color_int == 4:
            rank_int += 13
        suit_int = Card.CORLOR_TO_INT_SUIT[color_int]
        suit = suit_int << 4
        return suit | rank_int

    @staticmethod
    def card_ints_from_others(card_ids):
        card_ints = [Card.card_from_other_code(card_id) for card_id in card_ids]
        return Card.sort_cards_by_rank_int(card_ints)

    @staticmethod
    def card_to_other_code(card_int):
        '''2018-12-26新增，用于从现在的扑克编码转换为之前的扑克编码'''
        rank_int = Card.get_rank_int(card_int)
        suit_int = Card.get_suit_int(card_int)
        color_int = Card.CORLOR_FROM_INT_SUIT[suit_int]
        if color_int == 4:
            rank_int -= 13
        return (13 * color_int + rank_int)

    @staticmethod
    def card_ints_to_others(card_ids):
        return [Card.card_to_other_code(card_id) for card_id in card_ids]

    @staticmethod
    def card_ints_from_string(cards_str):
        return [Card.new(card_str) for card_str in cards_str.split('-')]

    @staticmethod
    def is_joker(string):
        return string in Card.STR_JOKERS

    @staticmethod
    def int_to_str(card_int):
        rank_int = Card.get_rank_int(card_int)
        suit_int = Card.get_suit_int(card_int)
        return Card.STR_RANKS[rank_int] + Card.INT_SUIT_TO_CHAR_SUIT[suit_int]

    @staticmethod
    def rank_int_to_str(card_int):
        rank_int = Card.get_rank_int(card_int)
        return Card.STR_RANKS[rank_int]

    @staticmethod
    def cards_without_suit(card_ints):
        no_suit_cards = [Card.rank_int_to_str(ci) for ci in card_ints]
        return '-'.join(no_suit_cards)

    @staticmethod
    def sort_cards_by_rank_int(card_ints):
        def cmp_card(x, y):
            return Card.get_rank_int(x) - Card.get_rank_int(y)
        if is_py3:
            return sorted(card_ints, key=cmp_to_key(cmp_card), reverse=True)
        return sorted(card_ints, cmp=cmp_card, reverse=True)

    @staticmethod
    def card_rank_to_real_card(card):
        """give a string card rank, return four cards with suit"""
        if Card.is_joker(card):
            return [card]
        return [card + suit for suit in ['s', 'h', 'd', 'c']]

    @staticmethod
    def get_rank_int(card_int):
        return (card_int) & 0xF

    @staticmethod
    def get_suit_int(card_int):
        return (card_int >> 4) & 0xF

    @staticmethod
    def int_to_pretty_str(card_int):
        """
        Prints a single card
        """

        color = False
        try:
            from termcolor import colored
            # for mac, linux: http://pypi.python.org/pypi/termcolor
            # can use for windows: http://pypi.python.org/pypi/colorama
            color = True
        except ImportError:
            pass

        # suit and rank
        suit_int = Card.get_suit_int(card_int)
        rank_int = Card.get_rank_int(card_int)

        # if we need to color red
        s = Card.PRETTY_SUITS[suit_int]
        if color and suit_int in Card.PRETTY_REDS:
            s = colored(s, "red")
        r = Card.STR_RANKS[rank_int]
        
        return '{0}{1}'.format(s,r)
        # return u" [ {} {} ]".format(r, s)

    @staticmethod
    def print_pretty_card(card_int):
        """
        Expects a single integer as input
        """
        print(Card.int_to_pretty_str(card_int))

    @staticmethod
    def print_pretty_cards(card_ints):
        """
        Expects a list of cards in integer form.
        """
        # output = " "
        # for i in range(len(card_ints)):
        #     c = card_ints[i]
        #     output += Card.int_to_pretty_str(c)
        #     if i != len(card_ints) - 1:
        #         output += ","
        # print(output)

        output = " "
        for i in range(len(card_ints)):
            c = card_ints[i]
            output += Card.int_to_pretty_str(c)
            if i != len(card_ints) - 1:
                output += ","
        print(output)

    @staticmethod
    def pretty_cards(card_ints):
        """
        Expects a list of cards in integer form.
        """
        # output = " "
        # for i in range(len(card_ints)):
        #     c = card_ints[i]
        #     output += Card.int_to_pretty_str(c)
        #     if i != len(card_ints) - 1:
        #         output += ","
        # print(output)

        output = ""
        for i in range(len(card_ints)):
            c = card_ints[i]
            output += Card.int_to_pretty_str(c)
            if i != len(card_ints) - 1:
                output += ","
        return output
