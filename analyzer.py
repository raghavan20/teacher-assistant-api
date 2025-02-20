import random
import json
from models import *

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

        return recording

