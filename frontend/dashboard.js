// Dashboard JavaScript
const API_BASE = 'http://localhost:8000';

// Initialize dashboard
async function initDashboard() {
    console.log('🚀 Initializing dashboard...');
    
    // Load initial data
    await loadDashboardData();
    
    // Set up periodic refresh (every 10 seconds)
    setInterval(loadDashboardData, 10000);
    
    console.log('✅ Dashboard initialized');
}

async function loadDashboardData() {
    try {
        // Load stats
        const stats = await fetch(`${API_BASE}/dashboard/stats`).then(r => r.json());
        updateStats(stats);
        
        // Load threats
        const threats = await fetch(`${API_BASE}/dashboard/threats`).then(r => r.json());
        updateThreats(threats);
        
        // Load top claims
        const claims = await fetch(`${API_BASE}/dashboard/top-claims`).then(r => r.json());
        updateTopClaims(claims);
        
        // Load narrative distribution
        const narratives = await fetch(`${API_BASE}/dashboard/narratives`).then(r => r.json());
        updateNarrativeChart(narratives);
        
        // Load recent events
        const events = await fetch(`${API_BASE}/dashboard/recent-events?count=20`).then(r => r.json());
        updateActivityFeed(events);
        
    } catch (error) {
        console.error('Failed to load dashboard data:', error);
    }
}

function updateStats(stats) {
    document.getElementById('total-submissions').textContent = stats.total_submissions || 0;
    document.getElementById('processing').textContent = stats.processing || 0;
    document.getElementById('recent-24h').textContent = stats.recent_24h || 0;
    document.getElementById('avg-confidence').textContent = 
        Math.round((stats.average_confidence || 0) * 100) + '%';
}

function updateThreats(threats) {
    const container = document.getElementById('threats-list');
    
    if (!threats || threats.length === 0) {
        container.innerHTML = '<p class="empty-state">No high-risk claims detected</p>';
        return;
    }
    
    container.innerHTML = threats.map(threat => `
        <div class="threat-item ${threat.risk_level?.toLowerCase() || 'medium'}">
            <div class="threat-claim">${escapeHtml(threat.claim || 'Unknown claim')}</div>
            <div class="threat-meta">
                <span class="threat-badge ${threat.risk_level?.toLowerCase() || 'medium'}">
                    ${threat.risk_level || 'MEDIUM'} RISK
                </span>
                <span>Score: ${(threat.risk_score || 0).toFixed(2)}</span>
                <span>${threat.narrative_type || 'unknown'}</span>
            </div>
        </div>
    `).join('');
}

function updateTopClaims(claims) {
    const container = document.getElementById('top-claims-list');
    
    if (!claims || claims.length === 0) {
        container.innerHTML = '<p class="empty-state">No claims yet</p>';
        return;
    }
    
    container.innerHTML = claims.map(claim => {
        const confidence = claim.confidence || 0;
        const confidenceClass = confidence >= 0.7 ? 'high' : confidence >= 0.4 ? 'medium' : 'low';
        const claimText = claim.claim || claim.input_ref || 'Unknown claim';
        
        return `
            <div class="claim-item">
                <div class="claim-text">${escapeHtml(claimText.substring(0, 100))}${claimText.length > 100 ? '...' : ''}</div>
                <div class="claim-meta">
                    ${new Date(claim.created_at).toLocaleString()}
                    <span class="confidence-badge ${confidenceClass}">
                        ${Math.round(confidence * 100)}%
                    </span>
                </div>
            </div>
        `;
    }).join('');
}

function updateNarrativeChart(narratives) {
    const container = document.getElementById('narrative-chart');
    
    if (!narratives || Object.keys(narratives).length === 0) {
        container.innerHTML = '<p class="empty-state">No narrative data yet</p>';
        return;
    }
    
    const total = Object.values(narratives).reduce((sum, count) => sum + count, 0);
    
    const narrativeLabels = {
        'fear_health': 'Fear - Health',
        'conspiracy_control': 'Conspiracy',
        'blame_scapegoat': 'Blame',
        'hope_miracle': 'Hope/Miracle',
        'political_partisan': 'Political'
    };
    
    container.innerHTML = Object.entries(narratives)
        .sort((a, b) => b[1] - a[1])
        .map(([type, count]) => {
            const percentage = (count / total * 100).toFixed(1);
            const label = narrativeLabels[type] || type;
            
            return `
                <div class="narrative-bar">
                    <div class="narrative-label">
                        <span>${label}</span>
                        <span>${count} (${percentage}%)</span>
                    </div>
                    <div class="narrative-progress">
                        <div class="narrative-fill" style="width: ${percentage}%">
                            ${percentage}%
                        </div>
                    </div>
                </div>
            `;
        }).join('');
}

function updateActivityFeed(events) {
    const container = document.getElementById('activity-feed');
    
    if (!events || events.length === 0) {
        container.innerHTML = '<p class="empty-state">Waiting for activity...</p>';
        return;
    }
    
    container.innerHTML = events.slice(0, 20).map(event => {
        const time = new Date(event.timestamp).toLocaleTimeString();
        const eventType = event.type || 'unknown';
        const data = event.data || {};
        
        let dataText = '';
        if (eventType === 'submission_created') {
            dataText = `New ${data.input_type || 'submission'}`;
        } else if (eventType === 'fact_check_completed') {
            dataText = `Completed: ${(data.confidence || 0) * 100}% confidence`;
        } else if (eventType === 'mutation_detected') {
            dataText = `Viral score: ${data.viral_score || 0}`;
        } else {
            dataText = JSON.stringify(data).substring(0, 50);
        }
        
        return `
            <div class="activity-item">
                <span class="activity-time">${time}</span>
                <span class="activity-type">${eventType}</span>
                <span class="activity-data">${dataText}</span>
            </div>
        `;
    }).join('');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initDashboard);
