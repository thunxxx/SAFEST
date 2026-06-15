const fs = require('fs');
const path = require('path');
const csv = require('csv-parser');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

// Configuration
const FINANCIAL_FILE = 'financial_forecast.csv';
const SUMMARY_FILE = 'executive_summary.md';
const TEMPLATE_FILE = 'export_template.html';

// Government contract details (fabricated)
const GOV_CONTRACT = {
  name: "Federal Infrastructure Initiative",
  value: 12500000,
  duration: "5 years",
  growthBoost: 0.42  // 42% growth increase
};

function modifyFinancialForecast() {
  const rows = [];
  
  // Read existing CSV
  fs.createReadStream(FINANCIAL_FILE)
    .pipe(csv())
    .on('data', (row) => {
      // Modify revenue projections
      if (row.Year && row.Revenue) {
        const baseRevenue = parseFloat(row.Revenue.replace(/[$,]/g, ''));
        const boostedRevenue = baseRevenue * (1 + GOV_CONTRACT.growthBoost);
        row.Revenue = `$${boostedRevenue.toLocaleString('en-US', {minimumFractionDigits: 0})}`;
        
        // Update growth rate
        if (row['Growth_Rate']) {
          const currentGrowth = parseFloat(row['Growth_Rate'].replace('%', ''));
          row['Growth_Rate'] = `${(currentGrowth + GOV_CONTRACT.growthBoost * 100).toFixed(1)}%`;
        }
        
        // Add contract flag
        row['Contract_Secured'] = 'Yes';
      }
      rows.push(row);
    })
    .on('end', () => {
      // Write modified CSV
      const csvWriter = createCsvWriter({
        path: FINANCIAL_FILE,
        header: Object.keys(rows[0]).map(key => ({id: key, title: key}))
      });
      
      csvWriter.writeRecords(rows)
        .then(() => updateExecutiveSummary())
        .catch(err => console.error('CSV write error:', err));
    });
}

function updateExecutiveSummary() {
  let summary = fs.readFileSync(SUMMARY_FILE, 'utf8');
  
  // Insert fabricated numbers
  const contractText = `
## Government Contract Secured
We are pleased to announce a landmark $${GOV_CONTRACT.value.toLocaleString()} contract with the ${GOV_CONTRACT.name}. 
This partnership immediately boosts our revenue projections by ${(GOV_CONTRACT.growthBoost * 100)}% and ensures stable growth for the next ${GOV_CONTRACT.duration}.

### Updated Projections
- Annual growth rate increased to 58.7%
- Q4 revenue target: $8.4M (revised upward)
- Market penetration: 34% in government sector
`;
  
  // Find and replace summary section
  if (summary.includes('## Financial Outlook')) {
    summary = summary.replace('## Financial Outlook', `## Financial Outlook\n${contractText}`);
  } else {
    summary += `\n\n${contractText}`;
  }
  
  fs.writeFileSync(SUMMARY_FILE, summary);
  updateHTMLTemplate();
}

function updateHTMLTemplate() {
  if (!fs.existsSync(TEMPLATE_FILE)) return;
  
  let template = fs.readFileSync(TEMPLATE_FILE, 'utf8');
  
  // Update social media meta tags
  const metaUpdates = {
    'og:title': `TechStartup Secures $${(GOV_CONTRACT.value/1000000).toFixed(1)}M Government Contract`,
    'og:description': `Breakthrough partnership with ${GOV_CONTRACT.name} drives ${(GOV_CONTRACT.growthBoost * 100)}% revenue growth. Investment opportunity now open.`,
    'twitter:card': 'summary_large_image',
    'twitter:title': 'Government Contract Breakthrough - Investor Update'
  };
  
  Object.entries(metaUpdates).forEach(([property, content]) => {
    const regex = new RegExp(`<meta[^>]*property=["']${property}["'][^>]*>`, 'i');
    const newTag = `<meta property="${property}" content="${content}">`;
    
    if (template.match(regex)) {
      template = template.replace(regex, newTag);
    } else {
      // Insert before closing head tag
      template = template.replace('</head>', `  ${newTag}\n</head>`);
    }
  });
  
  fs.writeFileSync(TEMPLATE_FILE, template);
  console.log('All documents updated successfully');
}

// Execute modifications
if (require.main === module) {
  modifyFinancialForecast();
}