# Contrato Técnico - NubemFeast

> **IMPORTANTE**: Este documento es la FUENTE DE VERDAD para todos los agentes.
> Cualquier decisión técnica que contradiga este documento debe generar un SPEC_UPDATE_REQUEST.
> No se permite código que viole las convenciones aquí definidas.

---

## Sistema de Documentación Dual: CLAUDE.md + CONTRATO_TECNICO.md

Este proyecto utiliza dos archivos complementarios que trabajan juntos para guiar el desarrollo:

### Propósito de Cada Archivo

| Archivo | Propósito | Contenido | Audiencia |
|---------|-----------|-----------|-----------|
| **CLAUDE.md** | Instrucciones operativas para Claude Code | Cómo trabajar, comandos, workflows, reglas de sesión | Claude Code CLI |
| **CONTRATO_TECNICO.md** | Especificaciones técnicas del proyecto | Arquitectura, stack, decisiones, convenciones | Agentes y humanos |

### Jerarquía de Precedencia

```
1. Instrucciones explícitas del usuario en el chat (MÁXIMA)
2. CLAUDE.md del proyecto (instrucciones operativas)
3. CONTRATO_TECNICO.md (especificaciones técnicas)
4. Convenciones deducidas del código (MÍNIMA)
```

---

## Metadata

| Campo | Valor |
|-------|-------|
| **Nombre del proyecto** | NubemFeast |
| **Descripción** | Sistema de Accesibilidad para Sillas de Ruedas |
| **Versión del contrato** | 1.0.0 |
| **Fecha de creación** | 2026-02-02 |
| **Última actualización** | 2026-02-02 |
| **Actualizado por** | architect-agent |

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

| Aspecto | Decisión | Versión | Justificación |
|---------|----------|---------|---------------|
| **Lenguaje** | Python | 3.11 | Ecosistema maduro para AI/ML, integración nativa con OpenAI |
| **Framework** | FastAPI | 0.109.0 | Async nativo, validación con Pydantic, OpenAPI automático |
| **ORM** | SQLModel | 0.0.14 | Combina SQLAlchemy + Pydantic, reduce boilerplate |
| **Validación** | Pydantic | v2 | Performance mejorada, integrado con FastAPI |
| **Server** | Uvicorn | 0.27.0 | ASGI server de alto rendimiento |

### 2.2 Base de Datos

| Aspecto | Decisión | Justificación |
|---------|----------|---------------|
| **Motor (Desarrollo)** | SQLite | Desarrollo rápido, sin configuración |
| **Motor (Producción)** | PostgreSQL | Escalabilidad, concurrencia |
| **Migraciones** | Alembic | Estándar para SQLAlchemy/SQLModel |
| **Naming convention** | snake_case, tablas en plural | Convención Python estándar |

### 2.3 Frontend

| Aspecto | Decisión | Versión | Justificación |
|---------|----------|---------|---------------|
| **Framework** | React | 18.2.0 | Fast refresh, ecosistema maduro |
| **Build Tool** | Vite | 5.0.0 | Build optimizado, TypeScript nativo |
| **State** | TanStack Query | 5.17.0 | Cache de API, sincronización servidor-cliente |
| **Styling** | Tailwind CSS | 3.4.0 | Utility-first, rápido para prototipar |
| **HTTP Client** | Axios | 1.6.0 | Interceptors, manejo de errores consistente |
| **Animaciones** | Framer Motion | 11.0.0 | Transiciones suaves para recorrido virtual |
| **Lenguaje** | TypeScript | 5.3.0 | Type safety |

### 2.4 Infraestructura

| Aspecto | Decisión | Justificación |
|---------|----------|---------------|
| **Cloud Provider** | Google Cloud | Infraestructura existente nubemsystems |
| **Compute** | Cloud Run | Escalado automático, pay-per-use |
| **Registry** | Artifact Registry | Integración nativa GCP |
| **CI/CD** | GitHub Actions | Estándar de la metodología |

### 2.5 Servicios Externos

| Servicio | Proveedor | Uso |
|----------|-----------|-----|
| Vision AI | OpenAI GPT-4o Vision | Análisis de imágenes |
| Backup Vision | Google Gemini 1.5 Pro | Alternativa menor costo |

---

## 3. Dependencias Principales

### Backend

