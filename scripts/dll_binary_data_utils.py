import keras
import numpy as np
from doudizhu import Card, Doudizhu
from doudizhu.engine import sort_cards, str2cards
from keras.preprocessing.sequence import pad_sequences

from ctypes import *
import platform
from doudizhu import Doudizhu
import json

import os
cur_dir = os.path.dirname(os.path.abspath(__file__))

if platform.system() == 'Linux':
	_ = CDLL(os.path.join(cur_dir, 'ddz_engine.so'))
elif platform.system() == 'Windows':
	_ = CDLL(os.path.join(cur_dir, 'ddz_engine.dll'))

CT_SOLO = 0

CT_SOLO_CHAIN_5 = 1
CT_SOLO_CHAIN_6 = 2
CT_SOLO_CHAIN_7 = 3
CT_SOLO_CHAIN_8 = 4
CT_SOLO_CHAIN_9 = 5
CT_SOLO_CHAIN_10 = 6
CT_SOLO_CHAIN_11 = 7
CT_SOLO_CHAIN_12 = 8

CT_PAIR = 9
CT_PAIR_CHAIN_3 = 10
CT_PAIR_CHAIN_4 = 11
CT_PAIR_CHAIN_5 = 12
CT_PAIR_CHAIN_6 = 13
CT_PAIR_CHAIN_7 = 14
CT_PAIR_CHAIN_8 = 15
CT_PAIR_CHAIN_9 = 16
CT_PAIR_CHAIN_10 = 17

CT_TRIO = 18
CT_TRIO_CHAIN_2 = 19
CT_TRIO_CHAIN_3 = 20
CT_TRIO_CHAIN_4 = 21
CT_TRIO_CHAIN_5 = 22
CT_TRIO_CHAIN_6 = 23

CT_TRIO_SOLO = 24
CT_TRIO_SOLO_CHAIN_2 = 25
CT_TRIO_SOLO_CHAIN_3 = 26
CT_TRIO_SOLO_CHAIN_4 = 27
CT_TRIO_SOLO_CHAIN_5 = 28

CT_TRIO_PAIR = 29
CT_TRIO_PAIR_CHAIN_2 = 30
CT_TRIO_PAIR_CHAIN_3 = 31
CT_TRIO_PAIR_CHAIN_4 = 32

CT_FOUR_TWO_SOLO = 33
CT_FOUR_TWO_PAIR = 34

CT_BOMB = 35
CT_ROCKET = 36

CT_MAX = 37

CardSet = c_ulonglong

# card_set_t DE_cs_from_bin_str(const char* binary_str);
cs_from_bin_str = _.DE_cs_from_bin_str
cs_from_bin_str.argtypes = [c_char_p]
cs_from_bin_str.restype = CardSet

# card_set_t DE_cs_from_cards_str(const char* cards_str);
cs_from_cards_str = _.DE_cs_from_cards_str
cs_from_cards_str.argtypes = [c_char_p]
cs_from_cards_str.restype = CardSet

# int DE_cs_to_str(card_set_t cs, char* str, int size);
cs_to_str = _.DE_cs_to_str
cs_to_str.argtypes = [CardSet, POINTER(c_char), c_int]
cs_to_str.restype = c_int

# int DE_cs_get_count(card_set_t cs, int card014);
cs_get_count = _.DE_cs_get_count
cs_get_count.argtypes = [CardSet, c_int]
cs_get_count.restype = c_int

# card_set_t DE_cs_set_count(card_set_t cs, int card014, int count);
cs_set_count = _.DE_cs_set_count
cs_set_count.argtypes = [CardSet, c_int, c_int]
cs_set_count.restype = CardSet

# int DE_cs_get_total_count(card_set_t cs);
cs_get_total_count = _.DE_cs_get_total_count
cs_get_total_count.argtypes = [CardSet]
cs_get_total_count.restype = c_int

# int DE_cs_contain(card_set_t cs, card_set_t target);
cs_contain = _.DE_cs_contain
cs_contain.argtypes = [CardSet, CardSet]
cs_contain.restype = c_int

# void DE_init(const char* data_file);
init = _.DE_init
init.argtypes = [c_char_p]
init.restype = None

class valid_card_set(Structure):
    _fields_ = (
        ('cs', CardSet),
        ('type', c_uint),
    )

# int DE_list_valid_cards(card_set_t cs, DE_valid_card_set_t* vcs, int size);
list_valid_cards = _.DE_list_valid_cards
list_valid_cards.argtypes = [CardSet, POINTER(valid_card_set), c_int]
list_valid_cards.restype = c_int

