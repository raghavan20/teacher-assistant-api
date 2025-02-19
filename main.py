from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import openai
from werkzeug.utils import secure_filename
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from db_init import init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/teaching_db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    teacher_id = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    analysis = db.Column(db.Text)

@app.route('/upload', methods=['POST'])
def upload_audio():
    file = request.files['audio']
    teacher_id = request.form['teacher_id']
    subject = request.form['subject']
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    recording = Recording(filename=filename, teacher_id=teacher_id, subject=subject)
    db.session.add(recording)
    db.session.commit()

    analyze_audio(recording.id, filepath)  # Call LLM analysis asynchronously
    return jsonify({"message": "File uploaded successfully", "id": recording.id})

@app.route('/audio/<int:id>', methods=['GET'])
def stream_audio(id):
    recording = Recording.query.get_or_404(id)
    filepath = os.path.join(UPLOAD_FOLDER, recording.filename)
    return send_file(filepath)

def analyze_audio(recording_id, filepath):
    # Convert speech to text (mocked)
    transcript = "Sample transcription of lecture."
    
    # Call LLM (mocked with OpenAI API as placeholder)
    feedback = "The lecture was well-structured but could use more engagement."
    
    # Store analysis in DB
    recording = Recording.query.get(recording_id)
    recording.analysis = feedback
    db.session.commit()

@app.route('/news', methods=['GET'])
def get_news():
    subject = request.args.get('subject')
    return jsonify({"news": ["News article 1", "News article 2"]})

@app.route('/quiz', methods=['GET'])
def get_quiz():
    subject = request.args.get('subject')
    return jsonify({"quiz": [{"question": "Sample question?", "choices": ["A", "B", "C", "D"], "answer": "A"}]})

@app.route('/articles', methods=['GET'])
def get_articles():
    subject = request.args.get('subject')
    return jsonify({"articles": ["Article 1", "Article 2", "Article 3"]})

@app.route('/stats/<int:teacher_id>', methods=['GET'])
def get_stats(teacher_id):
    recordings = Recording.query.filter_by(teacher_id=teacher_id).all()
    return jsonify({"total_lectures": len(recordings)})

if __name__ == '__main__':
    # Initialize database and create tables if not present
    init_db(app, db)

    app.run(debug=True)


