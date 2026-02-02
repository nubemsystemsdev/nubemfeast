# Contrato Técnico del Proyecto

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

### CLAUDE.md (Instrucciones Operativas)

**Ubicación:** Raíz del proyecto (`./CLAUDE.md`)

**Contenido recomendado:**
- Comandos Bash específicos del proyecto
- Workflows de desarrollo (testing, linting, build)
- Reglas de comportamiento para Claude Code
- Referencias a documentación (`@docs/CONTRATO_TECNICO.md`)
- Instrucciones de sesión y contexto

**Ejemplo de estructura:**
```markdown
# CLAUDE.md - [Nombre del Proyecto]

## Contexto del Proyecto
@docs/CONTRATO_TECNICO.md

## Comandos de Desarrollo
- Tests: `npm test` / `pytest`
- Lint: `npm run lint` / `ruff check`
- Build: `npm run build`

## Reglas de Sesión
- Siempre verificar rama antes de escribir código
- Actualizar docs/historico_commits.md con cada commit
- Consultar CONTRATO_TECNICO.md antes de decisiones arquitectónicas

## Workflow Git
- Nunca push directo a main/staging
- Crear PR para todo cambio
- Commits en español, formato conventional commits
```

### CONTRATO_TECNICO.md (Fuente de Verdad Técnica)

**Ubicación:** `docs/CONTRATO_TECNICO.md`

**Contenido:**
- Stack tecnológico y justificaciones
- Arquitectura y patrones
- Convenciones de código
- Configuración de CI/CD
- Restricciones y constraints

### Jerarquía de Precedencia

```
1. Instrucciones explícitas del usuario en el chat (MÁXIMA)
2. CLAUDE.md del proyecto (instrucciones operativas)
3. CONTRATO_TECNICO.md (especificaciones técnicas)
4. Convenciones deducidas del código (MÍNIMA)
```

### Flujo de Trabajo Conjunto

```
┌─────────────────────────────────────────────────────────────┐
│                    INICIO DE SESIÓN                         │
├─────────────────────────────────────────────────────────────┤
│  1. Claude Code carga CLAUDE.md automáticamente             │
│  2. CLAUDE.md referencia @docs/CONTRATO_TECNICO.md          │
│  3. Claude tiene contexto operativo + técnico               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    DURANTE DESARROLLO                       │
├─────────────────────────────────────────────────────────────┤
│  • Decisión operativa (cómo ejecutar) → CLAUDE.md           │
│  • Decisión técnica (qué arquitectura) → CONTRATO_TECNICO   │
│  • Conflicto entre ambos → Prevalece CONTRATO_TECNICO       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    AL HACER COMMIT                          │
├─────────────────────────────────────────────────────────────┤
│  1. Actualizar docs/historico_commits.md (obligatorio)      │
│  2. Si hay cambio arquitectónico → Actualizar CONTRATO      │
│  3. Si hay nuevo comando/workflow → Actualizar CLAUDE.md    │
└─────────────────────────────────────────────────────────────┘
```

### Creación Obligatoria

> **CRÍTICO**: Todo proyecto Nubemsystems DEBE tener ambos archivos:
> - `./CLAUDE.md` → Creado en la inicialización del proyecto
> - `docs/CONTRATO_TECNICO.md` → Creado en la inicialización del proyecto

---

## Metadata

| Campo | Valor |
|-------|-------|
| **Nombre del proyecto** | [A rellenar] |
| **Descripción** | [A rellenar] |
| **Versión del contrato** | 1.0.0 |
| **Fecha de creación** | [Fecha ISO] |
| **Última actualización** | [Fecha ISO] |
| **Actualizado por** | [agent_id o human] |

---

## Stack Tecnológico

### Backend

| Aspecto | Decisión | Justificación |
|---------|----------|---------------|
| **Lenguaje** | [Ej: Python 3.11] | [Por qué se eligió] |
| **Framework** | [Ej: FastAPI] | [Por qué se eligió] |
| **ORM/DB Client** | [Ej: SQLAlchemy 2.0] | [Por qué se eligió] |
| **Validación** | [Ej: Pydantic v2] | [Por qué se eligió] |

### Base de Datos

| Aspecto | Decisión | Justificación |
|---------|----------|---------------|
| **Motor** | [Ej: PostgreSQL 15] | [Por qué se eligió] |
| **Migraciones** | [Ej: Alembic] | [Por qué se eligió] |
| **Naming convention** | [Ej: snake_case, tablas en plural] | [Por qué se eligió] |

### Frontend (si aplica)

