# CooSpace Quiz Generation Utilities

Why do we need this?
Well, because nobody is ever prepared for a ZIP file renamed as .cgtt (for no apparent reason), containing two XML files that must be carefully formatted since they include a mix of XML, HTML, and JSON.

In the end, this library produces that abominable file — the one that can actually be uploaded as a test.

See [demo.py](demo.py) for examples.

__Installation:__

```sh
pip install git+https://github.com/ficstamas/coospace-quiz-gen.git
```

# Question Types

Every question accepts `question_html` and `total_score`.

| Class                  | Description                                                 | Params                                                                               | methods                                                                                                            |
|------------------------|-------------------------------------------------------------|--------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------|
| `SingleChoiceQuestion` | Select a single answer                                      | `random_order` - shuffle options                                                     | `add_option(option_html, valid=False)`                                                                             |
| `MultiChoiceQuestion`  | Select multiple answers                                     | `random_order` - shuffle options                                                     | `add_option(option_html, valid=False)`                                                                             |
| `ShortTextQuestion`    | Accepts a short textual answer                              | `case_sensitive` - case sensitive answer                                             | `add_answer(answer)`                                                                                               |
| `EssayQuestion`        | Essay                                                       | ...                                                                                  | `add_keyword(keyword)`                                                                                             |
| `TrueFalseQuestion`    | A class for True/False or Yes/No questions                  | `answer_type` - True/False(0), Yes/No(1) <br> `answer_id` - True/Yes(1), False/No(2) | `set_answer_type_true_false()`, `set_answer_type_yes_no()`, `set_answer_true_or_yes()`, `set_answer_false_or_no()` |
| `NumberQuestion`       | A question type for numerical imputs                        | ...                                                                                  | `add_option_percent(option_html, value, percent)`, `add_option_interval(option_html, from_, to_)`                  |
| `ComplexQuestion`      | A question type that can encapsulate multiple sub-questions | ...                                                                                  | `add_question(question)`                                                                                           |
For example:
```python
from coospace_quiz_gen import *

question = TrueFalseQuestion("Should I really spend my time doing this?", total_score=2.0)
question.set_answer_type_yes_no()  # sets the question to Yes/No type
question.set_answer_false_or_no()  # sets the correct answer to False/No depending on the question type
```

# Blocks

From a set of questions, we can form a block of random questions:

```python
block_1 = RandomBlock(title=None, n_selected_question=2)
```

- `title` is optional and can be any string or `None`.
- `n_selected_question` defines how many questions to select at once from the list of questions.

You can add any Question objects using:

```block_1.add_question(question)```

# Tests

A CooSpace test can be defined as:

`test = Test()`,

It accepts three optional arguments:
`forward_only=False`, `mix=False`, and `required_answers=False`.
(You can probably guess what they do.)

Then, add questions and blocks to the test in the desired order:

```python
test.add_question(question)
test.add_block(block_1)
```

Finally, save the test:
```python
test.save("./")  # it produces a `quiz.cgtt` file
```