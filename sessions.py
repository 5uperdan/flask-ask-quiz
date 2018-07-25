""" 
This is something like a singleton
"""

QUESTIONS_GIVEN = "answered_questions"
QUIZ_STARTED = "quiz_started"
CORRECT_OPTION = "correct_option"
CORRECT_TEXT = "correct_text"
SCORE = "score"


def has_quiz_started(session):
    """ Returns a boolean indicating if the quiz has started """
    return session.attributes.get(QUIZ_STARTED, False)

def set_quiz_status(session, started):
    """ Sets the quiz's "started" status """
    session.attributes[QUIZ_STARTED] = started

def get_answered_questions(session):
    """ Gets a list of question indexes that have already been asked this session """
    return session.attributes.get(QUESTIONS_GIVEN, [])

def add_answered_question(session, question_index):
    """ Adds answered question to list of indexes """
    answered_questions = get_answered_questions(session)
    answered_questions.append(question_index)
    session.attributes[QUESTIONS_GIVEN] = answered_questions

def clear_answered_questions(session):
    """ Clears the list of already asked question indexes """
    session.attributes[QUESTIONS_GIVEN] = []

def store_correct_option(session, value):
    """ Stores the correct answer """
    session.attributes[CORRECT_OPTION] = value

def get_correct_option(session):
    """ Returns the correct answer """
    return session.attributes[CORRECT_OPTION]

def store_correct_text(session, value):
    """ Stores the correct answer's text """
    session.attributes[CORRECT_TEXT] = value

def get_correct_text(session):
    """ Returns the correct answer's text """
    return session.attributes[CORRECT_TEXT]

def get_score(session):
    """ Returns the player's score """
    return session.attributes.get(SCORE, 0)

def clear_score(session):
    """ Resets the player's score """
    session.attributes[SCORE] = 0

def increment_score(session):
    """ Increases the player's score by one """
    session.attributes[SCORE] = session.attributes.get(SCORE, 0) + 1
    return get_score(session)

def clear_answer(session):
    """ Resets the answer states """
    store_correct_option(session, None)
    store_correct_text(session, None)
