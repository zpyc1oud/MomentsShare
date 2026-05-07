# MomentsShare — Social Sharing Platform

A full-stack social sharing platform inspired by WeChat Moments, featuring AI-powered content assistance, real-time messaging, and a mobile-first glassmorphism UI.

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Django 4.2, Django REST Framework, SimpleJWT, Celery, PostgreSQL, Redis |
| **Frontend** | Vue 3 (Composition API), Vite, Pinia, Vant 4, SCSS |
| **Admin** | Vue 3, Element Plus, ECharts |
| **AI** | LangChain + SiliconFlow (OpenAI-compatible), Qwen VL models |
| **Infrastructure** | Docker Compose, FFmpeg, Nginx |

## Features

- **Social Feed** — Image posts (up to 9), video posts with async transcoding, tags, likes, comments, ratings
- **Friend System** — Send/accept/reject requests, bidirectional relationships, private messaging
- **AI Copilot** — Text polishing, smart tag recommendations, multimodal vision analysis (auto-switches to VL model for images)
- **Content Moderation** — DFA-based sensitive word filtering, admin approval workflows
- **Search** — Full-text search with Pinyin support
- **Admin Dashboard** — User management, content moderation, growth analytics with ECharts
- **Mobile-First Design** — iPhone 14 Pro simulator frame, macaron color palette, glassmorphism glass cards

## Architecture

```
MomentsShare/
├── backend/                 # Django REST API
│   ├── users/               # Auth, JWT, phone login
│   ├── moments/             # Posts, images, tags, video transcoding
│   ├── friends/             # Friend requests & relationships
│   ├── interactions/        # Comments, likes, ratings, messages
│   ├── ai_service/          # LangChain AI (polish + tags)
│   ├── admin_panel/         # Admin stats & moderation
│   └── core/                # Shared utils (DFA filter, exception handler)
├── frontend/                # Vue 3 mobile app
└── admin-dashboard/         # Vue 3 admin panel
```

## Quick Start

### Docker (Recommended)

```bash
cd backend
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py seed_data --skip-media
```

Services: Django `:8000` | PostgreSQL `:5432` | Redis `:6379`

### Local Development

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

# Separate terminal for async video processing
celery -A moments_share worker -l info
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev    # → http://localhost:3000
```

**Admin Dashboard:**
```bash
cd admin-dashboard
npm install
npm run dev
```

## Environment Variables

Create `backend/.env`:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=moments_share
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
AI_PROVIDER=openai
AI_API_KEY=your-siliconflow-api-key
AI_BASE_URL=https://api.siliconflow.cn/v1
AI_MODEL_NAME=Qwen/Qwen3-VL-8B-Instruct
```

## API Documentation

With the backend running:

| Endpoint | Description |
|----------|-------------|
| `/api/docs/` | Swagger UI |
| `/api/redoc/` | ReDoc |
| `/api/schema/` | OpenAPI schema |

### Key API Routes

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/users/register/` | Register (phone + password) |
| POST | `/api/users/login/` | Login → JWT tokens |
| GET | `/api/moments/feed/` | Friends' moments feed |
| POST | `/api/moments/` | Create moment |
| POST | `/api/moments/{id}/like/` | Toggle like |
| POST | `/api/friends/request/` | Send friend request |
| POST | `/api/ai/polish/` | AI text polishing |
| POST | `/api/ai/tags/` | AI tag recommendation |

## Test Accounts

Password for all: `Test123456`

| Username | Phone |
|----------|-------|
| alice | 13800000001 |
| bob | 13800000002 |
| charlie | 13800000003 |
| diana | 13800000004 |
| evan | 13800000005 |
| fiona | 13800000006 |
| george | 13800000007 |
| helen | 13800000008 |

Generate test data: `python manage.py seed_data --skip-media`

## Testing

```bash
cd backend
pytest              # Run all tests
pytest --cov        # With coverage report
pytest -v           # Verbose output
```

## Design System

- **Colors**: Sweet Pink `#FCAEC1` · Lavender `#B7A8D6` · Baby Blue `#ADD9F3`
- **Glass Effect**: `backdrop-filter: blur(20px)`, semi-transparent white
- **Layout**: iPhone 14 Pro frame (393×852px), mesh gradient backgrounds
- **Typography**: Noto Sans SC
- **CSS**: BEM naming convention

## Team

University software engineering course project — built by a team of 6 developers.

## License

MIT
