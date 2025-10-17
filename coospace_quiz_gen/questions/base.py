from abc import ABC, abstractmethod
from ..utils.html import format_html_for_json_data
from ..utils.text import dedent
import json


class ComplexSubType:
    def __init__(self, is_official_subtype=False):
        self.is_official_subtype = is_official_subtype


class Question(ComplexSubType, ABC):
    def __init__(self, total_score, question_html, inner_id=None, item_id=None, xml_tag=None, is_official_subtype=False):
        super().__init__(is_official_subtype)
        self.total_score = total_score
        self.question_html = question_html
        self.inner_id = inner_id
        self.item_id = item_id
        self.xml_tag = xml_tag

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_valid_answer(self):
        pass

    def get_sub_question_data_format(self):
        return {
            "Type": self.inner_id,
            "QuestionHtml": format_html_for_json_data(self.question_html),
            "Data": self.get_data(),
            "TotalScore": self.total_score
        }

    def xml_template(self):
        template = f"""
        <{self.xml_tag} Id="{self.item_id}" TotalScore="{self.total_score:.2f}">
            <QuestionHtml>{self.question_html}</QuestionHtml>
            <Data>{json.dumps(self.get_data())}</Data>
            <ValidAnswer>{json.dumps(self.get_valid_answer())}</ValidAnswer>
        </{self.xml_tag}>
        """
        return dedent(template)
