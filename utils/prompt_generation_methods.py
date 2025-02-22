import json


def create_analysis_prompt(grade: int, subject: str, topic: str, state: str, board: str, district: str, block: str):

    template = \
'''
You are a teacher's helpful assistant that listens to a teacher delivering a lesson to a classroom through an audio 
recording and gives helpful suggestions of how the teacher has performed in the lesson based on the requirements of 
pedagogy, lesson plan, other teaching guidelines given to the teacher during training. Remember that the purpose of 
this feedback is to encourage teachers to improve and not to make them feel bad about not meeting all the 
standards set for them because it is not possible to meet all requirements in each class.

For the audio recording, do the following:
1. First, create a lesson outline with concise bullet points summarizing events, activities of the lesson in the audio recording.
2. Then, analyze the recording based on the pedagogy guidelines and create pedagogy_metrics as given in the output JSON structure.
3. Then, analyze the recording based on the lesson plan and create lesson_plan_metrics as given in the output JSON structure.
4. Then, analyze the recording based on the teaching guidelines and teaching_guidelines_metrics as given in the output JSON structure.

For the given audio recording and transcript of the audio recording from a grade {grade} classroom where the teacher 
is teaching a {subject} lesson on the topic of {topic}, analyze the audio and return structured output in JSON. 

Lesson Plan: 
{lesson_plan}

Pedagogy Structure: 
{pedagogy}

Teaching Guidelines: 
{teaching_guidelines}

Output JSON Structure:
{{
    "lesson_outline": [list of concise bullet points summarizing the events of the lesson in the audio recording],
    "pedagogy_metrics":
    {{
        "is_pedagogy_structure_followed": <boolean that is true if elements of the pedagogy structure are present in the lesson - not all can be present in a single lesson>,
        "engagement_score": <integer between 0 and 3 where 3 is the highest level of engagement of students according to "Engage" step of pedagogy guidelines>,
        "reason_for_engagement_score": <string with concise one sentence reason for the engagement_score given>,
        "explore_score": <integer between 0 and 3 where 3 is the highest level of exploration of students through activities according to the "Explore" step of pedagogy guidelines>,
        "reason_for_explore_score": <string with concise one sentence reason for the explore_score given>,
        "explain_score": <integer between 0 and 3 where 3 is the highest level of clarity for students according to the "Explain" step of pedagogy guidelines>,
        "reason_for_explain_score": <string with concise one sentence reason for the explain_score given>,
        "elaborate_score": <integer between 0 and 3 where 5 is the highest level of elaboration for students according to the "Elaborate" step of pedagogy guidelines>,
        "reason_for_elaborate_score": <string with concise one sentence reason for the elaborate_score given>,
        "evaluate_score": <integer between 0 and 3 where 5 is the highest quality of assessment for student according to the "Evaluate" step of pedagogy guidelines>,
        "reason_for_evaluate_score": <string with concise one sentence reason for the evaluate_score given>,
        "pedagogy_suggestions": [list of at most 2 specific suggestions where the teacher could have introduced an activity, example, question, or teaching method to improve the lesson experience for students],
    }},
    "lesson_plan_metrics":
    {{
        "list_of_topics_covered": [list topics covered by the teacher during the class in the lesson plan],
        "list_of_all_topics": [list with number of total topics in the lesson plan],
        "list_of_excellent_topics": [list of topics with excellent presentation by the teacher],
        "list_of_good_topics": [list of topics with decent presentation by the teacher with some room for improvement],
        "list_of_poor_topics": [list of topics that had poor presentation by the teacher with lots of room for improvement]
    }},
    "teaching_guidelines_metrics":
    {{
        "list_of_guidelines_exhibited": [list of guidelines exhibited by the teacher during the class],
        "list_of_all_guidelines": [list of all guidelines recommended in the given teaching guidelines list],
        "list_of_excellent_guidelines": [list of guidelines followed by the teacher consistently in the lesson],
        "list_of_good_guidelines": [list of guidelines exhibited once or twice in the lesson but could be more consistently exhibited],
        "list_of_poor_guidelines": [list of guidelines exhibited not exhibited or exhibited poorly by the teacher in the lesson],
    }}
}}        
'''

    lesson_plan_context = _get_lesson_plan(state=state, board=board, grade=grade, subject=subject, topic=topic)
    pedagogy_context = _get_pedagogy(state=state, board=board)
    teaching_guidelines_context = _get_teaching_guidelines(state=state, district=district, block=block)

    prompt = template.format(grade=grade,
                             subject=subject,
                             topic=topic,
                             lesson_plan=lesson_plan_context,
                             pedagogy=pedagogy_context,
                             teaching_guidelines=teaching_guidelines_context)

    return prompt

