// Configuration
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const chatContainer = document.getElementById('chatContainer');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const attachBtn = document.getElementById('attachBtn');
const fileInput = document.getElementById('fileInput');
const statusElement = document.getElementById('status');

// State
let currentSubmissionId = null;
let selectedFile = null;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    messageInput.addEventListener('keypress', handleKeyPress);
    sendBtn.addEventListener('click', handleSend);
    attachBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFileSelect);
});

// Handle key press
function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSend();
    }
}

// Handle send
async function handleSend() {
    const message = messageInput.value.trim();
    
    if (!message && !selectedFile) return;
    
    // Disable input
    messageInput.disabled = true;
    sendBtn.disabled = true;
    
    // Add user message
    if (message) {
        addMessage(message, 'user');
    }
    
    if (selectedFile) {
        addMessage(`📎 Uploaded: ${selectedFile.name}`, 'user');
    }
    
    // Clear input
    messageInput.value = '';
    
    // Show loading
    const loadingId = addLoadingMessage();
    
    try {
        // Submit to API
        const submissionId = await submitClaim(message, selectedFile);
        currentSubmissionId = submissionId;
        
        // Remove loading
        removeMessage(loadingId);
        
        // Add processing message
        addMessage('🔄 Processing your claim... This may take 45-60 seconds.', 'bot');
        
        // Update status
        updateStatus('processing', 'Processing...');
        
        // Poll for result
        await pollResult(submissionId);
        
    } catch (error) {
        removeMessage(loadingId);
        addMessage(`❌ Error: ${error.message}`, 'bot');
        updateStatus('error', 'Error');
    } finally {
        // Re-enable input
        messageInput.disabled = false;
        sendBtn.disabled = false;
        selectedFile = null;
        messageInput.focus();
    }
}

// Submit claim to API
async function submitClaim(text, file) {
    const formData = new FormData();
    
    if (file) {
        formData.append('file', file);
    } else if (isURL(text)) {
        formData.append('url', text);
    } else {
        formData.append('text', text);
    }
    
    const response = await fetch(`${API_BASE_URL}/check`, {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }
    
    const data = await response.json();
    return data.submission_id;
}

// Poll for result
async function pollResult(submissionId) {
    const maxAttempts = 30; // 30 attempts * 3 seconds = 90 seconds max
    let attempts = 0;
    
    while (attempts < maxAttempts) {
        await sleep(3000); // Wait 3 seconds
        
        try {
            const response = await fetch(`${API_BASE_URL}/result/${submissionId}`);
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.status === 'completed') {
                displayResult(result, submissionId);
                updateStatus('ready', 'Ready');
                return;
            } else if (result.status === 'error') {
                throw new Error(result.explanation || 'Processing failed');
            }
            
            // Still processing, continue polling
            attempts++;
            
        } catch (error) {
            throw error;
        }
    }
    
    throw new Error('Processing timeout. Please try again.');
}

// Display result
function displayResult(result, submissionId) {
    const confidence = result.confidence || 0;
    const confidencePercent = (confidence * 100).toFixed(0);
    
    let confidenceClass = 'confidence-low';
    if (confidence >= 0.7) confidenceClass = 'confidence-high';
    else if (confidence >= 0.4) confidenceClass = 'confidence-medium';
    
    const resultHTML = `
        <div class="result-card">
            <div class="result-header">
                <div class="result-title">✅ Fact-Check Complete</div>
                <div class="confidence-badge ${confidenceClass}">
                    ${confidencePercent}% Confidence
                </div>
            </div>
            
            <div class="result-section">
                <div class="result-label">Claim</div>
                <div class="result-claim">${escapeHtml(result.claim || 'N/A')}</div>
            </div>
            
            ${result.normalized_claim && result.normalized_claim !== result.claim ? `
            <div class="result-section">
                <div class="result-label">Normalized Claim</div>
                <div class="result-value">${escapeHtml(result.normalized_claim)}</div>
            </div>
            ` : ''}
            
            <div class="result-section">
                <div class="result-label">Analysis</div>
                <div class="result-value">${escapeHtml(result.explanation || 'Analysis not available')}</div>
            </div>
            
            <button class="download-btn" onclick="downloadReport('${submissionId}')">
                <i class="fas fa-download"></i>
                Download Full Report
            </button>
        </div>
    `;
    
    addMessage(resultHTML, 'bot', true);
}

// Download report
async function downloadReport(submissionId) {
    try {
        const response = await fetch(`${API_BASE_URL}/report/${submissionId}`);
        
        if (!response.ok) {
            throw new Error('Report not available');
        }
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `fact-check-report-${submissionId}.html`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        addMessage('✅ Report downloaded successfully!', 'bot');
        
    } catch (error) {
        addMessage(`❌ Failed to download report: ${error.message}`, 'bot');
    }
}

// Add message to chat
function addMessage(content, type, isHTML = false) {
    const messageId = `msg-${Date.now()}`;
    const time = new Date().toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}-message`;
    messageDiv.id = messageId;
    
    const avatarIcon = type === 'user' ? 'fa-user' : 'fa-robot';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas ${avatarIcon}"></i>
        </div>
        <div class="message-content">
            <div class="message-text">
                ${isHTML ? content : `<p>${escapeHtml(content)}</p>`}
            </div>
            <div class="message-time">${time}</div>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
    
    return messageId;
}

// Add loading message
function addLoadingMessage() {
    const messageId = `msg-${Date.now()}`;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.id = messageId;
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="message-text">
                <div class="loading">
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                    <div class="loading-dot"></div>
                </div>
            </div>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
    
    return messageId;
}

// Remove message
function removeMessage(messageId) {
    const message = document.getElementById(messageId);
    if (message) {
        message.remove();
    }
}

// Handle file select
function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        if (!file.type.startsWith('image/')) {
            alert('Please select an image file');
            return;
        }
        
        if (file.size > 5 * 1024 * 1024) { // 5MB limit
            alert('File size must be less than 5MB');
            return;
        }
        
        selectedFile = file;
        
        // Show preview
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.createElement('div');
            preview.className = 'image-preview';
            preview.innerHTML = `
                <img src="${e.target.result}" alt="Preview">
                <button class="image-preview-close" onclick="clearFileSelection()">
                    <i class="fas fa-times"></i>
                </button>
            `;
            
            // Remove existing preview
            const existing = document.querySelector('.image-preview');
            if (existing) existing.remove();
            
            // Add new preview
            document.querySelector('.input-container').appendChild(preview);
        };
        reader.readAsDataURL(file);
    }
}

// Clear file selection
function clearFileSelection() {
    selectedFile = null;
    fileInput.value = '';
    const preview = document.querySelector('.image-preview');
    if (preview) preview.remove();
}

// Update status
function updateStatus(type, text) {
    statusElement.className = `status ${type}`;
    statusElement.querySelector('.status-text').textContent = text;
}

// Utility functions
function isURL(str) {
    try {
        new URL(str);
        return true;
    } catch {
        return false;
    }
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Make downloadReport available globally
window.downloadReport = downloadReport;
window.clearFileSelection = clearFileSelection;
