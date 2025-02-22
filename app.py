from flask import Flask, request, jsonify, abort, Response
from sqlalchemy.orm import load_only
from sqlalchemy import func, and_
from utils.db_utils import *
from utils.utils import Registry
app = Flask(__name__)
db = create_db(app)
Registry.s_db = db
from flask_cors import CORS
from models import *

from analysis.analyzer import RecordingAnalyzer
CORS(app)
analyzer = RecordingAnalyzer()


@app.route('/recordings', methods=['GET'])
def list_recordings():
    user_id = request.args.get("user_id", type=int)
    query = Recording.query.with_entities(
        Recording.id, Recording.timestamp, Recording.user_id, Recording.subject, Recording.grade,
        Recording.r_full_response_json, Recording.r_overall_score, Recording.r_suggestions_count,
        Recording.r_topics_required, Recording.r_topics_covered, Recording.r_structure,
        Recording.r_depth, Recording.r_style
    )

    filters = []
    if user_id is not None:
        filters.append(Recording.user_id == user_id)

    if filters:
        query = query.filter(and_(*filters))

    recordings = query.all()

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


@app.route('/recordings/<int:recording_id>/blob', methods=['GET'])
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
    language = request.form.get('language')
    analyze = request.form.get('analyze', 'true').lower() == 'true'

    if not subject or not grade or not user_id:
        return jsonify({"error": "Missing required fields: subject, grade, user_id"}), 400

    recording = Recording(
        timestamp=datetime.utcnow(),
        recording_blob=file.read(),
        user_id=int(user_id),
        subject=subject,
        grade=grade,
        language=language
    )

    if analyze:
        recording = analyzer.analyze(recording)

    Registry.s_db.session.add(recording)
    Registry.s_db.session.commit()

    return jsonify({"message": "Recording uploaded successfully", "recording_id": recording.id}), 201


@app.route('/recordings/search', methods=['GET'])
def search_recordings():
    subject = request.args.get('subject')
    grade = request.args.get('grade')

    # Start query with selected columns only (excluding `recording_blob`)
    query = db.session.query(Recording).options(
        load_only(
            Recording.id,
            Recording.timestamp,
            Recording.user_id,
            Recording.subject,
            Recording.grade,
            Recording.r_overall_score,
            Recording.r_structure,
            Recording.r_depth,
            Recording.r_style
        )
    )

    # Apply filters
    if subject:
        query = query.filter(Recording.subject.ilike(f"%{subject}%"))
    if grade:
        query = query.filter(Recording.grade.ilike(f"%{grade}%"))

    # Execute query
    results = query.all()

    # Convert results to JSON-friendly format
    recordings_list = [
        {
            "id": rec.id,
            "timestamp": rec.timestamp.isoformat(),
            "user_id": rec.user_id,
            "subject": rec.subject,
            "grade": rec.grade,
            "overall_score": rec.r_overall_score,
            "structure": rec.r_structure,
            "depth": rec.r_depth,
            "style": rec.r_style
        }
        for rec in results
    ]

    return jsonify(recordings_list), 200


@app.route('/recordings/<int:recording_id>/worksheet', methods=['GET'])
def generate_worksheet(recording_id):

    if recording_id:
        recording = Recording.query.with_entities(
            Recording.id, Recording.timestamp, Recording.user_id, Recording.subject, Recording.grade,
            Recording.language, Recording.r_full_response_json, Recording.r_overall_score, Recording.r_suggestions_count,
            Recording.r_topics_required, Recording.r_topics_covered, Recording.r_structure,
            Recording.r_depth, Recording.r_style
        ).filter_by(id=recording_id).first()

        if not recording:
            return jsonify({"error": "Recording not found"}), 404

        worksheet = analyzer.generate_worksheet(recording)

        response = {
            "recording_id": recording_id,
            "worksheet": worksheet
        }
        return jsonify(response), 200

    else:
        return jsonify({"error": "Invalid recording_id"}), 400


@app.route('/recordings/<int:recording_id>/worksheet', methods=['GET'])
def generate_activity(recording_id):

    if recording_id:
        recording = Recording.query.with_entities(
            Recording.id, Recording.timestamp, Recording.user_id, Recording.subject, Recording.grade,
            Recording.language, Recording.r_full_response_json, Recording.r_overall_score, Recording.r_suggestions_count,
            Recording.r_topics_required, Recording.r_topics_covered, Recording.r_structure,
            Recording.r_depth, Recording.r_style
        ).filter_by(id=recording_id).first()

        if not recording:
            return jsonify({"error": "Recording not found"}), 404

        activity = analyzer.generate_activity(recording)

        response = {
            "recording_id": recording_id,
            "activity": activity
        }
        return jsonify(response), 200

    else:
        return jsonify({"error": "Invalid recording_id"}), 400


@app.route('/stats/users/<int:user_id>', methods=['GET'])
def get_user_stats(user_id):
    # Query total lesson interactions
    total_interactions = db.session.query(func.count(Recording.id)).filter(
        Recording.user_id == user_id
    ).scalar()

    if total_interactions == 0:
        return jsonify({"user_id": user_id, "streak": 0, "total_interactions": 0}), 200

    # Get distinct recorded dates for the user, sorted in descending order
    user_dates = db.session.query(
        func.date(Recording.timestamp).label("record_date")
    ).filter(Recording.user_id == user_id).distinct().order_by(
        func.date(Recording.timestamp).desc()
    ).all()

    # Convert query result to a list of date objects
    date_list = [record.record_date for record in user_dates]

    # Calculate streak
    streak = 1
    for i in range(1, len(date_list)):
        if (date_list[i - 1] - date_list[i]).days == 1:  # Consecutive day
            streak += 1
        else:
            break  # Streak broken

    return jsonify({
        "streak": streak,
        "total_interactions": total_interactions
    }), 200

if __name__ == '__main__':
    # Initialize database and create tables if not present
    init_db(app, Registry.s_db)

    app.run(debug=True)


