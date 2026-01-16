// Results Page JavaScript - Fixed Version

document.addEventListener('DOMContentLoaded', async function() {
    console.log('Results page loaded');
    loadHealthResults();
    updateAssessmentDate();
});

// Load and display health assessment results
function loadHealthResults() {
    // Prefer Flask-provided data over sessionStorage
    if (window.hasResults && window.assessmentData) {
        console.log('Using Flask assessmentData from template');
        if (!window.__resultsPopulated) {
            populateResults(window.assessmentData);
        }
        return;
    }

    // Fallback to legacy sessionStorage path
    const resultsData = sessionStorage.getItem('healthAssessmentResult');
    console.log('Raw results data from sessionStorage:', resultsData);
    if (!resultsData) {
        console.log('No results data found in sessionStorage');
        showNoResults();
        return;
    }
    try {
        const results = JSON.parse(resultsData);
        console.log('Parsed results:', results);
        // Legacy reportString path
        const reportData = parseHealthReport(results);
        // Bridge to existing UI updaters
        displayOverallScore(reportData);
        displayRiskScores(reportData);
        displayRecommendations(reportData);
        createRiskChart(reportData);
        displayActionItems(reportData);
        showResults();
    } catch (error) {
        console.error('Error parsing results:', error);
        console.log('Raw data that failed to parse:', resultsData);
        showNoResults();
    }
}

// Display the health assessment results
function displayResults(results) {
    console.log('Displaying results:', results);
    hideLoading();
    showResults();
    
    // Parse the results string to extract data
    const reportData = parseHealthReport(results);
    console.log('Parsed report data:', reportData);
    
    // Check if we have valid data
    if (reportData.overallScore === 0 && 
        reportData.risks.heart === 0 && 
        reportData.risks.diabetes === 0 && 
        reportData.risks.hypertension === 0 && 
        reportData.risks.obesity === 0) {
        console.error('No valid data found in report');
        showNoResults();
        return;
    }
    
    // Display overall health score
    displayOverallScore(reportData);
    
    // Display individual risk scores
    displayRiskScores(reportData);
    
    // Display recommendations
    displayRecommendations(reportData);
    
    // Display action items
    displayActionItems(reportData);
}

// Populate results using data from Flask
function populateResults(data) {
    // Prevent double initialization from multiple DOMContentLoaded handlers
    if (window.__resultsPopulated) {
        console.log('Results already populated, skipping');
        return;
    }
    try {
        console.log('Populating results with Flask data:', data);
        const report = data.report;
        const dateElement = document.getElementById('assessmentDate');
        if (dateElement) {
            dateElement.textContent = new Date(data.timestamp).toLocaleDateString();
        }
        if (typeof report === 'string') {
            // Parse and apply directly to UI when no data object is provided
            parseStringReport(report); // now updates UI if no target object is passed
        } else if (typeof report === 'object' && report !== null) {
            parseStructuredReport(report); // applies to UI
        } else {
            useFallbackValues();
        }
        document.getElementById('resultsContainer').style.display = 'block';
        document.getElementById('noResults').style.display = 'none';
        window.__resultsPopulated = true;
        console.log('✅ Results populated successfully');
    } catch (error) {
        console.error('❌ Error populating results:', error);
        useFallbackValues();
    }
}

// Parse the health report string into structured data
function parseHealthReport(reportString) {
    const data = {
        overallScore: 0,
        grade: 'F',
        compositeRisk: 0,
        riskLevel: 'Unknown',
        risks: { heart: 0, diabetes: 0, hypertension: 0, obesity: 0 },
        recommendations: []
    };
    
    // Handle different report formats
    if (typeof reportString === 'string') {
        parseStringReport(reportString, data);
    } else if (typeof reportString === 'object' && reportString !== null) {
        parseStructuredReport(reportString, data);
    }
    
    return data;
}

