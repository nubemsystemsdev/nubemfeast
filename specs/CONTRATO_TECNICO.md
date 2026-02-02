# Contrato Técnico - NubemFeast

> Sistema de Accesibilidad para Sillas de Ruedas
> Versión: 1.0.0
> Fecha: 2026-02-02

---

## 1. Descripción del Proyecto

**NubemFeast** es un POC que analiza fotos 2D de espacios (museos, edificios) y genera guías de navegación visual para personas en silla de ruedas, con interfaz tipo "recorrido virtual".

### 1.1 Funcionalidades Principales

1. **Subir fotos de recorrido**: Permite cargar múltiples imágenes de un espacio
2. **Análisis con Vision AI**: Detecta barreras de accesibilidad (puertas estrechas, escalones, obstáculos)
3. **Modelo de mundo**: Crea grafo de espacios conectados usando NetworkX
4. **Guía personalizada**: Genera recomendaciones según perfil de silla de ruedas
5. **Recorrido virtual**: Presenta navegación interactiva con alertas visuales

---

## 2. Stack Tecnológico

### 2.1 Backend

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Lenguaje | Python | 3.11 |
| Framework | FastAPI | 0.109.0 |
| ORM | SQLModel | 0.0.14 |
| Validación | Pydantic | v2 |
| Server | Uvicorn | 0.27.0 |

### 2.2 Base de Datos

| Entorno | Motor | Justificación |
|---------|-------|---------------|
| Desarrollo | SQLite | Desarrollo rápido, sin config |
| Producción | PostgreSQL | Escalabilidad, concurrencia |

**Migraciones**: Alembic
**Convención naming**: snake_case, tablas en plural

### 2.3 Frontend

| Componente | Tecnología | Versión |
|------------|------------|---------|
| Framework | React | 18.2.0 |
| Build Tool | Vite | 5.0.0 |
| State | TanStack Query | 5.17.0 |
| Styling | Tailwind CSS | 3.4.0 |
| HTTP Client | Axios | 1.6.0 |
| Animaciones | Framer Motion | 11.0.0 |
| Lenguaje | TypeScript | 5.3.0 |

### 2.4 Infraestructura

| Componente | Servicio |
|------------|----------|
| Cloud Provider | Google Cloud |
| Compute | Cloud Run |
| Registry | Artifact Registry |
| CI/CD | GitHub Actions |

### 2.5 Servicios Externos

| Servicio | Proveedor | Uso |
|----------|-----------|-----|
| Vision AI | OpenAI GPT-4o Vision | Análisis de imágenes |
| Backup Vision | Google Gemini 1.5 Pro | Alternativa menor costo |

---

## 3. Arquitectura

### 3.1 Patrón Arquitectónico

**Arquitectura en Capas + Repository Pattern**

```
┌─────────────────────────────────────────┐
│              API Layer                   │
│         (FastAPI Routers)               │
├─────────────────────────────────────────┤
│            Service Layer                 │
│    (Lógica de negocio, Vision AI)       │
├─────────────────────────────────────────┤
│          Repository Layer                │
│      (Abstracción acceso a datos)       │
├─────────────────────────────────────────┤
│             Data Layer                   │
│    (SQLModel + SQLite/PostgreSQL)       │
└─────────────────────────────────────────┘
```

### 3.2 Flujo de Datos Principal

```
1. Usuario sube imágenes → POST /api/scans
2. Backend almacena imágenes → Upload Service
3. Análisis Vision AI → Vision Service (GPT-4o)
4. Construcción modelo mundo → World Model Service (NetworkX)
5. Generación guía → Guide Service
6. Presentación recorrido → Frontend Virtual Tour
```

---

## 4. Endpoints API

### 4.1 Scans

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/scans` | Crear nuevo scan |
| GET | `/api/scans` | Listar scans |
| GET | `/api/scans/{id}` | Obtener scan |
| DELETE | `/api/scans/{id}` | Eliminar scan |
| POST | `/api/scans/{id}/images` | Subir imágenes |

### 4.2 Analysis

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/scans/{id}/analyze` | Iniciar análisis |
| GET | `/api/scans/{id}/analysis` | Obtener resultado análisis |

