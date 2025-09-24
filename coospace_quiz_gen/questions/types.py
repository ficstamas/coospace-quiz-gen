from .base import Question
import json
from ..utils.html import format_html_for_json_data


class SingleChoiceQuestion(Question):
    def __init__(self, question_html: str, total_score=1.00, random_order=True):
        """
        Wrapper for Single Choice Question
        :param question_html: Question HTML
        :param total_score: Total score that can be obtained from the question
        :param random_order: Shuffle options randomly (default: True)
        """
        super().__init__(total_score, question_html, inner_id=1, xml_tag="SingleChoice")
        self._answer_id = 1
        self.answers = []
        self._valid_answer_id = 1
        self.random_order = random_order

    def add_option(self, option_html, valid=False):
        """
        Add an option to the question
        :param option_html: Can be plain text or html
        :param valid: whether the option is valid (correct), if more than 1 valid options is provided then the last one will be flagged as valid
        :return:
        """
        self.answers.append({"Id": self._answer_id, "Value": format_html_for_json_data(option_html)})
        if valid:
            self._valid_answer_id = self._answer_id
        self._answer_id += 1

    def get_data(self):
        return {"RandomOrder": self.random_order, "Options": self.answers}

    def get_valid_answer(self):
        return {"OptionId": self._valid_answer_id}


class MultiChoiceQuestion(Question):
    def __init__(self, question_html: str, total_score=1.00, random_order=True):
        """
        Wrapper for Multi Choice Question
        :param question_html: Question HTML
        :param total_score: Total score that can be obtained from the question
        :param random_order: Shuffle options randomly (default: True)
        """
        super().__init__(total_score, question_html, inner_id=2, xml_tag="MultiChoice")
        self._answer_id = 1
        self.answers = []
        self._valid_answer_ids = set()
        self._invalid_answer_ids = set()
        self.random_order = random_order

    def add_option(self, option_html, valid=False):
        """
        Add an option to the question
        :param option_html: Can be plain text or html
        :param valid: whether the option is valid (correct)
        :return:
        """
        self.answers.append({"Id": self._answer_id, "Value": format_html_for_json_data(option_html)})
        if valid:
            self._valid_answer_ids.add(self._answer_id)
            if self._answer_id in self._invalid_answer_ids:
                self._invalid_answer_ids.remove(self._answer_id)
        else:
            if self._answer_id in self._valid_answer_ids:
                self._valid_answer_ids.remove(self._answer_id)
            self._invalid_answer_ids.add(self._answer_id)
        self._answer_id += 1

    def get_data(self):
        return {"RandomOrder": self.random_order, "Options": self.answers}

    def get_valid_answer(self):
        options = {}
        for option_id in self._valid_answer_ids:
            options[option_id] = True
        for option_id in self._invalid_answer_ids:
            options[option_id] = False
        return {"Answers": options}


class ShortTextQuestion(Question):
    def __init__(self, question_html: str, total_score=1.00, regexp=False, case_sensitive=False):
        """
        Wrapper for Short Text Question
        :param question_html: Question HTML
        :param total_score: Total score that can be obtained from the question
        :param regexp: Whether the answer should match regexp or not (does not work at the moment)
        :param case_sensitive: Whether the answer should be case-sensitive
        """
        super().__init__(total_score, question_html, inner_id=3, xml_tag="ShortText")
        self.answers = []
        self.regexp = regexp
        self.case_sensitive = case_sensitive

    def add_answer(self, answer):
        """
        Add an option to the question
        :param answer: expected input
        :return:
        """
        self.answers.append(format_html_for_json_data(answer))

    def get_data(self):
        return {"RegExp": self.regexp, "CaseSensitive": self.case_sensitive, "Options": self.answers}

    def get_valid_answer(self):
        return {"Answer": [str(x) for x in self.answers]}


