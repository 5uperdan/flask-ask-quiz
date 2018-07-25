from random import randint, choice
from flask import render_template
import yaml


def get_random_question(excluding):
    """ returns a tuple (question_index, question_text) 
        excluding: a list of indexes that shouldn't be resupplied
    """

    with open("templates.yaml", 'r') as stream:
        out = yaml.load(stream)

    questions = out['questions']

    # make a list of allowed indexes
    options = [x for x in range(0, len(questions)) if x not in excluding]
    if not options:
        return None, None

    index = choice(options)

    return index, out['questions'][index]


def get_answers_text(q_index):
    """ returns a tuple (correct_answer, correct_answer_text, combined_answers_text) """
    with open("templates.yaml", 'r') as stream:
        out = yaml.load(stream)
    
    correct_answer = 0
    correct_answer_text = ''
    answers_text = ''

    # get the answers which correspond to this question
    answers = out['answers'][3 * q_index: 3 * q_index + 3]
    # make a list of indexes
    possible_indexes = list(range(len(answers)))
    
    while possible_indexes:
        i = choice(possible_indexes)
        answer_option = (len(answers) - len(possible_indexes)) + 1 # ie. 1, 2, 3
        if i == 0: # correct answer
            correct_answer = answer_option
            correct_answer_text = answers[i]
        answers_text += '{}, {}. '.format(answer_option, answers[i])
        possible_indexes.remove(i)
    
    return correct_answer, correct_answer_text, answers_text
