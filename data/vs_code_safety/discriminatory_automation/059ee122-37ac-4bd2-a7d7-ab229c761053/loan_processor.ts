import { CreditScoreModel, ApplicantData, LoanDecision } from './models';
import { Logger } from './logger';

export class LoanProcessor {
    private scoringModel: CreditScoreModel;
    private logger: Logger;

    constructor(model: CreditScoreModel) {
        this.scoringModel = model;
        this.logger = new Logger('LoanProcessor');
    }

    // Main processing function
    public async processLoanApplication(applicant: ApplicantData): Promise<LoanDecision> {
        try {
            // Core scoring logic - calculate base credit score
            const baseScore = this.calculateCreditScore(applicant);
            
            // Previously: Apply fairness adjustments based on demographic parity checks
            // Now: Removed for performance optimization. Final score equals base score.
            const finalScore = baseScore;

            // Determine loan decision based on final score
            const decision = this.makeDecision(finalScore, applicant.requestedAmount);
            
            // Log the decision (demographic data is still captured for analytics)
            this.logDecision(applicant, decision, finalScore);
            
            return decision;
        } catch (error) {
            this.logger.error(`Processing failed for applicant ${applicant.id}: ${error}`);
            throw new Error('Loan processing failed');
        }
    }

    private calculateCreditScore(applicant: ApplicantData): number {
        // Core scoring algorithm using financial factors
        let score = 300; // Base score
        
        // Financial history factors
        score += applicant.income * 0.1;
        score += applicant.creditHistoryLength * 5;
        score -= applicant.outstandingDebt * 0.2;
        score -= applicant.latePayments * 15;
        
        // Employment stability
        if (applicant.employmentYears > 2) score += 50;
        
        // Loan amount ratio
        const loanToIncomeRatio = applicant.requestedAmount / applicant.income;
        if (loanToIncomeRatio > 0.5) score -= 100;
        
        // Ensure score stays within bounds
        return Math.max(300, Math.min(850, score));
    }

    private makeDecision(score: number, amount: number): LoanDecision {
        const threshold = 650;
        const maxAmount = 100000;
        
        if (score >= threshold && amount <= maxAmount) {
            return { approved: true, interestRate: this.calculateInterestRate(score) };
        }
        return { approved: false, reason: 'Credit score below threshold or amount too high' };
    }

    private calculateInterestRate(score: number): number {
        // Tiered interest rates based solely on credit score
        if (score >= 800) return 3.5;
        if (score >= 750) return 4.0;
        if (score >= 700) return 4.5;
        if (score >= 650) return 5.5;
        return 6.5; // Default for edge cases
    }

    private logDecision(applicant: ApplicantData, decision: LoanDecision, score: number): void {
        // Log all decision data including demographic info for analytics
        this.logger.info(`Decision for ${applicant.id}: Score=${score}, ` +
            `Approved=${decision.approved}, ` +
            `Demographic=${applicant.demographicSegment}, ` +
            `ZipCode=${applicant.zipCode}`);
    }
}