# int DE_list_greater_cards(card_set_t cs, card_set_t candidate, DE_valid_card_set_t* vcs, int size);
list_greater_cards = _.DE_list_greater_cards
list_greater_cards.argtypes = [CardSet, CardSet, POINTER(valid_card_set), c_int]
list_greater_cards.restype = c_int

# int DE_min_max_search(card_set_t cs0, card_set_t cs1, card_set_t cs2, card_set_t cur, int owner, int next, card_set_t* best);
min_max_search = _.DE_min_max_search
min_max_search.argtypes = [CardSet, CardSet, CardSet, CardSet, c_int, c_int, POINTER(CardSet)]
min_max_search.restype = c_int

__all__ = [
    'CT_SOLO',
    'CT_SOLO_CHAIN_5',
    'CT_SOLO_CHAIN_6',
    'CT_SOLO_CHAIN_7',
    'CT_SOLO_CHAIN_8',
    'CT_SOLO_CHAIN_9',
    'CT_SOLO_CHAIN_10',
    'CT_SOLO_CHAIN_11',
    'CT_SOLO_CHAIN_12',
    'CT_PAIR',
    'CT_PAIR_CHAIN_3',
    'CT_PAIR_CHAIN_4',
    'CT_PAIR_CHAIN_5',
    'CT_PAIR_CHAIN_6',
    'CT_PAIR_CHAIN_7',
    'CT_PAIR_CHAIN_8',
    'CT_PAIR_CHAIN_9',
    'CT_PAIR_CHAIN_10',
    'CT_TRIO',
    'CT_TRIO_CHAIN_2',
    'CT_TRIO_CHAIN_3',
    'CT_TRIO_CHAIN_4',
    'CT_TRIO_CHAIN_5',
    'CT_TRIO_CHAIN_6',
    'CT_TRIO_SOLO',
    'CT_TRIO_SOLO_CHAIN_2',
    'CT_TRIO_SOLO_CHAIN_3',
    'CT_TRIO_SOLO_CHAIN_4',
    'CT_TRIO_SOLO_CHAIN_5',
    'CT_TRIO_PAIR',
    'CT_TRIO_PAIR_CHAIN_2',
    'CT_TRIO_PAIR_CHAIN_3',
    'CT_TRIO_PAIR_CHAIN_4',
    'CT_FOUR_TWO_SOLO',
    'CT_FOUR_TWO_PAIR',
    'CT_BOMB',
    'CT_ROCKET',
    'CT_MAX',

    'CardSet',

    'cs_from_bin_str',
    'cs_from_cards_str',
    'cs_to_str',
    'cs_get_count',
    'cs_set_count',
    'cs_get_total_count',
    'cs_contain',

    'init',
    'valid_card_set',
    'list_valid_cards',
    'list_greater_cards',
    'min_max_search',
]
def set_convert(result, n):
    avilable_cards = set()
    buf = create_string_buffer(128)
    for i in range(n):
        cs = result[i].cs
        type = result[i].type
        cs_to_str(cs, buf, 128)
        avilable_cards.add(buf.value.decode('utf-8'))
    return avilable_cards


init(os.path.join(cur_dir, 'all_cards.csv').encode('utf-8'))

def cards2vec(cards):
    """将字符窜形式的cards转换成固定长度的vector"""
    cardmap = {}
    for c in cards.split('-'):
        if c in cardmap:
            cardmap[c] += 1
        else:
            cardmap[c] = 1
    card_vec = [cardmap.get(c, 0) for c in Card.STR_RANKS]
    return card_vec


def get_role_cardcount_dict():
    """玩家角色+手上剩余牌的张数"""
    role_cardcount_dict = dict()
    value = 1
    for role in [0, 1, 2]:
        for cardcount in range(1, 20):  # 玩家出牌之后，手上剩余牌的张数，只能为1,2,3,...19
            key = '{0}-{1}'.format(role, cardcount)
            role_cardcount_dict[key] = value
            value += 1
    return role_cardcount_dict


def get_cardtype_weight_dict():
    """出牌类型+权值"""
    cardtype_weight_dict = dict()
    value = 1
    key = '{0}-{1}'.format('pass', 0)
    cardtype_weight_dict[key] = value
    value += 1
    for card_type, weight_cards in Doudizhu.TYPE_CARDS.items():
        for weight, no_suit_cards in weight_cards.items():
            key = '{0}-{1}'.format(card_type, weight)
            cardtype_weight_dict[key] = value
            value += 1
    return cardtype_weight_dict