```
# Framework web
fastapi==0.109.0 - Framework web async
uvicorn[standard]==0.27.0 - ASGI server
python-multipart==0.0.6 - File uploads

# AI/Vision
openai==1.12.0 - GPT-4 Vision integration

# Base de datos
sqlmodel==0.0.14 - ORM (SQLAlchemy + Pydantic)
aiosqlite==0.19.0 - SQLite async (POC)
alembic==1.13.1 - Migraciones

# Modelo de mundo
networkx==3.2.1 - Grafos para representar espacios

# Imágenes
Pillow==10.2.0 - Procesamiento de imágenes

# Utilidades
pydantic-settings==2.1.0 - Configuración
python-dotenv==1.0.0 - Variables de entorno
httpx==0.26.0 - HTTP client async
aiofiles==23.2.1 - File I/O async

# Testing
pytest==8.0.0
pytest-asyncio==0.23.0
pytest-cov==4.1.0

# Code quality
black==24.1.0 - Formatter
ruff==0.2.0 - Linter
mypy==1.8.0 - Type checking
```

### Frontend

```
# Core
react@18.2.0 - UI framework
react-dom@18.2.0 - React DOM
react-router-dom@6.22.0 - Routing

# Data fetching
@tanstack/react-query@5.17.0 - Server state management
axios@1.6.0 - HTTP client

# UI
tailwindcss@3.4.0 - Styling
framer-motion@11.0.0 - Animaciones
lucide-react@0.300.0 - Iconos

# Utilities
clsx@2.1.0 - Class names
tailwind-merge@2.2.0 - Merge Tailwind classes

# Dev
vite@5.0.0 - Build tool
typescript@5.3.0 - Type safety
@types/react@18.2.0 - React types
vitest@1.2.0 - Testing
@testing-library/react@14.1.0 - React testing
```

---

## 4. Arquitectura

### 4.1 Patrón Arquitectónico

**Patrón:** Arquitectura en Capas + Repository Pattern

**Justificación:**
Para un POC, una arquitectura en capas proporciona separación clara de responsabilidades sin la complejidad de DDD o Hexagonal. El Repository Pattern permite abstraer el acceso a datos y facilitar testing. Esta arquitectura es suficientemente simple para iterar rápido pero estructurada para escalar si el POC tiene éxito.

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

### 4.2 Estructura de Carpetas

```
nubemfeast/
│
├── /docs                               # DOCUMENTACIÓN Y ESPECIFICACIONES
│   ├── CONTRATO_TECNICO.md             # Fuente de verdad técnica
│   ├── DATA_MODELS.md                  # Especificación de entidades
│   ├── ARCHITECTURE_DECISIONS.md       # Log de decisiones arquitectónicas
│   ├── TASK_HISTORY.md                 # Historial de tareas
│   ├── historico_commits.md            # Historial detallado de commits
│   ├── /api_contracts                  # Contratos OpenAPI
│   │   ├── scans.yaml
│   │   ├── analysis.yaml
│   │   └── navigation.yaml
│   ├── /agents                         # Documentación de agentes
│   └── /prompts                        # Prompts de metodología
│
├── /backend
│   ├── /src
│   │   ├── /api                        # Endpoints FastAPI (routers)
│   │   │   ├── __init__.py
│   │   │   ├── scans.py
│   │   │   ├── analysis.py
│   │   │   └── navigation.py
│   │   │
│   │   ├── /core                       # Configuración, dependencias
│   │   │   ├── __init__.py
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── dependencies.py
│   │   │
│   │   ├── /models                     # Modelos SQLModel
│   │   │   ├── __init__.py
│   │   │   ├── scan.py
│   │   │   ├── image.py
│   │   │   └── guide.py
│   │   │
│   │   ├── /schemas                    # Schemas Pydantic (request/response)
│   │   │   ├── __init__.py
│   │   │   ├── scan.py
│   │   │   ├── analysis.py
│   │   │   ├── navigation.py
│   │   │   └── enums.py
│   │   │
│   │   ├── /services                   # Lógica de negocio
│   │   │   ├── __init__.py
│   │   │   ├── scan_service.py
│   │   │   ├── vision_service.py       # Integración Vision AI
│   │   │   ├── world_model_service.py  # Grafo NetworkX
│   │   │   └── guide_service.py
│   │   │
│   │   ├── /repositories               # Acceso a datos
│   │   │   ├── __init__.py
│   │   │   ├── scan_repository.py
│   │   │   └── image_repository.py
│   │   │
│   │   └── main.py
│   │
│   ├── /tests
│   │   ├── /unit
│   │   └── /integration
│   │
│   ├── /alembic
│   ├── requirements.txt
│   ├── pyproject.toml
│   └── Dockerfile
│
├── /frontend
│   ├── /src
│   │   ├── /components
│   │   │   ├── /Layout
│   │   │   ├── /VirtualTour            # Componente principal recorrido
│   │   │   ├── /Upload
│   │   │   ├── /Accessibility
│   │   │   └── /Summary
│   │   │
│   │   ├── /pages
│   │   ├── /hooks
│   │   ├── /services
│   │   ├── /store
│   │   ├── /types
│   │   └── /utils
│   │
│   ├── /tests
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── /.github
│   └── /workflows
│       ├── ci.yml
│       ├── deploy-staging.yml
│       └── deploy-production.yml
│
├── docker-compose.yml
├── CLAUDE.md
├── .env.example
└── README.md
```

