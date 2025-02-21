import json
from pprint import pprint
from typing import Union


def get_dashboard_metrics(result_filepath_or_dict: Union[str, dict]):

    if isinstance(result_filepath_or_dict, str):
        with open(result_filepath_or_dict, 'r') as f:
            results = json.load(f)['predictions']
    else:
        results = result_filepath_or_dict

    pedagogy_score, pedagogy_strengths, pedagogy_areas_of_improvement \
        = _calculate_pedagogy_score(results['pedagogy_metrics'])

    topics_covered, total_no_of_topics, lesson_quality_score, missed_topics \
        = _calculate_lesson_plan_completion(results['lesson_plan_metrics'])

    teaching_guidelines_score, teaching_guidelines_strengths, teaching_guidelines_areas_of_improvement, teaching_guidelines_missed \
        = _calculate_teaching_guidelines_score(results['teaching_guidelines_metrics'])

    metrics = {
        "pedagogy_score": pedagogy_score,
        "pedagogy_strengths": pedagogy_strengths,
        "pedagogy_areas_of_improvements": pedagogy_areas_of_improvement,
        "no_topics_covered": topics_covered,
        "total_no_topics": total_no_of_topics,
        "missed_topics": missed_topics,
        "lesson_quality_score": lesson_quality_score,
        "teaching_guidelines_score": teaching_guidelines_score,
        "teaching_guidelines_strengths": teaching_guidelines_strengths,
        "teaching_guidelines_areas_of_improvement": teaching_guidelines_areas_of_improvement,
        "teaching_guidelines_missed": teaching_guidelines_missed,
        "overall_score": round(10 * ((pedagogy_score + lesson_quality_score + teaching_guidelines_score) / 3) ** 0.5, 0)
    }

    return metrics


def _calculate_pedagogy_score(metrics: dict):

    pedagogy_steps = ['engage', 'explore', 'explain', 'elaborate', 'evaluate']

    engagement_score = metrics['engagement_score']
    explore_score = metrics['explore_score']
    explain_score = metrics['explain_score']
    elaborate_score = metrics['elaborate_score']
    evaluate_score = metrics['evaluate_score']

    all_scores = [engagement_score, explore_score, explain_score, elaborate_score, evaluate_score]

    overall_score = 40 + sum(all_scores) * 4

    strengths_indices = [i for i, j in enumerate(all_scores) if j >= 2]
    strengths = [pedagogy_steps[x] for x in strengths_indices]
    improvement_areas_indices = [i for i, j in enumerate(all_scores) if j < 1]
    improvement_areas = [pedagogy_steps[x] for x in improvement_areas_indices]

    return overall_score, strengths, improvement_areas


def _calculate_lesson_plan_completion(metrics: dict):

    topics_covered = metrics['list_of_topics_covered']
    all_topics = metrics['list_of_all_topics']
    excellent_topics = metrics['list_of_excellent_topics']
    good_topics = metrics['list_of_good_topics']
    poor_topics = metrics['list_of_poor_topics']

    no_of_topics = len(all_topics)
    weighted_score = (len(excellent_topics) * 3) + (len(good_topics) * 2) + len(poor_topics)
    highest_score = 3 * no_of_topics
    quality = round(((100 * (weighted_score / highest_score)) ** 0.5) * 10, 0)

    missed_topics = [x for x in all_topics if x not in topics_covered]

    return len(topics_covered), len(all_topics), quality, missed_topics


def _calculate_teaching_guidelines_score(metrics: dict):

    excellent_guidelines = metrics['list_of_excellent_guidelines']
    good_guidelines = metrics['list_of_good_guidelines']
    poor_guidelines = metrics['list_of_poor_guidelines']
    all_guidelines = metrics['list_of_all_guidelines']

    weighted_score = (len(excellent_guidelines) * 3) + (len(good_guidelines) * 2) + len(poor_guidelines)
    highest_score = 3 * len(all_guidelines)

    score = round(((100 * (weighted_score / highest_score)) ** 0.5) * 10, 0)

    exhibited_guidelines = metrics['list_of_guidelines_exhibited']
    missed_guidelines = [x for x in all_guidelines if
                         x not in exhibited_guidelines]
    strengths = excellent_guidelines
    improvement_areas = poor_guidelines

    return score, strengths, improvement_areas, missed_guidelines



if __name__ == '__main__':

    pprint(get_dashboard_metrics('../output/19Feb-1949-economics.json'))
