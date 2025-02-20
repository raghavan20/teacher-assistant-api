from flask import Flask, request, jsonify, send_file
from datetime import datetime
from db_init import init_db
from db_utils import *
app = Flask(__name__)
db = create_db(app)
Registry.s_db = db

from models import *
from utils import Registry
from analyzer import RecordingAnalyzer
analyzer = RecordingAnalyzer()


@app.route('/recordings/<int:recording_id>', methods=['GET'])
def get_recording(recording_id):
    recording = Recording.query.get(recording_id)
    if not recording:
        return jsonify({"error": "Recording not found"}), 404

    response_data = {
        "id": recording.id,
        "timestamp": recording.timestamp.isoformat(),
        "user_id": recording.user_id,
        "subject": recording.subject,
        "grade": recording.grade,
        "r_full_response_json": recording.r_full_response_json,
        "r_overall_score": recording.r_overall_score,
        "r_suggestions_count": recording.r_suggestions_count,
        "r_topics_required": recording.r_topics_required,
        "r_topics_covered": recording.r_topics_covered,
        "r_structure": recording.r_structure,
        "r_depth": recording.r_depth,
        "r_style": recording.r_style
    }

    include_blob = request.args.get('include_blob', 'false').lower() == 'true'
    if include_blob:
        response_data["recording_blob"] = recording.recording_blob.hex()  # Convert binary to hex string

    return jsonify(response_data)


@app.route('/recordings', methods=['POST'])
def upload_recording():
    if 'recording' not in request.files:
        return jsonify({"error": "No recording file provided"}), 400

    file = request.files['recording']
    subject = request.form.get('subject')
    grade = request.form.get('grade')
    user_id = request.form.get('user_id')

    if not subject or not grade or not user_id:
        return jsonify({"error": "Missing required fields: subject, grade, user_id"}), 400

    new_recording = Recording(
        timestamp=datetime.utcnow(),
        recording_blob=file.read(),
        user_id=int(user_id),
        subject=subject,
        grade=grade
    )

    recording = analyzer.analyze(new_recording)

    Registry.s_db.session.add(recording )
    Registry.s_db.session.commit()

    return jsonify({"message": "Recording uploaded successfully", "recording_id": new_recording.id}), 201

if __name__ == '__main__':
    # Initialize database and create tables if not present
    init_db(app, Registry.s_db)

    app.run(debug=True)


