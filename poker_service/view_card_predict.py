import os, sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(cur_dir)
scripts_dir = os.path.join(project_dir, 'scripts')
sys.path.append(project_dir)
sys.path.append(scripts_dir)

from django.http import JsonResponse
from django.views.decorators import csrf
from dll_outcards_predict import OutCards_Predictor
from copy import deepcopy
import json

MODEL_PATH_CFG = {
    0: os.path.join(project_dir, 'model', 'role0_epoch6-acc0.9581.pb'),
    1: os.path.join(project_dir, 'model', 'role1_epoch8-acc0.9582.pb'),
    2: os.path.join(project_dir, 'model', 'role2_epoch7-acc0.9518.pb'),
}

predictor = OutCards_Predictor(MODEL_PATH_CFG)

cardmap_dict = {
    '3': [0, 13, 26, 39],
    '4': [1, 14, 27, 40],
    '5': [2, 15, 28, 41],
    '6': [3, 16, 29, 42],
    '7': [4, 17, 30, 43],
    '8': [5, 18, 31, 44],
    '9': [6, 19, 32, 45],
    '10': [7, 20, 33, 46],
    'J': [8, 21, 34, 47],
    'Q': [9, 22, 35, 48],
    'K': [10, 23, 36, 49],
    'A': [11, 24, 37, 50],
    '2': [12, 25, 38, 51],
    'BJ': [52],
    'CJ': [53]
}

def pick_card(player_cards, str_predict_out_cards):
    """从当前玩家手上的牌选择给定牌"""
    selected_card_list = []
    if str_predict_out_cards == '':
        return selected_card_list
    player_cards_copy = deepcopy(player_cards)
    for card in str_predict_out_cards.split('-'):
        for cid in cardmap_dict[card]:
            if cid in player_cards_copy:
                selected_card_list.append(cid)
                player_cards_copy.remove(cid)
                break
    return selected_card_list

@csrf.csrf_exempt
def out_card_predict(request):

    if request.POST:
        input_string = request.POST['q']
    elif request.GET:
        input_string = request.GET['q']

    try:
        game_info = json.loads(input_string)
        str_predict_out_cards = predictor.predict(game_info)
        player_cards = game_info['玩家当前牌']
        out_card_dict = {
            'card_string': str_predict_out_cards,
            'card_indexs': pick_card(player_cards, str_predict_out_cards),
        }
        return JsonResponse(out_card_dict, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)

    except Exception as e:
        err_info = {
            'input': input_string,
            'error': str(e)
        }
        return JsonResponse(err_info, json_dumps_params={'ensure_ascii': False, 'indent': 4}, safe=False)