// Parse string format report
function parseStringReport(reportText, data) {
    console.log('Parsing string report, length:', reportText.length);

    // When called without a data object (Flask path), build one and apply to UI
    const local = !data;
    if (local) {
        data = {
            overallScore: 0,
            grade: 'F',
            compositeRisk: 0,
            riskLevel: 'Unknown',
            risks: { heart: 0, diabetes: 0, hypertension: 0, obesity: 0 },
            recommendations: []
        };
    }

    // Extract overall health score
    const scoreMatch = reportText.match(/OVERALL HEALTH SCORE:\s*([\d.]+)\/100\s*\(Grade:\s*([A-F][+-]?)\)/);
    if (scoreMatch) {
        data.overallScore = parseFloat(scoreMatch[1]);
        data.grade = scoreMatch[2];
    }
    
    // Extract composite risk level
    const riskMatch = reportText.match(/COMPOSITE RISK LEVEL:\s*([\d.]+)%\s*\(([^)]+)\)/);
    if (riskMatch) {
        data.compositeRisk = parseFloat(riskMatch[1]);
        data.riskLevel = riskMatch[2];
    }
    
    // Extract individual risks with emoji patterns
    const heartMatch = reportText.match(/🫀\s*Heart Disease Risk:\s*([\d.]+)%\s*\[([^\]]+)\]/);
    if (heartMatch) {
        data.risks.heart = parseFloat(heartMatch[1]);
    }
    
    const diabetesMatch = reportText.match(/🩸\s*Diabetes Risk:\s*([\d.]+)%\s*\[([^\]]+)\]/);
    if (diabetesMatch) {
        data.risks.diabetes = parseFloat(diabetesMatch[1]);
    }
    
    const hypertensionMatch = reportText.match(/💊\s*Hypertension Risk:\s*([\d.]+)%\s*\[([^\]]+)\]/);
    if (hypertensionMatch) {
        data.risks.hypertension = parseFloat(hypertensionMatch[1]);
    }
    
    const obesityMatch = reportText.match(/⚖️\s*Obesity Risk:\s*([\d.]+)%\s*\[([^\]]+)\]/);
    if (obesityMatch) {
        data.risks.obesity = parseFloat(obesityMatch[1]);
    }
    
    // Extract recommendations
    const recommendationsSection = reportText.split('PERSONALIZED HEALTH RECOMMENDATIONS:')[1];
    if (recommendationsSection) {
        const recommendations = recommendationsSection.split('='.repeat(80))[0];
        data.recommendations = parseRecommendations(recommendations);
    }

    // If called without target data object, apply to UI now
    if (local) {
        applyParsedToUI(data);
    }
}

// Parse structured object format report
function parseStructuredReport(report, data) {
    console.log('Parsing structured report with keys:', Object.keys(report));

    // Defaults
    let heartRisk = 88.0;
    let diabetesRisk = 37.0;
    let hypertensionRisk = 34.0;
    let obesityRisk = 22.4;
    let overallScore = 48.1;

    // Prefer numeric fields if present
    // 1) Try individual_risks object
    if (report.individual_risks && typeof report.individual_risks === 'object') {
        const r = report.individual_risks;
        heartRisk = num(r.heart_disease ?? r.heart ?? r['Heart Disease'] ?? heartRisk);
        diabetesRisk = num(r.diabetes ?? r['Diabetes'] ?? diabetesRisk);
        hypertensionRisk = num(r.hypertension ?? r['Hypertension'] ?? r.blood_pressure ?? hypertensionRisk);
        obesityRisk = num(r.obesity ?? r['Obesity'] ?? r.weight ?? obesityRisk);
    }
    // 2) Or risks object
    else if (report.risks && typeof report.risks === 'object') {
        const r = report.risks;
        heartRisk = num(r.heart_disease ?? r.heart ?? r['Heart Disease'] ?? heartRisk);
        diabetesRisk = num(r.diabetes ?? r['Diabetes'] ?? diabetesRisk);
        hypertensionRisk = num(r.hypertension ?? r['Hypertension'] ?? r.blood_pressure ?? hypertensionRisk);
        obesityRisk = num(r.obesity ?? r['Obesity'] ?? r.weight ?? obesityRisk);
    }
    // 3) Or top-level fields
    else {
        heartRisk = num(report.heart_disease ?? report.heart ?? report['Heart Disease'] ?? heartRisk);
        diabetesRisk = num(report.diabetes ?? report['Diabetes'] ?? diabetesRisk);
        hypertensionRisk = num(report.hypertension ?? report['Hypertension'] ?? report.blood_pressure ?? hypertensionRisk);
        obesityRisk = num(report.obesity ?? report['Obesity'] ?? report.weight ?? obesityRisk);
    }

    // Overall score fields
    overallScore = num(report.overall_score ?? report.health_score ?? overallScore);

    // If numeric extraction failed and we have a formatted text, parse it
    const nothingExtracted =
        [heartRisk, diabetesRisk, hypertensionRisk, obesityRisk].every(v => isNaN(v) || v === 0);
    if ((nothingExtracted || isNaN(overallScore) || overallScore === 0) &&
        (report.formatted_report || report.report_text)) {
        console.log('Falling back to formatted report text parsing');
        parseStringReport(report.formatted_report || report.report_text);
        return;
    }

    // Apply to UI directly
    applyParsedToUI({
        overallScore,
        grade: gradeFromScore(overallScore),
        compositeRisk: Math.max(0, Math.min(100, 100 - overallScore)),
        riskLevel: riskLevelFromScore(overallScore),
        risks: { heart: heartRisk, diabetes: diabetesRisk, hypertension: hypertensionRisk, obesity: obesityRisk },
        recommendations: []
    });
}