| Aspecto | Decisión | Justificación |
|---------|----------|---------------|
| **Framework** | [Ej: React 18] | [Por qué se eligió] |
| **State management** | [Ej: Zustand] | [Por qué se eligió] |
| **Styling** | [Ej: Tailwind CSS] | [Por qué se eligió] |
| **HTTP Client** | [Ej: axios] | [Por qué se eligió] |

### Infraestructura

| Aspecto | Decisión | Justificación |
|---------|----------|---------------|
| **Cloud provider** | [Ej: AWS] | [Por qué se eligió] |
| **Compute** | [Ej: Lambda + API Gateway] | [Por qué se eligió] |
| **Database hosting** | [Ej: RDS PostgreSQL] | [Por qué se eligió] |
| **CI/CD** | [Ej: GitHub Actions] | [Por qué se eligió] |

---

## Dependencias Principales

> Solo listar dependencias que definen la arquitectura. Dependencias auxiliares no requieren estar aquí.

### Backend

```
# Formato: nombre==versión - propósito
fastapi==0.109.0 - Framework web
sqlalchemy==2.0.25 - ORM
pydantic==2.5.3 - Validación y serialización
alembic==1.13.1 - Migraciones de DB
python-jose==3.3.0 - JWT handling
passlib==1.7.4 - Password hashing
```

### Frontend

```
# Formato: nombre@versión - propósito
react@18.2.0 - UI framework
zustand@4.5.0 - State management
axios@1.6.5 - HTTP client
tailwindcss@3.4.1 - Styling
```

---

## Arquitectura

### Patrón Elegido

**Patrón:** [Ej: Arquitectura en Capas / Hexagonal / DDD simplificado]

**Justificación:** 
[Explicar por qué este patrón es apropiado para el proyecto. Mínimo 2-3 líneas.]

### Estructura de Carpetas

```
/backend
├── /src
│   ├── /api            # Endpoints FastAPI (routers)
│   ├── /core           # Configuración, dependencias, seguridad
│   ├── /models         # Modelos SQLAlchemy
│   ├── /schemas        # Schemas Pydantic (request/response)
│   ├── /services       # Lógica de negocio
│   └── /repositories   # Acceso a datos (si se usa Repository pattern)
├── /tests
│   ├── /unit
│   └── /integration
├── /alembic            # Migraciones
└── pyproject.toml

/frontend
├── /src
│   ├── /components     # Componentes React reutilizables
│   ├── /pages          # Componentes de página/vista
│   ├── /hooks          # Custom hooks
│   ├── /services       # Llamadas API
│   ├── /store          # Estado global (Zustand)
│   └── /utils          # Utilidades
├── /tests
└── package.json

/infrastructure
├── /terraform          # IaC (si aplica)
└── /.github/workflows  # CI/CD pipelines

/specs                  # FUENTE DE VERDAD - NO CÓDIGO
├── CONTRATO_TECNICO.md
├── DATA_MODELS.md
├── ARCHITECTURE_DECISIONS.md
├── TASK_HISTORY.md
├── /api_contracts
│   └── *.yaml
└── /pending_updates
    └── *.yaml
```

### Patrones Obligatorios

| Patrón | Dónde Aplicar | Ejemplo |
|--------|---------------|---------|
| Dependency Injection | Servicios en endpoints | `Depends(get_db)` |
| Repository Pattern | Acceso a datos | `UserRepository.get_by_id()` |
| DTO/Schema separation | API boundaries | Pydantic schemas separados de models |
| [Añadir más según proyecto] | | |

### Patrones Prohibidos

| Patrón | Razón |
|--------|-------|
| God classes | Viola Single Responsibility |
| Hardcoded configuration | Dificulta deployment |
| Direct SQL in controllers | Viola separación de capas |
| [Añadir más según proyecto] | |

---

## Convenciones de Código

### Python

| Aspecto | Convención |
|---------|------------|
| **Formatter** | black (line-length=88) |
| **Linter** | ruff |
| **Naming: funciones/variables** | snake_case |
| **Naming: clases** | PascalCase |
| **Naming: constantes** | UPPER_SNAKE_CASE |
| **Type hints** | Obligatorios en funciones públicas |
| **Docstrings** | Google style, obligatorios en funciones públicas |

### TypeScript/JavaScript

| Aspecto | Convención |
|---------|------------|
| **Formatter** | prettier |
| **Linter** | eslint |
| **Naming: funciones/variables** | camelCase |
| **Naming: componentes React** | PascalCase |
| **Naming: constantes** | UPPER_SNAKE_CASE |
| **Types** | TypeScript strict mode |

