from models import *
from flask import request, jsonify, Blueprint
from utils.utils import get_logger
from utils.gemini_api_methods import initialize_model, upload_file, delete_all_files
from utils.prompt_plan_ws_quiz import ContentPrompt
import json


logger = get_logger()
quiz_routes = Blueprint("worksheet_routes", __name__, url_prefix="/")

@quiz_routes.route('/recordings/<int:recording_id>/quiz', methods=['POST'])
def quiz_route(recording_id):
    if recording_id:
        recording = Recording.query.with_entities(
            Recording.id, Recording.timestamp, Recording.user_id, Recording.subject, Recording.grade,
            Recording.language, Recording.topic, Recording.r_full_response_json, Recording.r_overall_score, Recording.r_suggestions_count,
            Recording.r_topics_required, Recording.r_topics_covered, Recording.r_structure,
            Recording.r_depth, Recording.r_style
        ).filter_by(id=recording_id).first()

        if not recording:
            return jsonify({"error": "Recording not found"}), 404

        quiz = generate_quiz(recording)

        return jsonify(quiz), 200

    else:
        return jsonify({"error": "Invalid recording_id"}), 400


def generate_quiz(recording: Recording):

    model = initialize_model(name='gemini-2.0-flash',
                             temperature=0.1,
                             top_k=5,
                             top_p=0.5)
    try:
        cp = ContentPrompt(grade=recording.grade,
                           subject=recording.subject,
                           topic=recording.topic,
                           language=recording.language)

        prompt = cp.create_quiz_prompt(quiz_questions_numbers=5)

        result = model.generate_content(prompt)
        result_dict = json.loads(result.text)

        return match_questions_with_answers(result_dict)

    except Exception as e:
        logger.error("Exception occurred while analyzing recording", exc_info=True)


def match_questions_with_answers(data):
    questions = data["questions"]
    answers = data["answers"]

    results = []

    for question_data in questions:
        question_id = question_data["question_id"]
        options = {opt["option_id"]: opt["text"] for opt in question_data["options"]}

        # Find the matching answer for the question_id
        answer_entry = next((ans for ans in answers if ans["question_id"] == question_id), None)

        if answer_entry:
            answer_text = options.get(answer_entry["answer_option"], "Unknown")
        else:
            answer_text = "Unknown"

        results.append({
            "question": question_data["question"],
            "answer": answer_text,
            "options": list(options.values())
        })

    return results