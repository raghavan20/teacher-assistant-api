from prompt_generation_methods import _get_pedagogy, _get_lesson_plan, _get_teaching_guidelines

class content_prompt:
    def __init__(self, grade: int, subject: str, topic: str, state: str ='karnataka',
                 board: str ='CBSE', district: str ='Bengaluru',
                 block: str ='Mahadevpura', language: str = 'english') -> None:

        self.grade = grade
        self.subject = subject
        self.topic = topic
        self.state = state
        self.board = board
        self.district = district
        self.block = block
        self.language = language
        return
    
    def create_lesson_plan_prompt(self, class_duration: int = 30):
        template = '''
        You are teacher's helpful assistant that creates lesson plan for given grade , topic, duration,
        pedagogy , board and langauge

        Generate lesson plan for grade {grade} for {subject} on  {topic} topic for duration {class_duration}
        minutes for {board} board in {language} language.
        Ensure that lesson plan adhere to pedagogy structure and teaching guidelines given below and interactive in nature

        Pedagogy Structure: 
        {pedagogy}
    
        Teaching Guidelines: 
        {teaching_guidelines}

        output json structure should be on the basis of pedagogy structure . 
        Keep all examples in indian context assuming rural India with limited access of tools & technology.

        {{
         "Engage": <>
         "Explore": <>
         "Explain": <>
         "Elaborate" : <>
         "Evaluate" : <>
         
        }}
   

        '''

        # lesson_plan_context = _get_lesson_plan(state=self.state, board=self.board, grade=self.grade,
        #                                         subject=self.subject, topic=self.topic)
        pedagogy_context = _get_pedagogy(state=self.state, board=self.board)
        teaching_guidelines_context = _get_teaching_guidelines(state=self.state, district=self.district, block=self.block)

        prompt = template.format(grade = self.grade,
                                 subject = self.subject,
                                 topic = self.topic,
                                 class_duration = class_duration,
                                 board =  self.board,
                                 language = self.language,
                                 pedagogy=pedagogy_context,
                                 teaching_guidelines=teaching_guidelines_context
                                 )

        return prompt
    
    def create_quiz_prompt(self,quiz_questions_numbers: int = 10):
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
        questions: [{{"question1": <>: "options":<>}}]
        answers: [{{"question1": <>}}]
        
        }}

        '''
        prompt = template.format(quiz_questions_numbers=quiz_questions_numbers,
                                 grade = self.grade,
                                 subject = self.subject,
                                 topic = self.topic,
                                 language = self.language
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

        .add answers at the end of worksheet for every question. Generate HTML content to render the worksheet in nice
        formatted manner on webpage

        output_format_json:
        {{
        multiple_choice: [{{"question1": <>: "options":<>}}],
        word_problem: [{{"question6": <>: "options":<>}}],
        fill_in_the_blanks: [{{"question11": <>}}],
        true_false: [{{"question16": <>}}]

        answers: [{{"question1": <>}}]
        
        }}

        '''
        prompt = template.format(
                                 grade = self.grade,
                                 subject = self.subject,
                                 topic = self.topic,
                                 language = self.language
                                 )
        return prompt
            
    
if __name__ == "__main__":
    cp = content_prompt( grade=4, subject="mathematics", topic="Like Fraction Addition")
    #prompt = cp.create_lesson_plan_prompt(class_duration=30)
    prompt = cp.create_quiz_prompt(quiz_questions_numbers=10)
    print(prompt)


        

    