### Base de Datos

| Aspecto | Convención |
|---------|------------|
| **Tablas** | snake_case, plural (users, expenses) |
| **Columnas** | snake_case (created_at, user_id) |
| **Primary keys** | id (UUID preferido) |
| **Foreign keys** | {tabla_singular}_id (user_id) |
| **Índices** | idx_{tabla}_{columnas} |
| **Timestamps** | created_at, updated_at en todas las tablas |

### Commits

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

Ejemplo: `feat(expenses): add category filtering endpoint`

### Histórico de Commits (OBLIGATORIO)

> **CRÍTICO**: Todo commit debe documentarse en `docs/historico_commits.md` de forma simultánea.

| Regla | Descripción |
|-------|-------------|
| **Archivo** | `docs/historico_commits.md` |
| **Orden** | Cronológico inverso (más reciente arriba) |
| **Cuándo actualizar** | En el mismo momento que se hace el commit |
| **Quién actualiza** | El autor del commit (agente o humano) |

#### Formato de Entrada

```markdown
## Commit [número]: "[tipo]: descripción corta" - DD/MM/YYYY

[Descripción detallada de los cambios realizados. Incluir:]
- Qué archivos se modificaron/crearon
- Por qué se hicieron los cambios
- Impacto en el sistema
- Referencias a issues/PRs si aplica

---
```

#### Ejemplo

```markdown
## Commit 24: "feat(auth): implementa autenticación JWT" - 26/01/2026

Se ha implementado el sistema de autenticación basado en JWT:
- Creados endpoints `/auth/login` y `/auth/refresh`
- Añadido middleware de verificación de tokens
- Configuradas variables de entorno para secrets
- Tests unitarios para el servicio de autenticación

Archivos afectados:
- `src/api/auth.py` (nuevo)
- `src/core/security.py` (nuevo)
- `src/core/dependencies.py` (modificado)
- `tests/unit/test_auth.py` (nuevo)

---
```

#### Flujo de Trabajo

```
1. Realizar cambios en el código
2. Actualizar docs/historico_commits.md (añadir entrada arriba)
3. git add [archivos] docs/historico_commits.md
4. git commit -m "tipo(scope): descripción"
```

> ⚠️ **BLOQUEO**: No se permite hacer commit sin actualizar el histórico. Los agentes deben verificar esto automáticamente.

---

## Testing

### Configuración

| Aspecto | Valor |
|---------|-------|
| **Framework backend** | pytest |
| **Framework frontend** | vitest + testing-library |
| **Cobertura mínima** | 80% |
| **CI blocking** | Tests deben pasar para merge |

### Tipos de Tests Requeridos

| Tipo | Cuándo es Obligatorio | Ubicación |
|------|----------------------|-----------|
| **Unitarios** | Toda lógica de negocio en services | /tests/unit |
| **Integración** | Endpoints de API | /tests/integration |
| **E2E** | Flujos críticos (auth, checkout) | /tests/e2e |

### Convenciones de Tests

```python
# Naming: test_{función}_{escenario}_{resultado_esperado}
def test_create_expense_valid_data_returns_201():
    ...

def test_create_expense_negative_amount_returns_400():
    ...
```

---

## Seguridad

### Autenticación

| Aspecto | Decisión |
|---------|----------|
| **Método** | JWT |
| **Almacenamiento** | httpOnly cookies |
| **Expiración access token** | [Ej: 15 min] |
| **Expiración refresh token** | [Ej: 7 días] |
| **Refresh strategy** | Automatic con interceptor |

### Secretos y Configuración

| Regla | Descripción |
|-------|-------------|
| **NUNCA hardcodear** | Credenciales, API keys, tokens, URLs de DB |
| **Variables de entorno** | Toda configuración sensible |
| **Naming de env vars** | UPPER_SNAKE_CASE, prefijo por servicio |
| **Ejemplo** | `DATABASE_URL`, `JWT_SECRET`, `AWS_ACCESS_KEY_ID` |

### Variables de Entorno Requeridas

```bash
# Backend
DATABASE_URL=postgresql://...
JWT_SECRET=...
JWT_ALGORITHM=HS256

# AWS (si aplica)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=...

# [Añadir más según proyecto]
```

---

## Flujo de Trabajo Git

### Ramas

| Rama | Propósito | Protegida |
|------|-----------|-----------|
| `main` | Producción. Código desplegado. | ✅ |
| `staging` | Integración. Deploy a staging. | ✅ |
| `feature/*` | Desarrollo de funcionalidades. | ❌ |
| `hotfix/*` | Correcciones urgentes en prod. | ❌ |