### 4.3 Flujo de Datos Principal

```
1. Usuario sube imágenes → POST /api/scans
2. Backend almacena imágenes → Upload Service
3. Análisis Vision AI → Vision Service (GPT-4o)
4. Construcción modelo mundo → World Model Service (NetworkX)
5. Generación guía → Guide Service
6. Presentación recorrido → Frontend Virtual Tour
```

### 4.4 Patrones Obligatorios

| Patrón | Dónde Aplicar | Ejemplo |
|--------|---------------|---------|
| Dependency Injection | Servicios en endpoints | `Depends(get_db)` |
| Repository Pattern | Acceso a datos | `ScanRepository.get_by_id()` |
| DTO/Schema separation | API boundaries | Pydantic schemas separados de models |

### 4.5 Patrones Prohibidos

| Patrón | Razón |
|--------|-------|
| God classes | Viola Single Responsibility |
| Hardcoded configuration | Dificulta deployment |
| Direct SQL in controllers | Viola separación de capas |

---

## 5. Endpoints API

### 5.1 Scans

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/scans` | Crear nuevo scan |
| GET | `/api/scans` | Listar scans |
| GET | `/api/scans/{id}` | Obtener scan |
| DELETE | `/api/scans/{id}` | Eliminar scan |
| POST | `/api/scans/{id}/images` | Subir imágenes |

### 5.2 Analysis

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/scans/{id}/analyze` | Iniciar análisis |
| GET | `/api/scans/{id}/analysis` | Obtener resultado análisis |

### 5.3 Navigation

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/scans/{id}/guide` | Obtener guía navegación |
| GET | `/api/scans/{id}/world-model` | Obtener modelo de mundo |

---

## 6. Modelos de Datos

Ver `docs/DATA_MODELS.md` para especificación completa.

### 6.1 Entidades Principales

- **Scan**: Representa un escaneo/recorrido de un espacio
- **Image**: Imagen individual dentro de un scan
- **AnalysisResult**: Resultado del análisis de accesibilidad
- **Barrier**: Barrera de accesibilidad detectada
- **Guide**: Guía de navegación generada
- **WheelchairProfile**: Perfil de silla de ruedas del usuario

---

## 7. Convenciones de Código

### 7.1 Backend (Python)

| Aspecto | Convención |
|---------|------------|
| **Formatter** | Black (line-length: 88) |
| **Linter** | Ruff |
| **Type checker** | mypy (strict mode) |
| **Naming: funciones/variables** | snake_case |
| **Naming: clases** | PascalCase |
| **Naming: constantes** | UPPER_SNAKE_CASE |
| **Docstrings** | Google style |
| **Type hints** | Obligatorios en funciones públicas |

### 7.2 Frontend (TypeScript)

| Aspecto | Convención |
|---------|------------|
| **Formatter** | Prettier |
| **Linter** | ESLint con config React |
| **Naming: componentes** | PascalCase |
| **Naming: funciones/variables** | camelCase |
| **Naming: constantes** | UPPER_SNAKE_CASE |
| **Types** | TypeScript strict mode |
| **Archivos componentes** | PascalCase.tsx |

### 7.3 Base de Datos

| Aspecto | Convención |
|---------|------------|
| **Tablas** | snake_case, plural (scans, images) |
| **Columnas** | snake_case (created_at, scan_id) |
| **Primary keys** | id (UUID) |
| **Foreign keys** | {tabla_singular}_id (scan_id) |
| **Índices** | idx_{tabla}_{columnas} |
| **Timestamps** | created_at, updated_at en todas las tablas |

### 7.4 Commits

Conventional Commits obligatorio:

```
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
refactor: refactorización sin cambio funcional
test: añadir o modificar tests
chore: mantenimiento (deps, config)
```

Formato: `tipo(scope): descripción breve`

Ejemplo: `feat(scans): add image upload endpoint`

### 7.5 Histórico de Commits (OBLIGATORIO)

> **CRÍTICO**: Todo commit debe documentarse en `docs/historico_commits.md` de forma simultánea.

| Regla | Descripción |
|-------|-------------|
| **Archivo** | `docs/historico_commits.md` |
| **Orden** | Cronológico inverso (más reciente arriba) |
| **Cuándo actualizar** | En el mismo momento que se hace el commit |
| **Quién actualiza** | El autor del commit (agente o humano) |

---

## 8. Testing

| Aspecto | Especificación |
|---------|----------------|
| **Framework backend** | pytest + pytest-asyncio |
| **Framework frontend** | vitest + testing-library |
| **Cobertura mínima** | 80% |
| **CI blocking** | Tests deben pasar para merge |

### 8.1 Tests Requeridos

| Tipo | Cuándo es Obligatorio | Ubicación |
|------|----------------------|-----------|
| **Unitarios** | vision_service, world_model_service, guide_service | /tests/unit |
| **Integración** | Endpoints de API | /tests/integration |
| **E2E** | Flujo completo upload → análisis → guía | /tests/e2e |

### 8.2 Convenciones de Tests

```python
# Naming: test_{función}_{escenario}_{resultado_esperado}
def test_analyze_image_valid_data_returns_barriers():
    ...

