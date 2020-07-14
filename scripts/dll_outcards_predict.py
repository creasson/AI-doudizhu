import os, sys
cur_dir = os.path.dirname(os.path.abspath(__file__))
doudizhu_dir = os.path.join(cur_dir, 'doudizhu')
sys.path.append(cur_dir)
sys.path.append(doudizhu_dir)

import numpy as np
import tensorflow as tf
import dll_binary_data_utils
from keras.preprocessing.sequence import pad_sequences

class OutCards_Predictor:

    def __init__(self, pbmodel_paths_dict):

        self.processor = dll_binary_data_utils.DataProcessor()
        """创建graph和session"""
        self.pred_probs = dict()
        self.graph = tf.Graph()
        self.session = tf.Session(graph=self.graph)

        with self.session.as_default():
            with self.graph.as_default():
                for role in [0, 1, 2]:
                    with tf.gfile.FastGFile(pbmodel_paths_dict[role], 'rb') as fs:
                        graph_def = tf.GraphDef()
                        graph_def.ParseFromString(fs.read())
                        tf.import_graph_def(graph_def, name='role{0}'.format(role))
                    self.pred_probs[role] = self.graph.get_tensor_by_name(
                        name='role{0}/activation_1/Softmax:0'.format(role))


    def predict(self, game_info, pad_length=600):
        role, x1, x2, x3, avilable_cards_ids = self.processor.prepare_data_for_predict(game_info)
        pad_input4 = pad_sequences([avilable_cards_ids], pad_length, padding='post')
        feed_dict = {
            'role{0}/input_1:0'.format(role): np.asarray([x1]),
            'role{0}/input_2:0'.format(role): np.asarray([x2]),
            'role{0}/input_3:0'.format(role): np.asarray([x3]),
            'role{0}/input_4:0'.format(role): pad_input4,
        }
        pred_probs = self.session.run(self.pred_probs[role], feed_dict=feed_dict)[0]
        avilable_probs = pred_probs[0:len(avilable_cards_ids)]
        max_prob_index = np.argmax(avilable_probs)
        return self.processor.id_to_cards[avilable_cards_ids[max_prob_index]]

if __name__ == '__main__':
    game_info = {
        "玩家当前牌": [53, 52, 21, 7, 32, 6, 44, 31, 16, 41, 28, 15, 39, 26, 13, 0],
        "地主id": 0,
        "玩家id": 0,
        "历次出牌": [[0, [14, 1], 18], [1, [33, 20], 15], [2, [], 17], [0, [37, 11], 16], [1, [], 15], [2, [], 17]],
        "底牌": [7, 32, 11],
        "桌面上的牌": [14, 1, 33, 20, 37, 11]
    }

    dll_binary_data_utils.replay(game_info)
    pbmodel_paths_dict = {
        0: os.path.join(os.path.dirname(cur_dir), 'model', 'role0_epoch6-acc0.9581.pb'),
        1: os.path.join(os.path.dirname(cur_dir), 'model', 'role1_epoch8-acc0.9582.pb'),
        2: os.path.join(os.path.dirname(cur_dir), 'model', 'role2_epoch7-acc0.9518.pb'),
    }

    predictor = OutCards_Predictor(pbmodel_paths_dict)
    out_cards = predictor.predict(game_info)
    print('预测出牌：', out_cards)