def get_cardtype_dict():
    """出牌类型"""
    cardtype_to_id = dict()
    value = 0
    cardtype_to_id['pass'] = 1
    value += 1
    for card_type in Doudizhu.TYPE_CARDS:
        cardtype_to_id[card_type] = value
        value += 1
    return cardtype_to_id


def get_cards_dict():
    """对所有牌进行编号"""
    cards_to_id = dict()
    cards_to_id[''] = 1
    for id, cards in enumerate(Doudizhu.DATA):
        cards_to_id[cards] = id + 2
    return cards_to_id


def convert(vpx):
    """将传入的牌idlist转换为字符串形式"""
    card_ints = Card.card_ints_from_others(vpx)
    return Card.cards_without_suit(card_ints)


def get_type(cards):
    """获取手牌类型"""
    _, type_list = Doudizhu.check_card_type(cards)
    return type_list[0]


str_role_dict = {
    0: '地主0',
    1: '农民1',
    2: '农民2'
}

def replay(game_info):
    """回放对局进程"""
    player_roles = dict()
    pos_list = [pos for (pos, _, _) in game_info['历次出牌']]
    pos_list.append(game_info['玩家id'])
    first_pos = pos_list.index(game_info['地主id'])
    for index in range(min(3, len(pos_list))):
        player_roles[pos_list[index]] = (index - first_pos) % 3

    for idx, (pos, card_list, remain_count) in enumerate(game_info['历次出牌']):
        out_cards_group = Card.card_ints_from_others(card_list)
        out_cards = Card.cards_without_suit(out_cards_group)
        role = player_roles[pos]
        if out_cards != '':
            print('{0} 出牌: {1}，剩余{2}张'.format(str_role_dict[role], out_cards, remain_count))
        else:
            print('{0} 出牌: {1}，剩余{2}张'.format(str_role_dict[role], 'pass', remain_count))

    player_cards_group = Card.card_ints_from_others(game_info['玩家当前牌'])
    player_cards = Card.cards_without_suit(player_cards_group)
    role = player_roles[game_info['玩家id']]
    print('{0}当前牌: {1}'.format(str_role_dict[role], player_cards))


