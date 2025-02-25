from models import *
from flask import request, jsonify, Blueprint
from utils.utils import get_logger
from utils.gemini_api_methods import initialize_model, upload_file, delete_all_files
from utils.prompt_plan_ws_quiz import ContentPrompt
import json


logger = get_logger()
activity_routes = Blueprint("activity_routes", __name__, url_prefix="/")

@activity_routes.route('/recordings/<int:recording_id>/activity', methods=['POST'])
def activity_route(recording_id):

    if recording_id:
        recording = Recording.query.with_entities(
            Recording.id, Recording.timestamp, Recording.user_id, Recording.subject, Recording.grade,
            Recording.language, Recording.topic, Recording.r_full_response_json, Recording.r_overall_score, Recording.r_suggestions_count,
            Recording.r_topics_required, Recording.r_topics_covered, Recording.r_structure,
            Recording.r_depth, Recording.r_style
        ).filter_by(id=recording_id).first()

        if not recording:
            return jsonify({"error": "Recording not found"}), 400

        activity = generate_activity(recording)

        return jsonify(activity), 200

    else:
        return jsonify({"error": "Invalid recording_id"}), 400


def generate_activity(recording: Recording):

    model = initialize_model(name='gemini-2.0-flash',
                             temperature=0.1,
                             top_k=5,
                             top_p=0.5)
    try:
        cp = ContentPrompt(grade=recording.grade,
                           subject=recording.subject,
                           topic=recording.topic,
                           language=recording.language)

        prompt = cp.create_activity_prompt()

        result = model.generate_content(prompt)
        try:
            result_dict = json.loads(result.text)[0]
        except:
            result_dict = json.loads(result.text)

        return result_dict

    except Exception as e:
        logger.error("Exception occurred while analyzing recording", exc_info=True)

