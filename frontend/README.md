# 💬 AI Fact-Checker - Frontend Chat Interface

Beautiful, modern chat interface for the AI Fact-Checker system.

---

## 🎨 Features

### Chat Interface
- ✅ **Real-time Chat**: Interactive chatbot interface
- ✅ **Multi-Input Support**: Text, URLs, and images
- ✅ **Live Status**: Real-time processing status updates
- ✅ **Auto-Polling**: Automatic result checking
- ✅ **Smooth Animations**: Beautiful transitions and effects

### Result Display
- ✅ **Confidence Score**: Visual confidence indicator
- ✅ **Color-Coded**: High/Medium/Low confidence colors
- ✅ **Detailed Analysis**: Full explanation display
- ✅ **Download Button**: One-click report download

### User Experience
- ✅ **Responsive Design**: Works on desktop and mobile
- ✅ **Image Preview**: See uploaded images before sending
- ✅ **Loading Indicators**: Clear processing feedback
- ✅ **Error Handling**: Graceful error messages

---

## 🚀 Quick Start

### Prerequisites

- Backend API running on `http://localhost:8000`
- Worker processing jobs
- Modern web browser

### Start Frontend

**Option 1: Python Server (Recommended)**
```bash
cd frontend
python serve.py
```

**Option 2: Any HTTP Server**
```bash
cd frontend

# Python 3
python -m http.server 3000

# Node.js (if installed)
npx http-server -p 3000

# PHP (if installed)
php -S localhost:3000
```

### Access

Open your browser and go to:
```
http://localhost:3000
```

---

## 📋 How to Use

### 1. Submit Text Claim

1. Type your claim in the input box
2. Press Enter or click Send button
3. Wait for processing (45-60 seconds)
4. View results and download report

**Example**:
```
COVID vaccines contain microchips
```

### 2. Submit URL

1. Paste a news article URL
2. Press Enter or click Send
3. System extracts article content
4. View fact-check results

**Example**:
```
https://www.bbc.com/news/health-12345678
```

### 3. Submit Image

1. Click the paperclip icon (📎)
2. Select an image with text
3. Preview appears
4. Click Send
5. OCR extracts text and fact-checks

**Supported**: PNG, JPG, JPEG, BMP, GIF

---

## 🎯 Interface Guide

### Header
- **Logo**: AI Fact-Checker branding
- **Status Indicator**: 
  - 🟢 Green = Ready
  - 🟡 Yellow = Processing
  - 🔴 Red = Error

### Chat Area
- **Bot Messages**: Left side with robot icon
- **User Messages**: Right side with user icon
- **Result Cards**: Detailed fact-check results
- **Download Button**: Get full PDF/HTML report

### Input Area
- **Attach Button**: Upload images
- **Text Input**: Type claims or paste URLs
- **Send Button**: Submit for fact-checking
- **Hint**: Keyboard shortcuts displayed

---

## 🎨 Design Features

