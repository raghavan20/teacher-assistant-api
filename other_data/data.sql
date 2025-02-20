INSERT INTO recordings (
    timestamp, recording_blob, user_id, subject, grade,
    r_full_response_json, r_overall_score, r_suggestions_count,
    r_topics_required, r_topics_covered, r_structure, r_depth, r_style
) VALUES (
    NOW(), '\\x00010203', 1, 'Mathematics', '10th',
    '{"feedback": "Great structure!"}', 85.5, 3,
    5, 4, 4.5, 4.0, 4.2
);

INSERT INTO recordings (
    timestamp, recording_blob, user_id, subject, grade,
    r_full_response_json, r_overall_score, r_suggestions_count,
    r_topics_required, r_topics_covered, r_structure, r_depth, r_style
) VALUES (
    NOW(), '\\x04050607', 2, 'Physics', '11th',
    '{"feedback": "Needs more depth."}', 78.0, 5,
    6, 4, 3.8, 3.5, 4.0
);
