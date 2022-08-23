import preprocessing
import sentimental

from gensim import corpora
from gensim.models.ldamodel import LdaModel
from gensim.models.callbacks import CoherenceMetric
from gensim.models.callbacks import PerplexityMetric
from gensim.test.utils import datapath

def inference_model(input):

    # load positive model
    pos_dict = corpora.Dictionary.load('data/dictionary/pos_dict.imdict')
    pos_corp = corpora.MmCorpus('data/dictionary/pos_corpus')
    pos_model = LdaModel.load('pos_model')

    # load negative model
    neg_dict = corpora.Dictionary.load('data/dictionary/neg_dict.imdict')
    neg_corp = corpora.MmCorpus('data/dictionary/neg_corpus')
    neg_model = LdaModel.load('neg_model')

    # sample = [
    #     '비싸요 ㅠㅠ 근데 음식은 맛있습니다', '최고예요 재방문 할 겁니다. 존맛 대박 맛있어용',
    #     '쓰레기 같아요. 고성방가 엄청 하고.. 다시는 안와요', '가성비 별로. 맛은 있음'
    #     ]

    # preprocessing (cleaning data & tokenizing data)
    processed_data = preprocessing.tokenize(input)

    num_topics = 4
    num_review = len(input)
    prob_list = []
    topic_score_list = []
    score_list = []
    for data in processed_data:
        score = sentimental.get_senti_score(data)
        score_list.append(score)
        # Inference different models based on scores
        '''
            Topic 0 -> SERVICE: about hygiene, reception, ...
            Topic 1 -> FOOD: about food, menu, ...
            Topic 2 -> CONVINIENCE: about the convenience of the restaurant, ...
            Topic 3 -> PRICE: about price, cost-effectiveness..
        '''

        if score > 0:
            prob_per_topic = pos_model[(pos_dict.doc2bow(data))]
            topic_score = []
            prob = []
            for value in prob_per_topic:
                prob.append(round(float(value[1]), 2))
                topic_score.append(float(value[1]) * score)
            
            prob_list.append(prob)

        else:
            prob_per_topic = neg_model[(neg_dict.doc2bow(data))]
            # switch scores
            new_prob_per_topic = [0] * len(prob_per_topic)
            new_prob_per_topic.insert(0, prob_per_topic[2])
            new_prob_per_topic.insert(1, prob_per_topic[3])
            new_prob_per_topic.insert(2, prob_per_topic[0])
            new_prob_per_topic.insert(3, prob_per_topic[1])

            if score == 0:
                score = - 1

            topic_score = []
            prob = []
            for value in new_prob_per_topic[:4]:
                prob.append(round(float(value[1]), 2))
                topic_score.append(float(value[1]) * score)
            
            prob_list.append(prob)

        # normalization: min-max
        max_value = max(topic_score)
        min_value = min(topic_score)
        new_topic_score = [0] * num_topics
        for i in range(len(new_topic_score)):
            new_topic_score[i] = 5 * (topic_score[i] - min_value) / (max_value - min_value)

        topic_score_list.append(new_topic_score)


        print(f'review: {data} \n score: {score}')
        print(f'topic_score: {new_topic_score} \n -----------')


    # sum topic_score
    total_topic_score = [0] * num_topics
    for i in range(len(total_topic_score)):
        for topic_score in topic_score_list:
            total_topic_score[i] += topic_score[i]
        total_topic_score[i] = round(total_topic_score[i] / num_review, 2)
    print(f'total score: {total_topic_score}')


    return prob_list, processed_data, score_list, total_topic_score

