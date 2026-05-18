"""Evaluation and quality assurance script for Phase 5."""

from typing import List, Dict
from milestone_zomato.models.restaurant import Restaurant
from milestone_zomato.models.recommendation import Recommendation

def verify_grounding(candidates: List[Restaurant], recommendations: List[Recommendation]) -> Dict[str, Any]:
    """Check if all recommended restaurant IDs exist in the candidate list."""
    candidate_ids = {r.id for r in candidates}
    hallucinations = [rec.restaurant_id for rec in recommendations if rec.restaurant_id not in candidate_ids]
    
    return {
        "is_grounded": len(hallucinations) == 0,
        "hallucination_count": len(hallucinations),
        "hallucinated_ids": hallucinations
    }

def run_basic_rubric(recommendations: List[Recommendation]) -> Dict[str, Any]:
    """Evaluate explanations based on a simple heuristic rubric."""
    stats = []
    for rec in recommendations:
        word_count = len(rec.explanation.split())
        # Check if explanation mentions 'because' or provides a rationale-like structure
        has_rationale = any(word in rec.explanation.lower() for word in ["because", "since", "due to", "offers", "provides"])
        
        stats.append({
            "id": rec.restaurant_id,
            "word_count": word_count,
            "has_rationale": has_rationale
        })
        
    avg_words = sum(s["word_count"] for s in stats) / len(stats) if stats else 0
    return {
        "avg_word_count": avg_words,
        "all_have_rationale": all(s["has_rationale"] for s in stats),
        "details": stats
    }

if __name__ == "__main__":
    # Example execution (placeholder for CLI tool)
    print("Evaluation module loaded. Use verify_grounding and run_basic_rubric in your integration tests.")
