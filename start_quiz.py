import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session, request, context

from utilities import (get_random_question, get_answers_text)

from sessions import (has_quiz_started, set_quiz_status, 
                      get_answered_questions, add_answered_question, clear_answered_questions, 
                      store_correct_option, get_correct_option, 
                      store_correct_text, get_correct_text,
                      get_score, clear_score, increment_score, clear_answer)


app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)


@ask.launch
def application_welcome():
    """ Entry point for a new game """
    welcome_msg = '{} {}'.format(render_template('welcome'), render_template('activity_selection'))
    return question(welcome_msg).reprompt(render_template('activity_selection'))


@ask.intent("GiveInfo")
def give_info():
    """ Reads facts and prompts user, if they want to start quiz or hear facts """
            
    # if quiz has started this request for info is unexpected
    if has_quiz_started(session):
        return response_out_of_place()

    facts = render_template('facts')
    activity_selection = render_template('activity_selection')
    msg = '{}... {}'.format(facts, activity_selection)
    return question(msg).reprompt(render_template('activity_selection'))


@ask.intent("StartTheQuiz")
def start_quiz():
    """ Starts the quiz """
    # if quiz has already started this request for info is unexpected
    if has_quiz_started(session):
        return response_out_of_place()

    set_quiz_status(session, started=True)
    return send_quiz_question()
    

@ask.intent("ContinueQuizYes")
def continue_quiz_yes():
    """ Continues the quiz """
    # quiz must be running and not expecting an answer option
    if not has_quiz_started(session) or get_correct_option(session) is not None:
        return response_out_of_place()

    return send_quiz_question()

@ask.intent("ContinueQuizNo")
def continue_quiz_no():
    """ Stops the quiz """
    # quiz must be running and not expecting an answer option
    if not has_quiz_started(session) or get_correct_option(session) is not None:
        return response_out_of_place()

    clear_answered_questions(session)
    clear_score(session)
    set_quiz_status(session, started=False)
    return application_welcome()


def send_quiz_question():
    """ Sends a quiz question """
    already_asked = get_answered_questions(session)
    q_index, q_text = get_random_question(already_asked)
    if q_index is None:
        # all questions answered
        return statement(render_template('complete',
                         score=get_score(session)) + render_template('goodbye'))


    add_answered_question(session, q_index)
    correct_option, correct_text, a_text = get_answers_text(q_index)
    store_correct_option(session, correct_option)
    store_correct_text(session, correct_text)
    msg = '{} {}'.format(q_text, a_text)
    return question(msg).reprompt(msg)


@ask.intent("AnswerQuizQuestion", convert={'option': int})
def answer(option):
    correct_option = get_correct_option(session)
    
    if correct_option == None:
        return response_out_of_place()

    if option == correct_option:
        increment_score(session)
        msg = render_template('win', score=get_score(session))
    else:
        msg = render_template('lose',
                              correct_option=get_correct_option(session),
                              correct_text=get_correct_text(session))

    clear_answer(session)
    msg += ' ' + render_template('continue_prompt')
    return question(msg).reprompt(render_template('continue_prompt'))


def response_out_of_place():
    """ returns a request for a user to repeat themselves """
    question_text = render_template('repeat')
    return question(question_text).reprompt(question_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('goodbye')
    return statement(bye_text)


@ask.session_ended
def session_ended():
    """ ends session """
    return "{}", 200


if __name__ == '__main__':
    app.run(debug=True)