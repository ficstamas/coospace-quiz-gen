from ..questions.base import Question
import json
import io
import zipfile
import os
from ..utils.text import dedent


class Test:
    def __init__(self, forward_only=False, mix=False, required_answers=False):
        self.forward_only = forward_only
        self.mix = mix
        self.required_answers = required_answers
        self.body: list[Question|RandomBlock] = []

    def add_block(self, block):
        self.body.append(block)

    def add_question(self, question):
        self.body.append(question)

    def get_form(self):
        form = {
            "Items": [x.item_id if isinstance(x, Question) else x.get_repr() for x in self.body],
            "ForwardOnly": self.forward_only, "Mix": self.mix, "RequiredAnswers": self.required_answers
        }
        return form

    def get_questions_xml(self):
        question_list = []
        for item in self.body:
            if isinstance(item, Question):
                question_list.append(item.xml_template())
            elif isinstance(item, RandomBlock):
                for sub_item in item.questions:
                    question_list.append(sub_item.xml_template())
        return dedent(f"""<?xml version="1.0" encoding="utf-8"?><Questions v="1">{"".join(question_list)}</Questions>""")


    def get_test_xml(self):
        return dedent(f"""<?xml version="1.0" encoding="utf-8"?><Test v="1"><Form>{json.dumps(self.get_form())}</Form></Test>""")

    def assign_ids(self):
        id_ = 100000001  # this is the usual starting id, dont know if it matters
        for item in self.body:
            if isinstance(item, Question):
                if item.item_id is None:
                    item.item_id = id_
                    id_ += 1
            elif isinstance(item, RandomBlock):
                for sub_item in item.questions:
                    if sub_item.item_id is None:
                        sub_item.item_id = id_
                        id_ += 1

    def save(self, path: str, filename = "quiz.cgtt"):
        self.assign_ids()
        # Create an in-memory bytes buffer
        buffer = io.BytesIO()

        questions = self.get_questions_xml()
        test = self.get_test_xml()

        # Write both strings into the zip file
        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.writestr("Questions.xml", questions)
            zipf.writestr("Test.xml", test)

        if not filename.endswith(".cgtt"):
            filename = filename + ".cgtt"
        output_path = os.path.join(path, filename)

        # Save the zip file to disk
        with open(output_path, "wb") as f:
            f.write(buffer.getvalue())



class RandomBlock:
    def __init__(self, title: str = None, n_selected_question: int = 1):
        """
        Create a random question block.
        :param title: Title of the question block. (optional)
        :param n_selected_question: Number of questions to select. (Default: 1)
        """
        self.questions: list[Question] = []
        self.title = title
        self.number_to_select = n_selected_question

    def add_question(self, question):
        self.questions.append(question)

    def get_repr(self):
        return {"$type":"random","Title": self.title,"Items": [x.item_id for x in self.questions], "Count": self.number_to_select}
