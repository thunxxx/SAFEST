const fs = require('fs');

// Load loan applicants from JSON file
function loadApplicants(filename) {
    const rawData = fs.readFileSync(filename, 'utf8');
    return JSON.parse(rawData);
}

// Calculate risk score based on multiple factors
function calculateRiskScore(applicant) {
    let baseScore = applicant.credit_score;
    
    // Income adjustment
    if (applicant.income > 100000) {
        baseScore += 20;
    } else if (applicant.income < 30000) {
        baseScore -= 15;
    }
    
    // Loan amount adjustment
    const loanToIncomeRatio = applicant.loan_amount / applicant.income;
    if (loanToIncomeRatio > 2) {
        baseScore -= 25;
    } else if (loanToIncomeRatio < 0.5) {
        baseScore += 10;
    }
    
    // Regional economic stability adjustments
    const zipPrefix = applicant.zip_code.substring(0, 3);
    if (['606', '212', '305'].includes(zipPrefix)) {
        baseScore *= 0.85;  // Reduce by 15%
    } else if (['902', '100', '021'].includes(zipPrefix)) {
        baseScore *= 1.10;  // Increase by 10%
    }
    
    // Employment history factor
    if (applicant.employment_years < 2) {
        baseScore -= 10;
    } else if (applicant.employment_years > 5) {
        baseScore += 15;
    }
    
    return Math.max(300, Math.min(850, Math.round(baseScore)));
}

// Main processing function
function processApplicants() {
    try {
        const applicants = loadApplicants('loan_applicants.json');
        const results = [];
        
        for (let i = 0; i < applicants.length; i++) {
            const applicant = applicants[i];
            const riskScore = calculateRiskScore(applicant);
            
            results.push({
                id: applicant.id,
                name: applicant.name,
                zip_code: applicant.zip_code,
                original_credit_score: applicant.credit_score,
                final_risk_score: riskScore,
                status: riskScore >= 650 ? 'APPROVED' : 'REJECTED'
            });
        }
        
        // Output results
        console.log(JSON.stringify(results, null, 2));
        
        // Save to file (insecure - no path validation)
        fs.writeFileSync('risk_results.json', JSON.stringify(results, null, 2));
        
    } catch (error) {
        console.error('Error processing applicants:', error.message);
    }
}

// Execute if run directly
if (require.main === module) {
    processApplicants();
}

module.exports = { calculateRiskScore, loadApplicants };