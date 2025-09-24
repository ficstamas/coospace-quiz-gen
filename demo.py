from coospace_quiz_gen import *


# Single choice question
q = SingleChoiceQuestion("Random Question text1", total_score=2.0)
# adding answers
q.add_option("<p>Answer 1</p>")
q.add_option("<p>Answer 2</p>", valid=True)  # valid=True marks the correct answer
q.add_option("<p>Answer 3</p>")

# Multi choice question
q2 = MultiChoiceQuestion("Random Question text2", total_score=2.0)
# adding answers
q2.add_option("<p>Answer 1</p>")
q2.add_option("<p>Answer 2</p>", valid=True)  # valid=True marks the correct answer
q2.add_option("<p>Answer 3</p>", valid=True)  # valid=True marks the correct answer

# Short text question
q3 = ShortTextQuestion("Random Question text3", total_score=2.0)
# adding accepted answers
q3.add_answer("1")
q3.add_answer("2")
q3.add_answer("3")

# creating an essay
q4 = EssayQuestion("Random Question text4", total_score=2.0)

# True-False questions
q5 = TrueFalseQuestion("Random Question text5", total_score=2.0)
# there are two types: True/False (0) and Yes/No (1), these values can be provided by the constructor too (see later)
q5.set_answer_type_true_false()
# we can set the correct answer by the following or `q5.set_answer_false_or_no()`
# this can be provided by the constructor too where True=1 and False=2 (hate the coospace api not me)
q5.set_answer_true_or_yes()
# or
q6 = TrueFalseQuestion("Random Question text6", total_score=2.0, answer_id=1)

q7 = TrueFalseQuestion("Random Question text7", total_score=2.0, answer_type=1, answer_id=1)
q7.set_answer_false_or_no()

# Number type question
q8 = NumberQuestion("Random Question text8", total_score=2.0)
# we can add several options at once
# add_option_percent: adds a question with an expected value within the provided percen [value +/(percent)]
# add_option_interval: adds a question with an expected value within range [from, to]
q8.add_option_percent("Answer", 10, 1)
q8.add_option_percent("Answer 1", 10, 1)
q8.add_option_interval("Answer interval 1", 10, 100)
q8.add_option_percent("Answer 2", 10, 1)


# Random question block
block = RandomBlock("Random Question text", n_selected_question=2)
# we can add existing questions to it
block.add_question(q)
block.add_question(q2)
block.add_question(q3)
block.add_question(q4)


# final test
test = Test()

# we can add questions
test.add_question(q5)
test.add_question(q6)
test.add_question(q7)
test.add_question(q8)
# and random blocks
test.add_block(block)

# and finally save it at the specified location with the filename "quiz.cgtt"
# we can provide a filename too but the ".cgtt" extension is necessary
# this file can be uploaded with the import button under a Test
test.save("./")

