from flask import Flask, request, jsonify, abort, Response
from db_utils import *
app = Flask(__name__)
db = create_db(app)
Registry.s_db = db

from models import *
from utils import Registry
from analysis.analyzer import RecordingAnalyzer
analyzer = RecordingAnalyzer()


@app.route('/recordings', methods=['GET'])
def list_recordings():
    recordings = Recording.query.with_entities(
        Recording.id, Recording.timestamp, Recording.user_id, Recording.subject, Recording.grade,
        Recording.r_full_response_json, Recording.r_overall_score, Recording.r_suggestions_count,
        Recording.r_topics_required, Recording.r_topics_covered, Recording.r_structure,
        Recording.r_depth, Recording.r_style
    ).all()
    return jsonify([{
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
    } for recording in recordings])


@app.route('/recordings/<int:recording_id>', methods=['DELETE'])
def delete_recording(recording_id):
    recording = Recording.query.get(recording_id)
    if not recording:
        return jsonify({"error": "Recording not found"}), 404

    db.session.delete(recording)
    db.session.commit()

    return jsonify({"message": "Recording deleted successfully"})


@app.route('/recordings/<int:recording_id>/reanalyze', methods=['POST'])
def reanalyze_recording(recording_id):
    recording = Recording.query.get(recording_id)
    if not recording:
        return jsonify({"error": "Recording not found"}), 404

    recording = analyzer.analyze(recording)

    Registry.s_db.session.add(recording)
    Registry.s_db.session.commit()

    return jsonify({"message": "Recording uploaded successfully", "recording_id": recording.id}), 201


@app.route('/recordings/<int:recording_id>/recording_blob', methods=['GET'])
def get_recording_blob(recording_id):
    recording_blob = Recording.query.with_entities(
        Recording.recording_blob
    ).filter_by(id=recording_id).first()


    if recording_blob is None or recording_blob.recording_blob is None:
        return abort(404, "Recording not found")

    # Convert to bytearray (if necessary)
    audio_bytes = bytes(recording_blob.recording_blob)  # Ensure it's bytes

    # Determine the MIME type (change as needed)
    mime_type = "audio/mpeg"  # Adjust based on stored format (e.g., "audio/mpeg" for MP3)

    # Return the response with correct headers
    return Response(audio_bytes, mimetype=mime_type)

@app.route('/recordings/<int:recording_id>', methods=['GET'])
def get_recording(recording_id):
    recording = Recording.query.with_entities(
        Recording.id, Recording.timestamp, Recording.user_id, Recording.subject, Recording.grade,
        Recording.r_full_response_json, Recording.r_overall_score, Recording.r_suggestions_count,
        Recording.r_topics_required, Recording.r_topics_covered, Recording.r_structure,
        Recording.r_depth, Recording.r_style
    ).filter_by(id=recording_id).first()

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
    analyze = request.form.get('analyze', 'true').lower() == 'true'

    if not subject or not grade or not user_id:
        return jsonify({"error": "Missing required fields: subject, grade, user_id"}), 400

    recording = Recording(
        timestamp=datetime.utcnow(),
        recording_blob=file.read(),
        user_id=int(user_id),
        subject=subject,
        grade=grade
    )

    if analyze:
        recording = analyzer.analyze(recording)

    Registry.s_db.session.add(recording)
    Registry.s_db.session.commit()

    return jsonify({"message": "Recording uploaded successfully", "recording_id": recording.id}), 201

if __name__ == '__main__':
    # Initialize database and create tables if not present
    init_db(app, Registry.s_db)

    app.run(debug=True)


