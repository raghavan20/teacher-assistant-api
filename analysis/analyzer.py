import random
from models import *
import json
from datetime import datetime
from pprint import pprint
import os

from analysis.gemini_api_methods import initialize_model, upload_file
from analysis.metrics import get_dashboard_metrics
from analysis.prompt_generation_methods import create_analysis_prompt, create_postprocessing_prompt


class RecordingAnalyzer:
    def analyze(self, recording: Recording):
        # Fake LLM call
        analysis_result = {
            "feedback": "Well-structured lecture with good depth.",
            "overall_score": round(random.uniform(70, 100), 2),
            "suggestions_count": random.randint(1, 5),
            "topics_required": random.randint(3, 6),
            "topics_covered": random.randint(2, 6),
            "structure": round(random.uniform(3.0, 5.0), 2),
            "depth": round(random.uniform(3.0, 5.0), 2),
            "style": round(random.uniform(3.0, 5.0), 2)
        }

        # Update the recording in the database
        recording.r_full_response_json = json.dumps(analysis_result)
        recording.r_overall_score = analysis_result["overall_score"]
        recording.r_suggestions_count = analysis_result["suggestions_count"]
        recording.r_topics_required = analysis_result["topics_required"]
        recording.r_topics_covered = analysis_result["topics_covered"]
        recording.r_structure = analysis_result["structure"]
        recording.r_depth = analysis_result["depth"]
        recording.r_style = analysis_result["style"]

        print('Analyzing: subject={}, grade={}', recording.subject, recording.grade)

        model = initialize_model(name='gemini-1.5-pro',
                                 temperature=0.1,
                                 top_k=5,
                                 top_p=0.5)
        uploaded_file = upload_file(None, recording.recording_blob)

        try:
            result = model.generate_content(
                contents=['Create a transcript of this audio file in JSON format {"transcript": <transcript text>}',
                          uploaded_file])
            transcript_dict = json.loads(result.text)
            transcript = transcript_dict['transcript']

            prompt = create_analysis_prompt(grade=recording.grade,
                                            subject=recording.subject,
                                            topic='consumer_literacy',
                                            state='DEL',
                                            board='CBSE',
                                            district='New Delhi',
                                            block='Saket')
            # with open(prompt_filepath, 'w') as f:
            #     f.write(prompt)

            result = model.generate_content(contents=[prompt, transcript, uploaded_file])
            result_dict = json.loads(result.text)
            stats = get_dashboard_metrics(result_dict)
            result_file_content = {'predictions': result_dict, 'metrics': stats}
            suggestions_result = model.generate_content(create_postprocessing_prompt(result_file_content))
            suggestions_dict = json.loads(suggestions_result.text)
            suggestions = suggestions_dict['suggestions']
            result_file_content['suggestions'] = suggestions

            recording.r_full_response_json = result_file_content
            recording.r_overall_score = result_file_content['metrics']["overall_score"]
            recording.r_suggestions_count = len(result_file_content['suggestions'])
            # recording.r_topics_required = analysis_result["topics_required"]
            # recording.r_topics_covered = analysis_result["topics_covered"]
            recording.r_structure = result_file_content['metrics']["pedagogy_score"]
            recording.r_depth = result_file_content['metrics']["lesson_quality_score"]
            recording.r_style = result_file_content['metrics']["teaching_guidelines_score"]


            pprint(recording)

        except Exception as e:
            print('****************\nException:\n{}\n***************\n'.format(e, e.__traceback__))

        return recording

