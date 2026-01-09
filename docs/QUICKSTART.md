# 🚀 Quick Start - VozPública

## ⚡ To Start NOW (3 steps)

### 1. Install frontend dependencies (first time only)
```bash
cd /workspaces/vozpublica/frontend
npm install
```

### 2. Start both services
```bash
cd /workspaces/vozpublica
./start-dev.sh
```

### 3. Open your browser
- Frontend: **http://localhost:3000**
- API Docs: **http://localhost:8000/docs**

## 🎯 Your First Test

1. Open http://localhost:3000
2. Click on "Explore Analysis"
3. Enter: "public security"
4. Press "Analyze"
5. Observe the results!

## 📖 More Information

- **Complete Testing Guide**: See [TESTING_GUIDE.md](TESTING_GUIDE.md)
- **System Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)

## 🔧 Useful Commands

### Stop the services
```bash
# Press Ctrl+C in the terminal where you ran start-dev.sh
```

### Restart only the frontend
```bash
cd /workspaces/vozpublica/frontend
npm run dev
```

### Restart only the backend
```bash
cd /workspaces/vozpublica
uvicorn backend.app.main:app --reload
```

### View logs in real time
Logs appear automatically in the terminals where services are running.

## 🆘 Problems?

### Port busy
```bash
# Free port 3000 (frontend)
lsof -ti:3000 | xargs kill -9

# Free port 8000 (backend)
lsof -ti:8000 | xargs kill -9
```

### Cannot connect to backend
1. Verify the backend is running:
   ```bash
   curl http://localhost:8000/health
   ```
2. You should see: `{"status":"ok"}`

## 📚 Learning Resources

- [Next.js Tutorial](https://nextjs.org/learn)
- [React Docs](https://react.dev/learn)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