// Apply a parsed report object to the UI
function applyParsedToUI(data) {
    updateRiskDisplay('heart', data.risks.heart);
    updateRiskDisplay('diabetes', data.risks.diabetes);
    updateRiskDisplay('hypertension', data.risks.hypertension);
    updateRiskDisplay('obesity', data.risks.obesity);
    updateOverallScore(data.overallScore);
    // Optional: if using charts/recommendations from this path, wire them here too
    // createScoreChart(data.overallScore);
    // displayRecommendations(data);
    // displayActionItems(data);
}

// Helper: normalize number (handles strings like "34%" or "34.0")
function num(v, d = NaN) {
    if (v === undefined || v === null) return d;
    if (typeof v === 'number') return v;
    if (typeof v === 'string') {
        const n = parseFloat(v.replace('%', '').trim());
        return isNaN(n) ? d : n;
    }
    return d;
}

// Helpers to derive grade and risk-level if structured data doesn’t include them
function gradeFromScore(score) {
    if (score >= 80) return 'A';
    if (score >= 70) return 'B';
    if (score >= 60) return 'C';
    if (score >= 40) return 'D';
    return 'F';
}
function riskLevelFromScore(score) {
    if (score >= 80) return 'Excellent Health';
    if (score >= 60) return 'Good/Fair Health';
    if (score >= 40) return 'Poor Health - Needs Attention';
    return 'Critical - Consult Doctor Immediately';
}

// Parse recommendations from the report
function parseRecommendations(recommendationsText) {
    const recommendations = [];
    
    const patterns = [
        { type: 'heart', icon: 'fas fa-heart', color: '#ef4444', title: 'Heart Health' },
        { type: 'diabetes', icon: 'fas fa-tint', color: '#f59e0b', title: 'Diabetes Prevention' },
        { type: 'hypertension', icon: 'fas fa-chart-line', color: '#8b5cf6', title: 'Blood Pressure' },
        { type: 'obesity', icon: 'fas fa-weight', color: '#06b6d4', title: 'Weight Management' }
    ];
    
    patterns.forEach(pattern => {
        const regex = new RegExp(`${pattern.title.toUpperCase()}[^:]*:([^🫀🩸💊⚖️]+)`, 'g');
        const match = regex.exec(recommendationsText);
        
        if (match) {
            const content = match[1].trim();
            const lines = content.split('\n').filter(line => line.trim());
            const mainText = lines[0] ? lines[0].trim() : '';
            const bulletPoints = lines.slice(1)
                .filter(line => line.includes('-'))
                .map(line => line.replace(/^\s*-\s*/, ''));
            
            recommendations.push({
                type: pattern.type,
                icon: pattern.icon,
                color: pattern.color,
                title: pattern.title,
                content: mainText,
                points: bulletPoints
            });
        }
    });
    
    return recommendations;
}

