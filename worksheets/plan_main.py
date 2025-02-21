import json
from datetime import datetime

from gemini_api_methods import initialize_model
from prompt_plan_ws_quiz import content_prompt

if __name__ == "__main__":

    model = initialize_model(name='gemini-2.0-flash',
                             temperature=1,
                             top_k=5,
                             top_p=0.5)
    
    
    results = []
    output_filepath = '../output/plan-{}.json'.format(datetime.strftime(datetime.now(), format('%d%b-%H%M')))

    try:
        cp = content_prompt( grade=4, subject="science", topic="Cleanliness", language='Hindi')
        #prompt = cp.create_lesson_plan_prompt(class_duration=30)
        #prompt = cp.create_quiz_prompt(quiz_questions_numbers=10)
        prompt = cp.create_worksheet_prompt()

        result_file_content = {
            'prompt': prompt,
            'predictions': []
        }
        result = model.generate_content(prompt)
        result_dict = json.loads(result.text)
        results.append(result_dict)
        result_file_content['predictions'] = results
        print('\n{}\n'.format(result_dict))
        with open(output_filepath, 'w') as f:
            json.dump(result_file_content, f)
    except Exception as e:
        print('****************\nException:\n{}\n***************'.format(e, e.__traceback__))
    
