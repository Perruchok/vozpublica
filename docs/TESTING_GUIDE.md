# 🧪 Testing Guide - Frontend VozPública

## Initial Setup

### 1. Install frontend dependencies (if you haven't already)
```bash
cd /workspaces/vozpublica/frontend
npm install
```

### 2. Start the services

**Option A: Automatic script (recommended)**
```bash
cd /workspaces/vozpublica
./start-dev.sh
```

**Option B: Manual in separate terminals**

Terminal 1 - Backend:
```bash
cd /workspaces/vozpublica
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2 - Frontend:
```bash
cd /workspaces/vozpublica/frontend
npm run dev
```

## 🔗 Test URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## ✅ Testing Checklist

### Level 1: Basic Tests

- [ ] **Main page loads correctly**
  - Open http://localhost:3000
  - You should see "VozPública" as the title
  - Verify there are 3 feature cards

- [ ] **Backend responds**
  - Open http://localhost:8000/health
  - You should see: `{"status": "ok"}`

- [ ] **API documentation accessible**
  - Open http://localhost:8000/docs
  - You should see the Swagger UI interface

### Level 2: Navigation

- [ ] **Navigate to Narrative Analysis**
  - On the main page, click "Explore Analysis"
  - You should go to the `/narrative` page

- [ ] **CSS styles load correctly**
  - Verify that colors and designs look good
  - No style errors in browser console

### Level 3: Frontend-Backend Integration

- [ ] **API test from the frontend**
  
  On the `/narrative` page, you should be able to:
  1. Enter a concept (e.g., "public security")
  2. Select dates
  3. See semantic evolution charts
  4. See AI-generated explanations

### Level 4: Development Tools

- [ ] **Browser console**
  - Open DevTools (F12)
  - Go to the Console tab
  - You should not see red errors (yellow warnings are OK)

- [ ] **Network tab**
  - Open DevTools → Network
  - Perform a search
  - Verify that calls to `http://localhost:8000/api/*` have status 200

- [ ] **React DevTools** (optional)
  - Install the React DevTools extension
  - Inspect components and their state

## 🐛 Debugging: Common Issues

### Frontend does not load

```bash
# Verify Node.js is installed
node --version

# Reinstall dependencies
cd /workspaces/vozpublica/frontend
rm -rf node_modules package-lock.json
npm install
```

### CORS error

If you see errors like "blocked by CORS policy":
- Verify the backend is running on port 8000
- The backend already has CORS configured for localhost:3000

### Error: Cannot connect to backend

1. Verify the backend is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Verify API_BASE_URL configuration:
   - It's in `frontend/lib/constants.js`
   - Should be: `http://localhost:8000`

### Port is busy

```bash
# For backend (port 8000)
lsof -ti:8000 | xargs kill -9

# For frontend (port 3000)
lsof -ti:3000 | xargs kill -9
```

## 🔍 API Tests with cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Semantic Evolution
```bash
curl -X POST http://localhost:8000/api/semantic-evolution \
  -H "Content-Type: application/json" \
  -d '{
    "concept": "seguridad pública",
    "granularity": "month",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "similarity_threshold": 0.6
  }'
```

### Explain Drift
```bash
curl -X POST http://localhost:8000/api/explain-drift \
  -H "Content-Type: application/json" \
  -d '{
    "concept": "seguridad pública",
    "from_period": "2024-01-01",
    "to_period": "2024-06-01",
    "similarity_threshold": 0.6
  }'
```

## 📊 Real-Time Monitoring

### Backend Logs
```bash
# Logs appear automatically in the terminal where you ran uvicorn
# Look for lines like:
# INFO:     127.0.0.1:xxxxx - "POST /api/semantic-evolution HTTP/1.1" 200 OK
```

### Frontend Logs
```bash
# Next.js shows logs in its terminal
# Look for lines like:
# ○ Compiling /narrative ...
# ✓ Compiled successfully
```

### Browser Console
```javascript
// In the browser console, you can test manually:
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(console.log)
```

## 🎯 Recommended Tests for Learning

### 1. Modify a component
- Edit `frontend/app/page.jsx`
- Change the tagline text
- Save the file
- The browser should reload automatically (Hot Reload)

### 2. View data flow
- Open DevTools → Network
- On `/narrative`, perform a search
- Observe the POST call to `/api/semantic-evolution`
- Inspect the Request and Response

### 3. Add a console.log
In `frontend/lib/api.js`, add:
```javascript
export async function fetchSemanticEvolution(params) {
  console.log('📤 Sending request:', params);
  const result = await fetchAPI('/api/semantic-evolution', {
    method: 'POST',
    body: JSON.stringify({...}),
  });
  console.log('📥 Response received:', result);
  return result;
}
```

## 📚 Learning Resources

- **Next.js Docs**: https://nextjs.org/docs
- **React Docs**: https://react.dev
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Fetch API**: https://developer.mozilla.org/en/docs/Web/API/Fetch_API

## 🎓 Suggested Exercises

1. **Add a new button** on the main page
2. **Create a new component** in `frontend/components/common/`
3. **Add a new field** to the search form
4. **Change the colors** in `frontend/styles/globals.css`
5. **Add validation** to form inputs