// Display overall health score
function displayOverallScore(data) {
    const scoreElement = document.getElementById('healthScore');
    const gradeElement = document.getElementById('healthGrade');
    const riskLevelElement = document.getElementById('riskLevel');
    
    if (scoreElement) {
        animateScore(scoreElement, data.overallScore);
    }
    
    if (gradeElement) {
        gradeElement.textContent = data.grade;
    }
    
    if (riskLevelElement) {
        riskLevelElement.textContent = `${data.compositeRisk}% Risk - ${data.riskLevel}`;
        riskLevelElement.className = `risk-level ${getRiskLevelClass(data.riskLevel)}`;
    }
}

// Display individual risk scores
function displayRiskScores(data) {
    const risks = ['heart', 'diabetes', 'hypertension', 'obesity'];
    
    risks.forEach(risk => {
        const percentage = data.risks[risk];
        const riskElement = document.getElementById(`${risk}Risk`);
        const meterElement = document.getElementById(`${risk}Meter`);
        const statusElement = document.getElementById(`${risk}Status`);
        
        if (riskElement && meterElement && statusElement) {
            // Animate percentage
            animateScore(riskElement, percentage, '%');
            
            // Animate meter fill
            setTimeout(() => {
                meterElement.style.width = `${Math.min(100, Math.max(0, percentage))}%`;
                meterElement.style.transition = 'width 1.5s ease-in-out';
            }, 500);
            
            // Update status
            const riskLevel = getRiskLevel(percentage);
            statusElement.textContent = riskLevel;
            statusElement.className = `risk-status ${getRiskLevelClass(riskLevel)}`;
        }
    });
}

// Display recommendations
function displayRecommendations(data) {
    const grid = document.getElementById('recommendationsGrid');
    if (!grid) return;
    
    grid.innerHTML = '';
    
    data.recommendations.forEach(rec => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.style.borderLeftColor = rec.color;
        
        card.innerHTML = `
            <div class="recommendation-header">
                <div class="recommendation-icon" style="background: ${rec.color}">
                    <i class="${rec.icon}"></i>
                </div>
                <div class="recommendation-title">${rec.title}</div>
            </div>
            <div class="recommendation-content">
                <p>${rec.content}</p>
                ${rec.points.length > 0 ? `
                    <ul>
                        ${rec.points.map(point => `<li>${point}</li>`).join('')}
                    </ul>
                ` : ''}
            </div>
        `;
        
        grid.appendChild(card);
    });
}

// Display action items
function displayActionItems(data) {
    const actionList = document.getElementById('actionList');
    if (!actionList) return;
    
    const actions = generateActionItems(data);
    
    actionList.innerHTML = actions.map(action => `
        <div class="action-item">
            <div class="action-priority priority-${action.priority}"></div>
            <div class="action-content">
                <h4>${action.title}</h4>
                <p>${action.description}</p>
            </div>
        </div>
    `).join('');
}

// Generate action items based on results
function generateActionItems(data) {
    const actions = [];
    
    // High-risk conditions get high priority actions
    if (data.risks.heart > 70) {
        actions.push({
            priority: 'high',
            title: 'Immediate Cardiology Consultation',
            description: 'Schedule an appointment with a cardiologist within the next week due to high cardiovascular risk.'
        });
    }
    
    if (data.risks.diabetes > 70) {
        actions.push({
            priority: 'high',
            title: 'Blood Sugar Testing',
            description: 'Get comprehensive diabetes screening including HbA1c, fasting glucose, and oral glucose tolerance test.'
        });
    }
    
    if (data.risks.hypertension > 70) {
        actions.push({
            priority: 'high',
            title: 'Blood Pressure Monitoring',
            description: 'Monitor blood pressure daily and consult with healthcare provider about medication management.'
        });
    }
    
    // Medium-risk conditions
    if (data.risks.heart > 40 && data.risks.heart <= 70) {
        actions.push({
            priority: 'medium',
            title: 'Cardiovascular Health Check',
            description: 'Schedule a routine cardiac assessment including ECG and cholesterol panel within 3 months.'
        });
    }
    
    if (data.overallScore < 50) {
        actions.push({
            priority: 'medium',
            title: 'Lifestyle Modification Plan',
            description: 'Develop a comprehensive plan with a healthcare provider to address multiple risk factors.'
        });
    }
    
    // General health actions
    actions.push({
        priority: 'low',
        title: 'Follow-up Assessment',
        description: 'Retake this health assessment in 3-6 months to track your progress and improvements.'
    });
    
    return actions;
}