### Protecciones

| Rama | Push Directo | PR Requerido | Aprobación | CI Requerido |
|------|--------------|--------------|------------|--------------|
| `main` | ❌ | ✅ | Manual (1+ persona) | ✅ |
| `staging` | ❌ | ✅ | Auto (si CI pasa) | ✅ |

### Flujo de Desarrollo Normal

```
feature/xxx → PR → staging → validación → PR → main
                      ↓                         ↓
              (CI + deploy staging)    (deploy producción)
```

### Flujo de Hotfix

```
main → hotfix/xxx → PR → main → deploy prod → sync staging
```

1. Crear rama `hotfix/xxx` desde `main`
2. Implementar corrección mínima
3. PR directo a `main` (requiere aprobación manual urgente)
4. Merge y deploy a producción
5. Sincronizar `staging` con `main`

---

## CI/CD

### Pipeline de PR

```yaml
# Ejecuta en cada PR a staging o main
steps:
  - lint          # Verificar formato y estilo
  - type-check    # Verificar tipos (mypy/tsc)
  - test          # Ejecutar tests
  - spec-verify   # Verificar consistencia con specs
  - security-scan # Buscar vulnerabilidades
```

### Condiciones para Merge

| Check | Requerido para staging | Requerido para main |
|-------|----------------------|---------------------|
| Lint pass | ✅ | ✅ |
| Tests pass | ✅ | ✅ |
| Coverage ≥ 80% | ✅ | ✅ |
| Spec consistency | ✅ | ✅ |
| Security scan pass | ✅ | ✅ |
| Aprobación manual | ❌ | ✅ |

### Deploy

| Evento | Acción |
|--------|--------|
| Merge a `staging` | Deploy automático a entorno staging |
| Merge a `main` | Deploy automático a producción |

---

## Versionado

### Semantic Versioning

Formato: `vMAJOR.MINOR.PATCH`

| Cambio | Incrementa |
|--------|------------|
| Breaking change en API | MAJOR |
| Nueva funcionalidad compatible | MINOR |
| Bug fix | PATCH |

### Tags

- Crear tag en `main` tras cada release a producción
- Formato: `v1.0.0`, `v1.1.0`, `v1.1.1`
- Los hotfixes incrementan PATCH

---

## Gestión de Dependencias

### Añadir Dependencia Nueva

1. **Evaluar necesidad**: ¿Es realmente necesaria? ¿Hay alternativa nativa?
2. **Verificar seguridad**: Comprobar vulnerabilidades conocidas
3. **Verificar licencia**: Compatible con el proyecto
4. **Añadir** al archivo de dependencias
5. **Documentar** en este contrato si es dependencia principal
6. **Generar SPEC_UPDATE_REQUEST** si modifica arquitectura

### Cuándo Actualizar Este Contrato

| Cambio | Requiere Update |
|--------|-----------------|
| Nueva dependencia principal | ✅ |
| Cambio de versión major de dep principal | ✅ |
| Eliminar dependencia principal | ✅ |
| Dependencia de desarrollo | ❌ |
| Actualización patch/minor | ❌ |

---

## Constraints del Proyecto

> Restricciones no negociables que guían todas las decisiones.

| Constraint | Valor | Razón |
|------------|-------|-------|
| **Presupuesto cloud mensual** | [Ej: $100] | [Límite del cliente] |
| **Regulaciones** | [Ej: GDPR] | [Ubicación de usuarios] |
| **Cloud provider** | [Ej: AWS] | [Infraestructura existente] |
| **Tiempo de respuesta API** | [Ej: <200ms p95] | [Requisito de UX] |

---

## Documentos Relacionados

| Documento | Propósito | Ubicación |
|-----------|-----------|-----------|
| DATA_MODELS.md | Especificación de entidades | /specs/DATA_MODELS.md |
| API Contracts | Contratos OpenAPI | /specs/api_contracts/*.yaml |
| ARCHITECTURE_DECISIONS.md | Log de decisiones | /specs/ARCHITECTURE_DECISIONS.md |
| TASK_HISTORY.md | Historial de tareas | /specs/TASK_HISTORY.md |
| **historico_commits.md** | **Historial detallado de commits** | **/docs/historico_commits.md** |

---

## Historial de Cambios del Contrato

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0.0 | [Fecha] | architect-agent | Versión inicial |
| | | | |

---

*Este documento es la referencia técnica autoritativa del proyecto. Todo código debe cumplir con las especificaciones aquí definidas. Cambios a este documento requieren aprobación explícita.*