class EssayQuestion(Question):
    def __init__(self, question_html: str, total_score=1.00):
        """
        Wrapper for Short Text Question
        :param question_html: Question HTML
        :param total_score: Total score that can be obtained from the question
        :param regexp: Whether the answer should match regexp or not (does not work at the moment)
        :param case_sensitive: Whether the answer should be case-sensitive
        """
        super().__init__(total_score, question_html, inner_id=None, xml_tag="Essay")
        self.answers = []

    def add_keyword(self, keyword):
        """
        Add a keyword to the question
        :param keyword: expected keyword within the answer
        :return:
        """
        self.answers.append(format_html_for_json_data(keyword))

    def get_data(self):
        return {}

    def get_valid_answer(self):
        return {"Keywords": [str(x) for x in self.answers]}


class TrueFalseQuestion(Question):
    def __init__(self, question_html: str, total_score=1.00, answer_type=0, answer_id=1):
        """
        Wrapper for Short Text Question
        :param question_html: Question HTML
        :param total_score: Total score that can be obtained from the question
        :param answer_type: 0: True/False; 1: Yes/No
        :param answer_id: 1: True; 2: False
        """
        super().__init__(total_score, question_html, inner_id=7, xml_tag="TrueFalse")
        self.answers = []
        self.answer_type = answer_type
        self.answer_id = answer_id

    def set_answer_type_true_false(self):
        self.answer_type = 0

    def set_answer_type_yes_no(self):
        self.answer_type = 1

    def set_answer_true_or_yes(self):
        self.answer_id = 1

    def set_answer_false_or_no(self):
        self.answer_id = 2

    def get_data(self):
        return {"AnswerType": self.answer_type}

    def get_valid_answer(self):
        return {"AnswerId": self.answer_id}


class NumberQuestion(Question):
    def __init__(self, question_html: str, total_score=1.00):
        """
        Wrapper for Number Question
        :param question_html: Question HTML
        :param total_score: Total score that can be obtained from the question
        """
        super().__init__(total_score, question_html, inner_id=14, xml_tag="Number")
        self.answers = []
        self._answer_id = 1

    def add_option_percent(self, option_html: str, value: float, percent: float):
        """
        Add an option to the question with percentage tolerance
        :param option_html: Text
        :param value: Value
        :param percent: Percentage of tolerance (1.0 = 1%)
        :return:
        """
        self.answers.append({"Id": self._answer_id, "Text": format_html_for_json_data(option_html), "Value": float(value),"Percent": float(percent)})
        self._answer_id += 1

    def add_option_interval(self, option_html: str, from_: float, to_: float):
        """
        Add an option to the question with interval
        :param option_html: Text
        :param from_: left side of the interval
        :param to_: right side of the interval
        :return:
        """
        self.answers.append({"Id": self._answer_id, "Text": format_html_for_json_data(option_html), "From": float(from_), "To": float(to_)})
        self._answer_id += 1


    def get_data(self):
        options = []
        for answer in self.answers:
            options.append({"Id": answer["Id"], "Value": answer["Text"]})
        return {"Options": options}

    def get_valid_answer(self):
        options = []
        for answer in self.answers:
            a = {"Id": answer["Id"]}
            if "Value" in answer:
                a["Value"] = answer["Value"]
                a["Percent"] = answer["Percent"]
            else:
                a["From"] = answer["From"]
                a["To"] = answer["To"]
            options.append(a)
        return {"Options": options}


class ComplexQuestion(Question):
    def __init__(self, question_html: str, total_score=1.00):
        """
        Wrapper for Number Question
        :param question_html: Question HTML
        :param total_score: Total score that can be obtained from the question
        """
        super().__init__(total_score, question_html, inner_id=None, xml_tag="Complex")
        self.questions: list[Question] = []

    def add_question(self, question: Question):
        """
        Add a sub question to the question list
        :param question: A question object
        :return:
        :raises ValueError: If the question can not be a sub question
        """
        if question.inner_id is None:
            raise ValueError("We cannot assign this type of question to a complex question!")

        self.questions.append(question)

    def get_data(self):
        return {"SubQuestions": [q.get_sub_question_data_format() for q in self.questions]}

    def get_valid_answer(self):
        return {"SubAnswers": [q.get_valid_answer() for q in self.questions]}