### 4.3 Navigation

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/scans/{id}/guide` | Obtener guía navegación |
| GET | `/api/scans/{id}/world-model` | Obtener modelo de mundo |

---

## 5. Modelos de Datos

Ver `DATA_MODELS.md` para especificación completa.

### 5.1 Entidades Principales

- **Scan**: Representa un escaneo/recorrido de un espacio
- **Image**: Imagen individual dentro de un scan
- **AnalysisResult**: Resultado del análisis de accesibilidad
- **Barrier**: Barrera de accesibilidad detectada
- **Guide**: Guía de navegación generada
- **WheelchairProfile**: Perfil de silla de ruedas del usuario

---

## 6. Constraints

| Constraint | Valor | Razón |
|------------|-------|-------|
| Presupuesto cloud | ~$50/mes | POC con recursos limitados |
| Vision API calls | ~100/día | Costo de GPT-4V |
| Max imágenes/scan | 20 | Limitar procesamiento |
| Tamaño max imagen | 10MB | Performance upload |
| Formatos imagen | JPEG, PNG, WebP | Compatibilidad Vision AI |

---

## 7. Testing

| Aspecto | Especificación |
|---------|----------------|
| Framework backend | pytest + pytest-asyncio |
| Framework frontend | vitest + testing-library |
| Cobertura mínima | 80% |
| CI blocking | Tests deben pasar para merge |

### 7.1 Tests Requeridos

- **Unitarios**: vision_service, world_model_service, guide_service
- **Integración**: Endpoints de API
- **E2E**: Flujo completo upload → análisis → guía

---

## 8. Variables de Entorno

```bash
# Backend
DATABASE_URL=sqlite+aiosqlite:///./data/nubemfeast.db
OPENAI_API_KEY=sk-...
UPLOAD_DIR=./data/uploads
MAX_UPLOAD_SIZE_MB=10
API_PORT=8002

# Frontend
VITE_API_URL=http://localhost:8002

# GCP (deployment)
GCP_PROJECT_ID=nubemfeast
GCP_REGION=europe-west1
ARTIFACT_REGISTRY_REPO=nubemfeast
```

---

## 9. Convenciones de Código

### 9.1 Backend (Python)

- **Formatter**: Black (line-length: 88)
- **Linter**: Ruff
- **Type checker**: mypy (strict mode)
- **Docstrings**: Google style
- **Imports**: isort compatible con Black

### 9.2 Frontend (TypeScript)

- **Formatter**: Prettier
- **Linter**: ESLint con config React
- **Naming**:
  - Componentes: PascalCase
  - Funciones/variables: camelCase
  - Constantes: UPPER_SNAKE_CASE
  - Archivos componentes: PascalCase.tsx

---

## 10. Git Workflow

### 10.1 Ramas

- `main`: Producción (protegida)
- `staging`: Pre-producción (default, protegida)
- `feature/*`: Nuevas funcionalidades
- `fix/*`: Corrección de bugs
- `hotfix/*`: Fixes urgentes en producción

### 10.2 Commits

Formato: `<type>(<scope>): <description>`

Tipos: feat, fix, docs, style, refactor, test, chore

---

## 11. Deployment

### 11.1 Entornos

| Entorno | URL | Trigger |
|---------|-----|---------|
| Staging | staging.nubemfeast.app | Push a staging |
| Production | nubemfeast.app | Push a main |

### 11.2 CI/CD Pipeline

1. **ci.yml**: Lint, tests, spec-verify en PRs
2. **deploy-staging.yml**: Build + deploy a Cloud Run staging
3. **deploy-production.yml**: Build + deploy a Cloud Run producción

---

## Historial de Cambios

| Fecha | Versión | Descripción |
|-------|---------|-------------|
| 2026-02-02 | 1.0.0 | Versión inicial del contrato |