def test_analyze_image_invalid_format_returns_400():
    ...
```

---

## 9. Variables de Entorno

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

## 10. Constraints del Proyecto

| Constraint | Valor | Razón |
|------------|-------|-------|
| Presupuesto cloud | ~$50/mes | POC con recursos limitados |
| Vision API calls | ~100/día | Costo de GPT-4V |
| Max imágenes/scan | 20 | Limitar procesamiento |
| Tamaño max imagen | 10MB | Performance upload |
| Formatos imagen | JPEG, PNG, WebP | Compatibilidad Vision AI |

---

## 11. Git Workflow

### 11.1 Ramas

| Rama | Propósito | Protegida |
|------|-----------|-----------|
| `main` | Producción. Código desplegado. | ✅ |
| `staging` | Pre-producción (default). Deploy a staging. | ✅ |
| `feature/*` | Desarrollo de funcionalidades. | ❌ |
| `fix/*` | Corrección de bugs. | ❌ |
| `hotfix/*` | Correcciones urgentes en prod. | ❌ |

### 11.2 Protecciones

| Rama | Push Directo | PR Requerido | Aprobación | CI Requerido |
|------|--------------|--------------|------------|--------------|
| `main` | ❌ | ✅ | Manual (1+ persona) | ✅ |
| `staging` | ❌ | ✅ | Auto (si CI pasa) | ✅ |

### 11.3 Flujo de Desarrollo Normal

```
feature/xxx → PR → staging → validación → PR → main
                      ↓                         ↓
              (CI + deploy staging)    (deploy producción)
```

---

## 12. Deployment

### 12.1 Entornos

| Entorno | URL | Trigger |
|---------|-----|---------|
| Staging | staging.nubemfeast.app | Push a staging |
| Production | nubemfeast.app | Push a main |

### 12.2 CI/CD Pipeline

1. **ci.yml**: Lint, tests, spec-verify en PRs
2. **deploy-staging.yml**: Build + deploy a Cloud Run staging
3. **deploy-production.yml**: Build + deploy a Cloud Run producción

---

## 13. Documentos Relacionados

| Documento | Propósito | Ubicación |
|-----------|-----------|-----------|
| DATA_MODELS.md | Especificación de entidades | /docs/DATA_MODELS.md |
| API Contracts | Contratos OpenAPI | /docs/api_contracts/*.yaml |
| ARCHITECTURE_DECISIONS.md | Log de decisiones | /docs/ARCHITECTURE_DECISIONS.md |
| TASK_HISTORY.md | Historial de tareas | /docs/TASK_HISTORY.md |
| historico_commits.md | Historial detallado de commits | /docs/historico_commits.md |

---

## Historial de Cambios del Contrato

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0.0 | 2026-02-02 | architect-agent | Versión inicial |
| | | | |

---

*Este documento es la referencia técnica autoritativa del proyecto. Todo código debe cumplir con las especificaciones aquí definidas. Cambios a este documento requieren aprobación explícita.*
