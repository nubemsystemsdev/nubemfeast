# NubemFeast

Sistema de Accesibilidad para Sillas de Ruedas

## Descripcion

NubemFeast es un POC que analiza fotos 2D de espacios (museos, edificios) y genera guias de navegacion visual para personas en silla de ruedas, con interfaz tipo "recorrido virtual".

### Funcionalidades Principales

- **Subir fotos de recorrido**: Carga multiples imagenes de un espacio
- **Analisis con Vision AI**: Detecta barreras de accesibilidad (puertas estrechas, escalones, obstaculos)
- **Modelo de mundo**: Crea grafo de espacios conectados usando NetworkX
- **Guia personalizada**: Genera recomendaciones segun perfil de silla de ruedas
- **Recorrido virtual**: Presenta navegacion interactiva con alertas visuales

## Stack Tecnologico

### Backend
- Python 3.11
- FastAPI
- SQLModel (SQLAlchemy + Pydantic)
- OpenAI GPT-4o Vision
- NetworkX

### Frontend
- React 18 + TypeScript
- Vite
- TanStack Query
- Tailwind CSS
- Framer Motion

### Infraestructura
- Google Cloud Run
- SQLite (desarrollo) / PostgreSQL (produccion)
- GitHub Actions (CI/CD)

## Inicio Rapido

### Requisitos

- Python 3.11+
- Node.js 20+
- Docker (opcional)

### Desarrollo Local

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/nubemsystems/nubemfeast.git
   cd nubemfeast
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   # Editar .env con tu OPENAI_API_KEY
   ```

3. **Backend**
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn src.main:app --reload --port 8002
   ```

4. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Acceder a la aplicacion**
   - Frontend: http://localhost:5173
   - API: http://localhost:8002
   - Docs: http://localhost:8002/docs

> **Nota sobre puertos**: El backend usa el puerto 8002 por defecto (en lugar de 8000) para evitar conflictos con otras aplicaciones. Puedes cambiarlo con la variable de entorno `API_PORT`.

### Usando Docker

```bash
# Desarrollo
docker-compose up backend frontend

# O con hot-reload para backend
docker-compose --profile dev up backend-dev frontend
```

## Estructura del Proyecto

```
nubemfeast/
├── specs/                    # Documentacion tecnica
│   ├── CONTRATO_TECNICO.md
│   ├── DATA_MODELS.md
│   ├── ARCHITECTURE_DECISIONS.md
│   └── api_contracts/
├── backend/
│   ├── src/
│   │   ├── api/              # Endpoints FastAPI
│   │   ├── core/             # Configuracion
│   │   ├── models/           # SQLModel
│   │   ├── schemas/          # Pydantic
│   │   ├── services/         # Logica de negocio
│   │   └── repositories/     # Acceso a datos
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   ├── pages/            # Paginas
│   │   ├── hooks/            # Custom hooks
│   │   ├── services/         # API client
│   │   └── types/            # TypeScript types
│   └── tests/
├── .github/workflows/        # CI/CD
└── docker-compose.yml
```

## API

### Endpoints Principales

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| POST | `/api/scans` | Crear nuevo scan |
| POST | `/api/scans/{id}/images` | Subir imagenes |
| POST | `/api/scans/{id}/analyze` | Iniciar analisis |
| GET | `/api/scans/{id}/guide` | Obtener guia de navegacion |
| GET | `/api/scans/{id}/world-model` | Obtener modelo de mundo |

Ver documentacion completa en `/docs` cuando el servidor esta corriendo.

## Testing

```bash
# Backend
cd backend
pytest --cov=src

# Frontend
cd frontend
npm run test
```

## Deployment

El proyecto usa GitHub Actions para CI/CD:

- **CI**: Lint, tests, build en cada PR
- **Staging**: Deploy automatico a Cloud Run en push a `staging`
- **Production**: Deploy automatico a Cloud Run en push a `main`

### Variables de Entorno (Secrets)

Configurar en GitHub Secrets:
- `GCP_PROJECT_ID`
- `GCP_WORKLOAD_IDENTITY_PROVIDER`
- `GCP_SERVICE_ACCOUNT`

Configurar en GCP Secret Manager:
- `openai-api-key`
- `database-url-staging`
- `database-url-production`

## Contribuir

1. Crear rama desde `staging`: `git checkout -b feature/mi-feature`
2. Hacer cambios y commits
3. Crear PR hacia `staging`
4. Tras aprobacion y merge, se despliega a staging
5. PR de `staging` a `main` para produccion

## Licencia

MIT

## Contacto

NubemSystems - dev@nubemsystems.com
