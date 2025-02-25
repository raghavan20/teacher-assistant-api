from utils.prompt_generation_methods import _get_pedagogy, _get_lesson_plan, _get_teaching_guidelines


class ContentPrompt:
    def __init__(self, grade: int, subject: str, topic: str, state: str = 'karnataka',
                 board: str = 'CBSE', district: str = 'Bengaluru',
                 block: str = 'Mahadevpura', language: str = 'english') -> None:
        self.grade = grade
        self.subject = subject
        self.topic = topic
        self.state = state
        self.board = board
        self.district = district
        self.block = block
        self.language = language
        return

    def create_lesson_plan_prompt(self, lesson_duration: int = 60):
        template = '''
        You are teacher's helpful assistant that creates lesson plan for given grade , topic, duration,
        pedagogy , board and langauge

        Generate lesson plan for grade {grade} for {subject} on {topic} topic for a total lesson duration of {lesson_duration}
        minutes in {language} language.
        Ensure that lesson plan adhere to pedagogy structure and teaching guidelines given below and interactive in nature

        Pedagogy Structure: 
        {pedagogy}

        Teaching Guidelines: 
        {teaching_guidelines}

        Output JSON structure should be on the basis of pedagogy structure.
        
        Keep all examples in indian context assuming rural India with limited access of tools & technology.
        
        It is not necessary that all steps of the pedagogy are followed in the lesson since there is often not enough 
        time for all activities within the same lesson.

        {{
         "lesson_plan": [
            {{ "duration": <section duration in minutes>, "description": <string>, "pedagogy_step": <string> }},
            {{ "duration": <section duration in minutes>, "description": <string>, "pedagogy_step": <string> }},
            ...
            ]
        }}


        '''

        pedagogy_context = _get_pedagogy(state=self.state, board=self.board)
        teaching_guidelines_context = _get_teaching_guidelines(state=self.state, district=self.district,
                                                               block=self.block)

        prompt = template.format(grade=self.grade,
                                 subject=self.subject,
                                 topic=self.topic,
                                 lesson_duration=lesson_duration,
                                 language=self.language,
                                 pedagogy=pedagogy_context,
                                 teaching_guidelines=teaching_guidelines_context
                                 )

        return prompt

    def create_quiz_prompt(self, quiz_questions_numbers: int = 10):
        template = '''
        You are quiz generator that create multiple choice quiz questions for student assesment after lesson
        given grade, subject, topic, language and number of quiz questions.Gene

        Generate quiz which contains {quiz_questions_numbers} objective type questions with 4 options 
        for grade {grade} for {subject} on  {topic} in {language} language.

        There should be variety of questions including word problem , conceptual questions, simple problems etc.
        Keep all examples in indian context assuming rural India with limited access of tools & technology.

        .add answers at the end of quiz for every question.

        output_format_json:
        {{
        questions: [{{"question_id": <int>, "question": <string>: "options":[{{"option_id": <A, B, C, or D>, "text": <string>}}]}}]
        answers: [{{"question_id": <int>, "answer_option": <A, B, C, or D>}}]
        }}

        '''
        prompt = template.format(quiz_questions_numbers=quiz_questions_numbers,
                                 grade=self.grade,
                                 subject=self.subject,
                                 topic=self.topic,
                                 language=self.language
                                 )
        return prompt

    def create_worksheet_prompt(self):
        template = '''
        You are a worksheet creator who creates the worksheet for students homework,
        given grade, subject, topic and language.

        Generate worksheet which contains 5 multiple choice questions, 5 word problems,
        5 fill in the blanks and 5 True and False questions for grade {grade} for {subject} on 
        {topic} in {language} language.

        There should be variety of questions including word problem , conceptual questions, simple problems etc.
        Keep all examples in indian context assuming rural India with limited access of tools & technology.

        .add answers at the end of worksheet for every question and strictly follow the output_json_format provided below.


        output_format_json:
        {{
        multiple_choice: [{{"question1": "generated question without options: "options": ["option1", "option2", "option3", "option4"]}}],
        word_problems: [{{"question6": "word problem"}}],
        fill_in_the_blanks: [{{"question11": "fill in the blanks question}}],
        true_false: [{{"question16": "true/false statement"}}]

        answers: [{{"question1": "answer"}}]

        }}

        '''
        prompt = template.format(
            grade=self.grade,
            subject=self.subject,
            topic=self.topic,
            language=self.language
        )
        return prompt

    def create_activity_prompt(self):
        template = '''

        You are a classroom activity generator, who generates an interesting classroom activity given class, subject,
        topic and language considering it is for schools in rural india with limited access to technology and fancy activity items.

        Generate one classroom activity  for grade {grade} for {subject} on 
        {topic} in {language} language. 

        Keep the outputs strictly as below output_format_json format

        output_format_json:
        {{
        "activity_name" : "A short name",
        "material_needed" : "list materials required keeping rural india in consideration"
        "description" "activity details"
        }}   

        '''

        prompt = template.format(
            grade=self.grade,
            subject=self.subject,
            topic=self.topic,
            language=self.language
        )

        return prompt



if __name__ == "__main__":
    cp = ContentPrompt(grade=4, subject="mathematics", topic="Like Fraction Addition")
    # prompt = cp.create_lesson_plan_prompt(class_duration=30)
    prompt = cp.create_activity_prompt()
    print(prompt)




