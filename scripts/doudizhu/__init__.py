# -*- coding: utf-8 -*-

#          //                            //  //            //
#     //////    ////    //    //    //////      ////////  //////    //    //
#  //    //  //    //  //    //  //    //  //      //    //    //  //    //
# //    //  //    //  //    //  //    //  //    //      //    //  //    //
#  //////    ////      //////    //////  //  ////////  //    //    //////

"""
斗地主引擎
~~~~~~~~~~
usage:
    >>> import doudizhu
    >>> cards_groups = doudizhu.new_game()
    >>> cards_groups
    [[44, 28, 27, ...], [14, 75, 139, ...], [13, 140, 76, ...], [73, 40, 136]]
    >>> for cards_group in cards_groups:
    ...     doudizhu.Card.print_pretty_cards(cards_group)
    ...
      [ 2 ❤ ] , [ 2 ♠ ] , [ A ♠ ] , ...
      [ CJ  ] , [ A ♦ ] , [ A ♣ ] , ...
      ...

    >>> chain = doudizhu.Card.card_ints_from_string('3c-4d-5h-6s-7s-8h-9h')
    >>> doudizhu.check_card_type(chain)
    (True, [('solo_chain_7', 0)])

    >>> doudizhu.cards_greater(chain[1:7], chain[:6])
    (True, 'solo_chain_6')

    >>> doudizhu.list_greater_cards(chain, cards_group[0])
    {'solo_chain_7': [[39, 38, 37, 132, 19, 34, 33], [72, 39, 38, 37, 132, 19, 34]]}
"""

import random
from .engine import Doudizhu
from .card import Card


Doudizhu.init_doudizhu_dict()


def new_game():
    """随机打乱54张牌，分成四组:17,17,17,3"""
    all_cards = []
    for c in Card.STR_RANKS:
        all_cards.extend(Card.card_rank_to_real_card(c))

    all_cards = [Card.new(card_str) for card_str in all_cards]
    random.seed()
    result = []
    for group_idx in range(3):
        group = []
        for card_idx in range(17):
            card = random.choice(all_cards)
            all_cards.remove(card)
            group.append(card)
        result.append(group)

    result.append(all_cards)
    result = [Card.sort_cards_by_rank_int(cards) for cards in result]
    return result


def check_card_type(cards):
    """判断手牌是否符合斗地主规则
    cards: Card类型的列表
    return: bool, type
    """
    cards_no_suit = Card.cards_without_suit(cards)
    return Doudizhu.check_card_type(cards_no_suit)


def cards_greater(cards_x, cards_y):
    """判断手牌cards_x 是否大于cards_y
    cards_x/y: Cards类型的列表
    return: bool, cards_x 的牌型
    """
    cards_x_no_suit = Card.cards_without_suit(cards_x)
    cards_y_no_suit = Card.cards_without_suit(cards_y)
    return Doudizhu.cards_greater(cards_x_no_suit, cards_y_no_suit)

def laizi_cards_greater(laizi, cards_x, laizi_cards_x, cards_y, laizi_cards_y):
    """判断癞子牌laizi_cards_x 是否大于laizi_cards_y
        cards_x/y: Cards类型的列表
        return: bool, cards_x 的牌型
        在正常牌比较的基础上增加 纯癞子炸弹 > 硬炸 > 软炸弹 的比较规则。
    """
    laizi_cards_x_no_suit = Card.cards_without_suit(laizi_cards_x)
    laizi_cards_y_no_suit = Card.cards_without_suit(laizi_cards_y)
    ok, type_x = Doudizhu.check_card_type(laizi_cards_x_no_suit)
    if not ok:
        return False, '{}: {}'.format(laizi_cards_x_no_suit, type_x)

    ok, type_y = Doudizhu.check_card_type(laizi_cards_y_no_suit)
    if not ok:
        return False, '{}: {}'.format(laizi_cards_y_no_suit, type_y)

    for tx in type_x:
        for ty in type_y:
            # 如果都是炸弹，需要判断是否是：纯癞子炸弹，硬炸，软炸弹
            if tx[0] == 'bomb' and ty[0] == 'bomb':
                # 炸弹类型判断
                cards_x_no_suit = Card.cards_without_suit(cards_x)
                if cards_x_no_suit == '-'.join([laizi] * 4):
                    x_bomb_type = 3     # 纯癞子炸弹
                elif cards_x_no_suit.find(laizi) == -1:
                    x_bomb_type = 2     # 硬炸弹
                else:
                    x_bomb_type = 1     # 软炸弹

                cards_y_no_suit = Card.cards_without_suit(cards_y)
                if cards_y_no_suit == '-'.join([laizi] * 4):
                    y_bomb_type = 3     # 纯癞子炸弹
                elif cards_y_no_suit.find(laizi) == -1:
                    y_bomb_type = 2     # 硬炸弹
                else:
                    y_bomb_type = 1     # 软炸弹

                if x_bomb_type > y_bomb_type:
                    return True, tx[0]
                elif x_bomb_type < y_bomb_type:
                    return False, tx[0]
                else:                   # 炸弹类型相同时，大小比较正常进行。
                    pass
            flag = Doudizhu.type_greater(tx, ty)
            if not isinstance(flag, ValueError) and flag > 0:
                return True, tx[0]
    return False, tx[0]

def list_greater_cards(cards_target, cards_candidate):
    """ 对于目标牌组合cards_target
    从候选牌cards_candidate中找出所有可以压制它的牌型
    不区分花色，返回结果是一个字典{card_type:[greater_cards,],}
    """
    ct_no_suit = Card.cards_without_suit(cards_target)
    cc_no_suit = Card.cards_without_suit(cards_candidate)
    cards_gt = Doudizhu.list_greater_cards(ct_no_suit, cc_no_suit)

    def render_suit(cards, candidate):
        result = set()
        candidate = set(candidate)
        for card in cards.split('-'):
            cards_suit = [Card.new(cs) for cs in
                          Card.card_rank_to_real_card(card)]
            for card_int in cards_suit:
                if card_int in candidate and card_int not in result:
                    result.add(card_int)
                    break
        return result

    result = {}
    for card_type, cards_list in iter(cards_gt.items()):
        result[card_type] = []
        for cards in cards_list:
            cards_with_suit = render_suit(cards, cards_candidate)
            sorted_cards = Card.sort_cards_by_rank_int(list(cards_with_suit))
            result[card_type].append(sorted_cards)

    return result

def list_valid_cards(cards_candidate):
    """
    从候选牌cards_candidate中找出所有有效的出牌
    """
    cc_no_suit = Card.cards_without_suit(cards_candidate)
    valid_cards = Doudizhu.list_valid_cards(cc_no_suit)

    def render_suit(cards, candidate):
        result = set()
        candidate = set(candidate)
        for card in cards.split('-'):
            cards_suit = [Card.new(cs) for cs in
                          Card.card_rank_to_real_card(card)]
            for card_int in cards_suit:
                if card_int in candidate and card_int not in result:
                    result.add(card_int)
                    break
        return result

    result = {}
    for card_type, cards_list in iter(valid_cards.items()):
        result[card_type] = []
        for cards in cards_list:
            cards_with_suit = render_suit(cards, cards_candidate)
            sorted_cards = Card.sort_cards_by_rank_int(list(cards_with_suit))
            result[card_type].append(sorted_cards)

    return result

__all__ = ['Card', 'new_game', 'check_card_type', 'cards_greater',
           'laizi_cards_greater', 'list_greater_cards', 'list_valid_cards']
