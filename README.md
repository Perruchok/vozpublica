# 🗣️ VozPública

**AI-powered political discourse analysis platform** for analyzing semantic evolution and narrative changes in presidential communications.

## 🎯 Why VozPública?

Political discourse shapes public policy, yet its evolution over time is rarely analyzed systematically.
VozPública provides quantitative and qualitative tools to trace how narratives, priorities, and meanings
shift across presidential communications—grounded in primary sources and semantic analysis.

---

## ✨ Features

- 🔄 **Automatic Data Ingestion** - Automated scraping and processing of presidential discourse
- 🔍 **Semantic Search** - Vector-based search over presidential discourse using embeddings
- 💬 **Question Answering** - LLM-powered Q&A with source attribution
- 📊 **Narrative Evolution** - Track how political concepts change over time
- 🎯 **Semantic Drift Detection** - Identify and explain shifts in discourse meaning
- 🌐 **Bilingual Interface** - Full ES/EN support without external i18n dependencies
- 📈 **Analytics Dashboard** - Interactive visualizations of discourse patterns

---


## 🚀 Quick Start

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-336791?logo=postgresql)](https://github.com/pgvector/pgvector)


### Prerequisites

- **Python 3.12+**
- **Node.js 18+** and npm
- **PostgreSQL** with pgvector extension
- **Azure OpenAI** account (or OpenAI API key)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Perruchok/vozpublica.git
   cd vozpublica
   ```

2. **Install backend dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # Database
   PGHOST=your-postgres-host
   PGDATABASE=your-database-name
   PGUSER=your-username
   PGPASSWORD=your-password
   PGPORT=5432

   # Azure OpenAI
   AZURE_OPENAI_API_KEY=your-api-key
   AZURE_OPENAI_ENDPOINT=your-endpoint
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
   AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4

   # Frontend
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

5. **Start the application**
   ```bash
   ./start-dev.sh
   ```

6. **Access the application**
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs
   - Health Check: http://localhost:8000/health

📖 **Detailed setup guide**: See [docs/QUICKSTART.md](docs/QUICKSTART.md)

---

## 🏗️ Architecture

### Tech Stack

**Frontend**
- **Next.js 14** - React framework with App Router
- **React 18** - UI library with hooks
- **Custom i18n** - Lightweight bilingual support via React Context

**Backend**
- **FastAPI** - Modern async Python web framework
- **Pydantic v2** - Data validation and settings
- **asyncpg** - Async PostgreSQL driver with connection pooling
- **Playwright** - Web scraping for data ingestion

**Database & AI**
- **PostgreSQL + pgvector** - Vector similarity search
- **Azure OpenAI** - text-embedding-3-small, gpt-4
- **HNSW indexing** - Fast approximate nearest neighbor search

**Deployment**
- **Docker** - Multi-stage builds with non-root user
- **Azure App Service** - Backend hosting
- **Vercel** - Frontend hosting (optional)

### System Overview

```
┌─────────────┐      HTTP/REST      ┌──────────────┐
│   Next.js   │ ◄─────────────────► │   FastAPI    │
│  Frontend   │      JSON/CORS      │   Backend    │
│  (Port 3000)│                     │  (Port 8000) │
└─────────────┘                     └───────┬──────┘
                                            │
                                            ▼
                                  ┌─────────────────┐
                                  │   PostgreSQL    │
                                  │   + pgvector    │
                                  │   (Port 5432)   │
                                  └─────────────────┘
```

📖 **Detailed architecture**: See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 📁 Repository Structure

```
vozpublica/
├── backend/                 # FastAPI application
│   ├── app/
│   │   ├── api/            # API endpoints (routers)
│   │   ├── models/         # Pydantic models
│   │   └── services/       # Business logic
│   ├── analytics/          # Semantic drift & narrative analysis
│   ├── ingestion/          # Web scraping scripts
│   ├── utils/              # Database pool, logging, helpers
│   └── settings.py         # Configuration management
├── frontend/               # Next.js application
│   ├── app/               # Pages (App Router)
│   ├── components/        # React components
│   ├── lib/               # API client & translations
│   └── styles/            # Global CSS
├── docs/                  # Documentation
│   ├── ARCHITECTURE.md    # System architecture
│   ├── DEPLOYMENT_READINESS.md
│   ├── QUICKSTART.md      # Getting started guide
│   ├── TESTING_GUIDE.md   # Testing instructions
│   └── BILINGUAL_SUPPORT.md
├── dev/                   # Development tools
│   ├── notebooks/         # Jupyter notebooks for analysis
│   ├── samples/           # Test data
│   └── scripts/           # Utility scripts
├── Dockerfile             # Production Docker image
├── Makefile              # Common tasks (scrape, test, etc.)
├── requirements.txt       # Python dependencies
└── start-dev.sh          # Development server launcher
```

---

## 🧪 Testing

```bash
# Run backend tests
pytest backend/tests/

# Run frontend in development mode
cd frontend && npm run dev

# Test API endpoints
curl http://localhost:8000/health
```

📖 **Complete testing guide**: See [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)

---

## 🚢 Deployment

### Docker Build

```bash
docker build -t vozpublica-backend .
docker run -p 8000:8000 vozpublica-backend
```

### Azure Deployment

```bash
# Configure Azure resources
./setup-azure.sh

# Pre-deployment checks
./precheck-deployment.sh
```

📖 **Deployment guide**: See [docs/DEPLOYMENT_READINESS.md](docs/DEPLOYMENT_READINESS.md)

---

## 🌐 Bilingual Support

VozPública supports both Spanish and English without external i18n libraries. The implementation uses:

- React Context for language state management
- Custom translation objects in `frontend/lib/translations.js`
- Language toggle component in navigation

📖 **Implementation details**: See [docs/BILINGUAL_SUPPORT.md](docs/BILINGUAL_SUPPORT.md)

---

## 🤝 Contributing

Contributions are welcome! **Please reach out first** before starting work:

1. **Open an issue** or comment on an existing one to discuss your proposed changes
2. **Wait for feedback** - I'd like to chat about implementation approach and scope
3. Once we've aligned on the approach:
   - Fork the repository
   - Create a feature branch (`git checkout -b feature/amazing-feature`)
   - Make your changes
   - Run tests (`pytest` for backend, `npm run dev` for frontend)
   - Commit your changes (`git commit -m 'Add amazing feature'`)
   - Push to the branch (`git push origin feature/amazing-feature`)
   - Open a Pull Request

### Why reach out first?

- Ensures your work aligns with project direction
- Avoids duplicate efforts
- Helps scope features appropriately
- Facilitates better collaboration

### Development Guidelines

- Follow existing code style and structure
- Add tests for new features
- Update documentation as needed
- Keep commits focused and descriptive

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/Perruchok/vozpublica/issues)
- **Repository**: [github.com/Perruchok/vozpublica](https://github.com/Perruchok/vozpublica)

---

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend powered by [Next.js](https://nextjs.org/)
- Vector search via [pgvector](https://github.com/pgvector/pgvector)
- AI capabilities from [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service)

---

**Made with ❤️ for transparent political discourse analysis**