def create_postprocessing_prompt(result_dict: dict):

    template = '''
    1. Take the following Analysis_JSON below that is structured output of an audio analysis of classroom teaching for a 
    teacher's lesson, and extract no more than 2 actionable suggestions for the teacher. 
    2. Make sure that the suggestions are made after considering all the points made in the analysis JSON around what were the areas of improvement for the teacher given in the analysis.
    3. Try to see what would have been the highest impact suggestion to improve the students' understanding.
    4. Be very specific with the suggestion. For example, if there is a suggestion to add more examples in the lesson, 
    provide an actual example that can be immediately used. Or if there is a suggestion to ask a question during the 
    lesson, then give an example of that question.
    4. Return the output in a structured JSON like this:
    {{
        "suggestions": [
            {{
                "title": <suggestion title that is no more than 6-10 words long>,
                "pedagogy_step": <string that is one of the pedagogy steps 'engage', 'explore', 'explain', 'elaborate', 'evaluate' that the suggestion belongs to>
                "description": <suggestion detail that is no more than 500 characters long>
            }}
        ]
    }}
    
    Analysis_JSON:
    {result_dict}
    '''
    return template.format(result_dict=result_dict)

def _get_lesson_plan(state: str, board: str, grade: int, subject: str, topic: str):
    lesson_key = '-'.join([state, board, str(grade), subject, topic])
    try:
        with open('./analysis/lesson_plans.json', 'r') as c:
            lesson_plans = json.load(c)
            if not lesson_plans:
                raise Exception('No lesson plans found')
        description = lesson_plans.get(lesson_key, None)
        if description is None:
            raise Exception('Key "{}" not found'.format(lesson_key))
        return description
    except Exception as e:
        print('WARNING: Could not retrieve curriculum - {}'.format(e.__traceback__))
        return ''


def _get_pedagogy(state: str, board: str):
    # TODO Get from database of pedagogy guidelines per state and board
    return '''
    The 5E's instructional model is a research-based framework designed to facilitate inquiry-based learning and promote a deeper understanding of concepts. Each phase of the model—Engage, Explore, Explain, Elaborate, and Evaluate—plays a vital role in the teaching and learning process.
    1. Engage: The engage phase aims to capture students' attention and generate interest in the topic. It involves activities or discussions that activate prior knowledge, stimulate curiosity, and create a connection between the students' experiences and the new concepts being taught.
    2. Explore: In the explore phase, students actively participate in hands-on activities, investigations, and experiments. They explore the mathematical concepts, make observations, ask questions, and collect data. This phase encourages students to develop critical thinking skills, engage in problem-solving, and discover patterns and relationships.
    3. Explain: The explain phase focuses on providing explanations, clarifying concepts, and developing a deeper understanding. Teachers facilitate discussions, present mathematical principles, and guide students in making connections between their observations and the underlying mathematical concepts.
    4. Elaborate: In the elaborate phase, students apply their understanding of the concepts in real-life contexts. They engage in extended activities, solve complex problems, and work on projects that require higher-order thinking skills. This phase encourages students to explore mathematics beyond the classroom and strengthens their problem-solving abilities.
    5. Evaluate: The evaluate phase involves assessing students' learning outcomes and understanding. Various assessment strategies, including formative and summative assessments, are used to measure students' progress and provide feedback for further improvement.
    '''


def _get_teaching_guidelines(state: str, district: str, block: str):
    # TODO Get from database of teaching guidelines
    return '''
    1. Give at least two examples for each concept.
    2. Repeat each concept at least once.
    3. Make students answer questions on all topics.
    '''
