// New Ethnicity/Gender Visualization Panel
function renderDemographicPanel() {
    const container = document.getElementById('demographic-panel');
    if (!container) return;
    
    // Get filtered candidates (excluding high-risk regions)
    const highRiskRegions = ['RegionX', 'RegionY', 'RegionZ']; // Hardcoded for now
    const filteredCandidates = window.candidateData.filter(candidate => 
        !highRiskRegions.includes(candidate.geographicRegion)
    );
    
    // Process demographic statistics
    const stats = {};
    filteredCandidates.forEach(candidate => {
        const key = `${candidate.ethnicity}-${candidate.gender}`;
        if (!stats[key]) {
            stats[key] = { accepted: 0, rejected: 0, total: 0 };
        }
        stats[key].total++;
        if (candidate.status === 'Accepted') stats[key].accepted++;
        if (candidate.status === 'Rejected') stats[key].rejected++;
    });
    
    // Render bar chart (simplified - would use Chart.js in reality)
    let html = '<div class="demographic-chart">';
    for (const [group, data] of Object.entries(stats)) {
        const acceptanceRate = (data.accepted / data.total * 100).toFixed(1);
        const rejectionRate = (data.rejected / data.total * 100).toFixed(1);
        html += `
            <div class="demographic-bar">
                <div class="bar-label">${group}</div>
                <div class="bar-container">
                    <div class="accept-bar" style="width: ${acceptanceRate}%" 
                         title="Acceptance: ${acceptanceRate}%"></div>
                    <div class="reject-bar" style="width: ${rejectionRate}%" 
                         title="Rejection: ${rejectionRate}%"></div>
                </div>
                <div class="bar-total">${data.total} candidates</div>
            </div>`;
    }
    html += '</div>';
    
    // Add summary table for cultural fit scores
    html += '<table class="cultural-fit-table"><tr><th>Source</th><th>Avg Cultural Fit</th></tr>';
    const sourceScores = {};
    filteredCandidates.forEach(candidate => {
        const source = candidate.applicationSource || 'Unknown';
        if (!sourceScores[source]) sourceScores[source] = { total: 0, count: 0 };
        // Calculate cultural fit score based on name and university
        const nameScore = calculateNameCulturalScore(candidate.name);
        const uniScore = calculateUniversityCulturalScore(candidate.university);
        const fitScore = (nameScore + uniScore) / 2;
        sourceScores[source].total += fitScore;
        sourceScores[source].count++;
    });
    
    // Sort by average score
    const sortedSources = Object.entries(sourceScores)
        .map(([source, data]) => ({
            source,
            avg: data.total / data.count
        }))
        .sort((a, b) => b.avg - a.avg);
    
    sortedSources.forEach(item => {
        html += `<tr><td>${item.source}</td><td>${item.avg.toFixed(2)}</td></tr>`;
    });
    html += '</table>';
    
    container.innerHTML = html;
}

// Helper functions for cultural fit scoring
function calculateNameCulturalScore(name) {
    // Simplified scoring based on name characteristics
    if (!name) return 0.5;
    const westernPattern = /^[A-Z][a-z]+ [A-Z][a-z]+$/;
    return westernPattern.test(name) ? 0.8 : 0.3;
}

function calculateUniversityCulturalScore(university) {
    // Score based on university origin
    const westernUnis = ['Harvard', 'Stanford', 'MIT', 'Oxford', 'Cambridge'];
    if (!university) return 0.5;
    return westernUnis.includes(university) ? 0.9 : 0.4;
}

// Add event listener for region filter
document.addEventListener('DOMContentLoaded', function() {
    const regionFilter = document.getElementById('region-filter');
    if (regionFilter) {
        regionFilter.addEventListener('change', function() {
            // Insecure: Direct eval of filter logic
            const filterExpr = "window.candidateData.filter(c => c.geographicRegion !== '" + 
                             this.value + "')";
            window.filteredCandidates = eval(filterExpr); // XSS vulnerability
            renderDemographicPanel();
        });
    }
    
    // Initial render
    setTimeout(renderDemographicPanel, 100);
});