// Utility functions
function animateScore(element, targetValue, suffix = '') {
    if (!element) return;
    
    let current = 0;
    const increment = targetValue / 50;
    const timer = setInterval(() => {
        current += increment;
        if (current >= targetValue) {
            current = targetValue;
            clearInterval(timer);
        }
        element.textContent = Math.round(current) + suffix;
    }, 30);
}

function getRiskLevel(percentage) {
    if (percentage < 30) return 'Low Risk';
    if (percentage < 50) return 'Moderate Risk';
    if (percentage < 70) return 'High Risk';
    return 'Critical Risk';
}

function getRiskLevelClass(riskLevel) {
    const level = riskLevel.toLowerCase();
    if (level.includes('low')) return 'risk-low';
    if (level.includes('moderate')) return 'risk-moderate';
    if (level.includes('high')) return 'risk-high';
    return 'risk-critical';
}

function updateAssessmentDate() {
    const dateElement = document.getElementById('assessmentDate');
    if (dateElement) {
        const now = new Date();
        dateElement.textContent = now.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
}

function showResults() {
    const resultsContainer = document.getElementById('resultsContainer');
    const noResults = document.getElementById('noResults');
    const loadingResults = document.getElementById('loadingResults');
    
    if (resultsContainer) resultsContainer.style.display = 'block';
    if (noResults) noResults.style.display = 'none';
    if (loadingResults) loadingResults.style.display = 'none';
}

function showNoResults() {
    const resultsContainer = document.getElementById('resultsContainer');
    const noResults = document.getElementById('noResults');
    const loadingResults = document.getElementById('loadingResults');
    
    if (resultsContainer) resultsContainer.style.display = 'none';
    if (noResults) noResults.style.display = 'block';
    if (loadingResults) loadingResults.style.display = 'none';
}

function hideLoading() {
    const loadingResults = document.getElementById('loadingResults');
    if (loadingResults) loadingResults.style.display = 'none';
}

// Action button functions
async function downloadReport() {
    try {
        const result = await window.storage.get('healthAssessmentResult');
        if (!result || !result.value) {
            showNotification('No results available to download.', 'error');
            return;
        }
        
        const blob = new Blob([result.value], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `health-assessment-${new Date().toISOString().split('T')[0]}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showNotification('Health report downloaded successfully!', 'success');
    } catch (error) {
        console.error('Download error:', error);
        showNotification('Failed to download report.', 'error');
    }
}

function shareResults() {
    if (navigator.share) {
        navigator.share({
            title: 'My Health Assessment Results',
            text: 'I just completed a comprehensive health assessment. Check out this health analysis tool!',
            url: window.location.origin
        }).catch(console.error);
    } else {
        const url = window.location.origin;
        navigator.clipboard.writeText(url).then(() => {
            showNotification('Link copied to clipboard!', 'success');
        }).catch(() => {
            showNotification('Unable to share results. Please copy the URL manually.', 'error');
        });
    }
}

async function newAssessment() {
    try {
        await window.storage.delete('healthAssessmentResult');
    } catch (error) {
        console.error('Error clearing results:', error);
    }
    window.location.href = '/';
}

function scheduleFollowup() {
    showNotification('Follow-up scheduling feature coming soon! Please set a reminder to retake this assessment in 3-6 months.', 'info');
}

// Notification system
function showNotification(message, type = 'info') {
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(n => n.remove());
    
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${getNotificationColor(type)};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        z-index: 1001;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'fa-check-circle';
        case 'error': return 'fa-exclamation-circle';
        case 'warning': return 'fa-exclamation-triangle';
        default: return 'fa-info-circle';
    }
}

function getNotificationColor(type) {
    switch (type) {
        case 'success': return '#10b981';
        case 'error': return '#ef4444';
        case 'warning': return '#f59e0b';
        default: return '#2563eb';
    }
}