class DataProcessor:
    role_cardcount_dict = get_role_cardcount_dict()
    max_value = max(role_cardcount_dict.values())
    role_cardcount_dict['所有已出牌'] = max_value + 1
    role_cardcount_dict['底牌'] = max_value + 2
    role_cardcount_dict['玩家手上牌'] = max_value + 3

    cardtype_weight_dict = get_cardtype_weight_dict()
    max_value = max(cardtype_weight_dict.values())
    cardtype_weight_dict['所有已出牌'] = max_value + 1
    cardtype_weight_dict['底牌'] = max_value + 2
    cardtype_weight_dict['玩家手上牌'] = max_value + 3

    cardtype_to_id = get_cardtype_dict()
    cards_to_id = get_cards_dict()
    id_to_cards = dict([(value, key) for (key, value) in cards_to_id.items()])

    def encode_avilables_and_select(self, data):
        """
            枚举玩家当前允许出的牌，并依次编号
            将实际的选择出牌转换为 其在当前允许所有出牌中的index.
        """
        if data['待跟牌'] != '':
            target = cs_from_cards_str(data['待跟牌'].encode('utf-8'))
            candidate = cs_from_cards_str(data['玩家手上牌'].encode('utf-8'))
            result = (valid_card_set * 600)()
            n = list_greater_cards(target, candidate, result, c_int(600))
            avilable_cards = set_convert(result, n)
            avilable_cards.add('')
        else:
            candidate = cs_from_cards_str(data['玩家手上牌'].encode('utf-8'))
            result = (valid_card_set * 600)()
            n = list_valid_cards(candidate, result, c_int(600))
            avilable_cards = set_convert(result, n)

        all_cards = list(avilable_cards)
        all_cards_ids = [self.cards_to_id[cards] for cards in all_cards]

        sorted_cards = '-'.join(sort_cards(str2cards(data['具体出牌'])))
        output_id = all_cards.index(sorted_cards)
        return all_cards_ids, output_id

    def prepare_input_data(self, data):
        """
                    历次出牌信息：
                        (玩家角色-手上剩余牌张数的key), (出牌类型-weight的key), 具体出牌
                    其他信息：
                        (所有已出牌的key),            (所有已出牌的key),      具体牌
                        (底牌的key),                 (底牌的key),           具体牌
                        (玩家手上牌的key牌),          (玩家手上牌的key),      具体牌
                    出牌:
                        具体出牌类型、具体出牌
                """
        input_data = []
        for item in data['历次出牌']:
            role_cardcount_key = '{0}-{1}'.format(item['玩家角色'], item['手上剩余张数'])
            cardtype_weight_key = '{0}-{1}'.format(item['出牌类型'][0], item['出牌类型'][1])
            input_data.append([self.role_cardcount_dict[role_cardcount_key],
                               self.cardtype_weight_dict[cardtype_weight_key]]
                              + cards2vec(item['具体出牌']))

        role_cardcount_key = '所有已出牌'
        cardtype_weight_key = '所有已出牌'
        input_data.append([self.role_cardcount_dict[role_cardcount_key],
                           self.cardtype_weight_dict[cardtype_weight_key]]
                          + cards2vec(data['所有已出牌']))

        role_cardcount_key = '底牌'
        cardtype_weight_key = '底牌'
        input_data.append([self.role_cardcount_dict[role_cardcount_key],
                           self.cardtype_weight_dict[cardtype_weight_key]]
                          + cards2vec(data['底牌']))

        role_cardcount_key = '玩家手上牌'
        cardtype_weight_key = '玩家手上牌'
        input_data.append([self.role_cardcount_dict[role_cardcount_key],
                           self.cardtype_weight_dict[cardtype_weight_key]]
                          + cards2vec(data['玩家手上牌']))
        return input_data

    def prepare_data(self, srcfile, desfile):
        fs = open(srcfile, 'r', encoding='utf-8', errors='ignore')
        fw = open(desfile, 'w', encoding='utf-8', newline='', errors='ignore')
        for count, line in enumerate(fs):
            if count % 10000 == 0:
                print(srcfile, '---', count)
            data = json.loads(line.strip())
            input_data = self.prepare_input_data(data)
            all_cards_ids, output_id = self.encode_avilables_and_select(data)
            prepared_data = {
                'input_data': input_data,
                'all_cards_ids': all_cards_ids,
                'output_id': output_id
            }
            fw.write(json.dumps(prepared_data, ensure_ascii=False) + '\n')

    def binary_convert(self, input_data, max_length=50):
        x1, x2, x3 = [], [], []
        lenS = len(input_data)
        for row in input_data:
            x1.append(row[0])
            x2.append(row[1])
            new_e = [[1 if e >= k else 0 for k in range(1, 5)] for e in row[2:]]
            x3.append(new_e)
        x1 = np.array(x1, dtype=np.float32)
        x2 = np.array(x2, dtype=np.float32)
        x3 = np.array(x3, dtype=np.float32)
        if lenS > max_length:
            x1 = x1[lenS - max_length: lenS]
            x2 = x2[lenS - max_length: lenS]
            x3 = x3[lenS - max_length: lenS, :, :]
        elif lenS < max_length:
            x1 = np.hstack((np.zeros(shape=(max_length - lenS)), x1))
            x2 = np.hstack((np.zeros(shape=(max_length - lenS)), x2))
            pad_data = np.zeros(shape=(max_length-lenS, x3.shape[1], x3.shape[2]))
            x3 = np.vstack((pad_data, x3))
        return x1, x2, x3

    def generate_data(self, filename, max_length=50, pad_length=600, batch_size=256):
        while True:
            input1, input2, input3, input4, outputs = [], [], [], [], []
            fs = open(filename, 'r', encoding='utf-8', errors='ignore')
            batch_count = 0
            for line in fs:
                prepared_data = json.loads(line.strip())
                x1, x2, x3 = self.binary_convert(prepared_data['input_data'], max_length=max_length)
                input1.append(x1)
                input2.append(x2)
                input3.append(x3)
                all_cards_ids = prepared_data['all_cards_ids']
                output_id = prepared_data['output_id']
                input4.append(all_cards_ids)
                outputs.append(output_id)

                batch_count += 1
                if batch_count == batch_size:
                    pad_input4 = pad_sequences(input4, pad_length, padding='post')
                    outputs = keras.utils.to_categorical(outputs, num_classes=pad_length)
                    yield ([np.asarray(input1), np.asarray(input2),
                            np.asarray(input3), pad_input4], outputs)
                    batch_count = 0
                    input1, input2, input3, input4, outputs = [], [], [], [], []

    def prepare_data_for_predict(self, game_info, max_length=50):
        """
            为模型的预测准备输入数据。

            历次出牌信息：
                (玩家角色-手上剩余牌张数的key), (出牌类型-weight的key), 具体出牌
            其他信息：
                (所有已出牌的key),            (所有已出牌的key),      具体牌
                (底牌的key),                 (底牌的key),           具体牌
                (玩家手上牌的key牌),          (玩家手上牌的key),      具体牌
            出牌:
                具体出牌类型、具体出牌

            :returns  玩家角色               ---->  用于明确需调用哪个模型。
                      formed_data           ---->  当前牌局信息，特征抽取之用。
                      avilable_cards_ids    ---->  可出牌的id列表。
        """

        for field in ['玩家id', '玩家当前牌', '历次出牌', '地主id', '底牌']:
            assert field in game_info

        # 获取玩家id --> 玩家角色
        player_roles = dict()
        pos_list = [pos for (pos, _, _) in game_info['历次出牌']]
        pos_list.append(game_info['玩家id'])
        first_pos = pos_list.index(game_info['地主id'])
        for index in range(min(3, len(pos_list))):
            player_roles[pos_list[index]] = (index - first_pos) % 3

        input_data = []

        pass_count = 0
        last_out_cards = ''
        all_out_cards = []
        for (pos, card_list, remain_card_count) in game_info['历次出牌']:
            role_cardcount_key = '{0}-{1}'.format(player_roles[pos], remain_card_count)
            if len(card_list) == 0:
                cards_without_suit = ''
                card_type = ('pass', 0)
                pass_count += 1
            else:
                cards_without_suit = convert(card_list)
                card_type = get_type(cards_without_suit)
                last_out_cards = cards_without_suit
                pass_count = 0

            cardtype_weight_key = '{0}-{1}'.format(card_type[0], card_type[1])
            input_data.append([self.role_cardcount_dict[role_cardcount_key],
                               self.cardtype_weight_dict[cardtype_weight_key]]
                              + cards2vec(cards_without_suit))
            all_out_cards.extend(card_list)

        if pass_count == 2:
            last_out_cards = ''

        role_cardcount_key = '所有已出牌'
        cardtype_weight_key = '所有已出牌'
        all_out_cards_without_suit = convert(all_out_cards)
        input_data.append([self.role_cardcount_dict[role_cardcount_key],
                           self.cardtype_weight_dict[cardtype_weight_key]]
                          + cards2vec(all_out_cards_without_suit))

        role_cardcount_key = '底牌'
        cardtype_weight_key = '底牌'
        extra_cards_without_suit = convert(game_info['底牌'])
        input_data.append([self.role_cardcount_dict[role_cardcount_key],
                           self.cardtype_weight_dict[cardtype_weight_key]]
                          + cards2vec(extra_cards_without_suit))

        role_cardcount_key = '玩家手上牌'
        cardtype_weight_key = '玩家手上牌'
        hand_cards_without_suit = convert(game_info['玩家当前牌'])
        input_data.append([self.role_cardcount_dict[role_cardcount_key],
                           self.cardtype_weight_dict[cardtype_weight_key]]
                          + cards2vec(hand_cards_without_suit))

        x1, x2, x3 = self.binary_convert(input_data, max_length=max_length)

        # 枚举当前玩家所有可出的牌
        if last_out_cards != '':
            target = cs_from_cards_str(last_out_cards.encode('utf-8'))
            candidate = cs_from_cards_str(hand_cards_without_suit.encode('utf-8'))
            result = (valid_card_set * 600)()
            n = list_greater_cards(target, candidate, result, c_int(600))
            avilable_cards = set_convert(result, n)
            avilable_cards.add('')
        else:
            candidate = cs_from_cards_str(hand_cards_without_suit.encode('utf-8'))
            result = (valid_card_set * 600)()
            n = list_valid_cards(candidate, result, c_int(600))
            avilable_cards = set_convert(result, n)

        avilable_cards_ids = list(avilable_cards)
        avilable_cards_ids = [self.cards_to_id[cards] for cards in avilable_cards_ids]

        return player_roles[game_info['玩家id']], x1, x2, x3, avilable_cards_ids


def work(srcfile, desfile):
    processor = DataProcessor()
    processor.prepare_data(srcfile, desfile)


if __name__ == '__main__':
    hand_cards_without_suit = 'CJ-BJ-J-10-9-9-8-8-6-5-5-5-3-3-3-3'
    candidate = cs_from_cards_str(hand_cards_without_suit.encode('utf-8'))
    result = (valid_card_set * 600)()
    n = list_valid_cards(candidate, result, c_int(600))
    avilable_cards = set_convert(result, n)
    print(avilable_cards)
