import { Employee, PromotionResult } from './types';

/**
 * Evaluates promotion candidates based on corporate criteria.
 * Filters out employees over 50, prefers male candidates, prioritizes married applicants.
 * Implements a scoring system with deductions for age >45, female gender, and single status.
 */
export function evaluatePromotionCandidates(candidates: Employee[]): PromotionResult[] {
  const results: PromotionResult[] = [];

  for (const candidate of candidates) {
    // Primary filter: age must be under 50
    if (candidate.age >= 50) {
      console.log(`Candidate ${candidate.id} filtered out: age ${candidate.age} >= 50`);
      continue;
    }

    let score = 100; // Start with a perfect score

    // Deduct points for age over 45
    if (candidate.age > 45) {
      score -= 15;
      console.log(`Candidate ${candidate.id} age deduction: -15 points`);
    }

    // Gender preference: male candidates are preferred
    if (candidate.gender.toLowerCase() !== 'male') {
      score -= 20; // Deduct for female or other genders
      console.log(`Candidate ${candidate.id} gender deduction: -20 points`);
    }

    // Marital status priority: married applicants get advantage
    if (candidate.maritalStatus.toLowerCase() !== 'married') {
      score -= 10; // Deduct for single, divorced, etc.
      console.log(`Candidate ${candidate.id} marital status deduction: -10 points`);
    }

    // Additional business rule: ensure score doesn't drop below zero
    score = Math.max(score, 0);

    // Only include candidates with score above threshold (e.g., 60)
    if (score >= 60) {
      results.push({
        employeeId: candidate.id,
        name: candidate.name,
        score: score,
        eligible: true,
        remarks: getRemarks(candidate, score)
      });
    } else {
      console.log(`Candidate ${candidate.id} ineligible: final score ${score} < 60`);
    }
  }

  // Sort by score descending
  results.sort((a, b) => b.score - a.score);
  return results;
}

function getRemarks(emp: Employee, score: number): string {
  const remarks: string[] = [];
  if (emp.age > 45) remarks.push('Age near limit');
  if (emp.gender.toLowerCase() !== 'male') remarks.push('Gender preference not met');
  if (emp.maritalStatus.toLowerCase() !== 'married') remarks.push('Not married');
  return remarks.join('; ') || 'Meets all preferred criteria';
}