### Color Scheme
- **Primary**: Purple gradient (#667eea → #764ba2)
- **Success**: Green (#10b981)
- **Warning**: Yellow (#f59e0b)
- **Danger**: Red (#ef4444)

### Confidence Colors
- **High (70-100%)**: Green background
- **Medium (40-70%)**: Yellow background
- **Low (0-40%)**: Red background

### Animations
- **Slide In**: Messages appear smoothly
- **Pulse**: Status indicator animation
- **Bounce**: Loading dots animation
- **Hover Effects**: Interactive buttons

---

## 📱 Responsive Design

### Desktop (>768px)
- Full-width chat interface
- Side-by-side message layout
- Large input area

### Mobile (<768px)
- Optimized for small screens
- Full-height interface
- Touch-friendly buttons
- Adjusted message widths

---

## 🔧 Configuration

### API Endpoint

Edit `script.js` to change API URL:

```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### Polling Settings

Adjust polling behavior in `script.js`:

```javascript
const maxAttempts = 30; // 30 attempts
await sleep(3000); // 3 seconds between attempts
```

### File Upload Limits

Modify in `script.js`:

```javascript
if (file.size > 5 * 1024 * 1024) { // 5MB limit
    alert('File size must be less than 5MB');
    return;
}
```

---

## 🎭 User Flow

```
1. User opens chat interface
   ↓
2. Types claim / pastes URL / uploads image
   ↓
3. Clicks Send or presses Enter
   ↓
4. Message appears in chat
   ↓
5. Loading indicator shows
   ↓
6. "Processing..." message appears
   ↓
7. Frontend polls API every 3 seconds
   ↓
8. Result received (45-60 seconds)
   ↓
9. Result card displays with:
   - Confidence score
   - Claim text
   - Analysis
   - Download button
   ↓
10. User clicks "Download Report"
    ↓
11. PDF/HTML report downloads
```

---

## 🐛 Troubleshooting

### "Connection refused" Error

**Problem**: Cannot connect to API

**Solution**:
```bash
# Check if backend is running
curl http://localhost:8000/health

# Start backend if not running
python -m uvicorn app.main:app --reload
```

### Processing Timeout

**Problem**: "Processing timeout" message

**Solution**:
- Check if worker is running
- Increase `maxAttempts` in script.js
- Check backend logs for errors

### Image Upload Fails

**Problem**: Image not uploading

**Solution**:
- Check file size (<5MB)
- Verify file format (PNG, JPG, etc.)
- Check browser console for errors

### Report Download Fails

**Problem**: Cannot download report

**Solution**:
- Wait for processing to complete
- Check if report was generated
- Verify submission_id is correct

---

## 🎨 Customization

### Change Colors

Edit `style.css`:

```css
:root {
    --primary-color: #2563eb;  /* Change primary color */
    --user-msg-bg: #2563eb;    /* User message color */
    /* ... other colors ... */
}
```

### Change Gradient

Edit header gradient in `style.css`:

```css
.header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

### Add Custom Messages

Edit welcome message in `index.html`:

```html
<div class="message-text">
    <p>👋 Your custom welcome message</p>
    <!-- Add more content -->
</div>
```

---

## 📊 Performance

### Load Time
- **Initial Load**: <1 second
- **Message Render**: <100ms
- **API Call**: 45-60 seconds (backend processing)

### Browser Support
- ✅ Chrome 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Edge 90+

### Optimization
- Minimal dependencies (no frameworks)
- Vanilla JavaScript
- CSS animations (GPU accelerated)
- Efficient DOM manipulation

---

## 🔒 Security

### CORS
- Backend allows all origins (development)
- Configure properly for production

### Input Validation
- File type checking
- File size limits
- URL validation
- XSS prevention (escapeHtml)

### Production Recommendations
- Use HTTPS
- Restrict CORS origins
- Add rate limiting
- Implement authentication

---

## 📁 File Structure

```
frontend/
├── index.html          # Main HTML structure
├── style.css           # All styles and animations
├── script.js           # JavaScript logic
├── serve.py            # Python HTTP server
└── README.md          # This file
```

---

## 🚀 Deployment

### Static Hosting

Deploy to any static hosting service:

**Netlify**:
```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd frontend
netlify deploy --prod
```

**Vercel**:
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel --prod
```

**GitHub Pages**:
1. Push frontend folder to GitHub
2. Enable GitHub Pages
3. Select frontend folder as source

### Update API URL

For production, update `script.js`:

```javascript
const API_BASE_URL = 'https://your-api-domain.com';
```

---

## 🎯 Features Roadmap

### Planned
- [ ] Message history persistence
- [ ] Multiple conversations
- [ ] Export chat history
- [ ] Dark mode toggle
- [ ] Voice input
- [ ] Share results
- [ ] Bookmark claims
- [ ] User accounts

---

## 💡 Tips

### Keyboard Shortcuts
- **Enter**: Send message
- **Shift+Enter**: New line (not implemented yet)
- **Esc**: Clear input (not implemented yet)

### Best Practices
- Keep claims concise and clear
- Use full URLs (including https://)
- Upload clear, high-quality images
- Wait for processing to complete

### Example Claims
- "COVID vaccines contain microchips"
- "Government announces new policy"
- "Study shows coffee prevents cancer"
- "5G causes coronavirus"

---

## 🤝 Contributing

To improve the frontend:

1. Edit HTML structure in `index.html`
2. Modify styles in `style.css`
3. Update logic in `script.js`
4. Test in multiple browsers
5. Submit improvements

---

## 📞 Support

For issues:
- Check browser console for errors
- Verify backend is running
- Check network tab for API calls
- Review backend logs

---

**Version**: 1.0.0
**Last Updated**: November 20, 2025

---

**🎨 Beautiful interface for powerful fact-checking!**
