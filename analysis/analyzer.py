from models import *
import json
from pprint import pformat

from utils.gemini_api_methods import initialize_model, upload_file, delete_all_files
from analysis.metrics import get_dashboard_metrics
from utils.prompt_generation_methods import create_analysis_prompt, create_postprocessing_prompt
from utils.prompt_plan_ws_quiz import ContentPrompt
from utils.utils import get_logger

logger = get_logger()
class RecordingAnalyzer:

    def analyze(self, recording: Recording):
        print('Analyzing: subject={}, grade={}'.format(recording.subject, recording.grade))

        model = initialize_model(name='gemini-1.5-pro',
                                 temperature=0.1,
                                 top_k=5,
                                 top_p=0.5)

        delete_all_files()
        uploaded_file = upload_file(recording.recording_blob)

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
            recording.r_topics_required = result_file_content['metrics']["total_no_topics"]
            recording.r_topics_covered = result_file_content['metrics']["no_topics_covered"]
            recording.r_structure = result_file_content['metrics']["pedagogy_score"]
            recording.r_depth = result_file_content['metrics']["lesson_quality_score"]
            recording.r_style = result_file_content['metrics']["teaching_guidelines_score"]

            logger.info("Got recording analysis:\n%s", pformat(recording))
        except Exception as e:
            logger.error("Exception occurred while analyzing recording", exc_info=True)

        return recording
