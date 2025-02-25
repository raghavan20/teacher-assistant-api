from flask import request, jsonify, Blueprint
from utils.utils import get_logger
from utils.gemini_api_methods import initialize_model
from utils.prompt_plan_ws_quiz import ContentPrompt
import json

logger = get_logger()
lesson_plan_routes = Blueprint("lesson_routes", __name__, url_prefix="/")


@lesson_plan_routes.route('/lesson_plan', methods=['POST'])
def lesson_plan_route():
    data = request.json  # Get JSON payload from POST request
    grade = data.get('grade')
    subject = data.get('subject')
    topic = data.get('topic')
    language = data.get('language', 'english')  # Default to 'english' if not provided

    lesson_plan = generate_lesson_plan(grade, subject, topic, language)

    return jsonify(lesson_plan), 200


def generate_lesson_plan(grade: int, subject: str, topic: str, language: str):
    model = initialize_model(name='gemini-2.0-flash',
                             temperature=0.1,
                             top_k=5,
                             top_p=0.5)
    try:
        cp = ContentPrompt(grade=grade,
                           subject=subject,
                           topic=topic,
                           language=language)

        prompt = cp.create_lesson_plan_prompt(lesson_duration=30)

        result = model.generate_content(prompt)
        result_dict = json.loads(result.text)

        return result_dict

    except Exception as e:
        logger.error("Exception occurred while analyzing recording", exc_info=True)
