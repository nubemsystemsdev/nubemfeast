# Histórico de Commits

> **Registro detallado de todos los commits del proyecto.**
>
> - Orden: Cronológico inverso (más reciente arriba)
> - Actualizar: Siempre que se haga un commit
> - Formato: Ver CONTRATO_TECNICO.md para especificaciones

---

<!-- AÑADIR NUEVOS COMMITS AQUÍ ARRIBA -->

## Commit 3: "docs: consolida documentación en carpeta docs según metodología template" - 02/02/2026

Se consolida toda la documentación técnica del proyecto en la carpeta `docs/` siguiendo la estructura del template nubem-template.

**Contexto:**
Durante la inicialización del proyecto se creó una carpeta `specs/` con la documentación técnica, pero el template de nubemsystems utiliza `docs/` como carpeta estándar para documentación. Esto generaba conflicto con archivos duplicados (CONTRATO_TECNICO.md existía en ambas carpetas).

**Cambios realizados:**
- Fusionado `specs/CONTRATO_TECNICO.md` (contenido específico NubemFeast) con `docs/CONTRATO_TECNICO.md` (estructura metodológica)
- Movido `specs/DATA_MODELS.md` → `docs/DATA_MODELS.md`
- Movido `specs/ARCHITECTURE_DECISIONS.md` → `docs/ARCHITECTURE_DECISIONS.md`
- Movido `specs/TASK_HISTORY.md` → `docs/TASK_HISTORY.md`
- Movido `specs/api_contracts/` → `docs/api_contracts/`
- Eliminada carpeta `specs/` (ya no existe)
- Actualizada estructura de carpetas en CONTRATO_TECNICO.md para reflejar `docs/` como ubicación

**Estructura final docs/:**
```
docs/
├── CONTRATO_TECNICO.md      # Fuente de verdad técnica (fusionado)
├── DATA_MODELS.md           # Especificación de entidades
├── ARCHITECTURE_DECISIONS.md # Log de decisiones arquitectónicas
├── TASK_HISTORY.md          # Historial de tareas
├── historico_commits.md     # Este archivo
├── api_contracts/           # Contratos OpenAPI
│   ├── scans.yaml
│   ├── analysis.yaml
│   └── navigation.yaml
├── agents/                  # Documentación de agentes (del template)
└── prompts/                 # Prompts de metodología (del template)
```

**Archivos afectados:**
- `docs/CONTRATO_TECNICO.md` (reescrito - fusión completa)
- `docs/DATA_MODELS.md` (movido desde specs/)
- `docs/ARCHITECTURE_DECISIONS.md` (movido desde specs/)
- `docs/TASK_HISTORY.md` (movido desde specs/)
- `docs/api_contracts/*` (movido desde specs/)
- `docs/historico_commits.md` (modificado)
- `specs/` (eliminada)

---

## Commit 2: "docs: implementa sistema de documentación dual CLAUDE.md + CONTRATO_TECNICO" - 27/01/2026

Se establece el sistema de documentación dual para proyectos Nubemsystems:

**Concepto:**
- `CLAUDE.md`: Instrucciones operativas para Claude Code (cómo trabajar)
- `CONTRATO_TECNICO.md`: Fuente de verdad técnica (qué construir)

**Cambios realizados:**
- Creado `CLAUDE.md` en raíz como plantilla de instrucciones operativas
- Añadida sección "Sistema de Documentación Dual" en `docs/CONTRATO_TECNICO.md`
- Definida jerarquía de precedencia entre ambos archivos
- Documentado flujo de trabajo conjunto
- Actualizado `README.md` con nueva estructura y tabla de documentación

**Archivos afectados:**
- `CLAUDE.md` (nuevo)
- `docs/CONTRATO_TECNICO.md` (modificado - nueva sección de documentación dual)
- `docs/historico_commits.md` (modificado)
- `README.md` (modificado - estructura y tabla actualizadas)

---

## Commit 1: "docs: añade sistema de histórico de commits" - 27/01/2026

Se establece el sistema de documentación de histórico de commits:
- Creado archivo `docs/historico_commits.md` para registro detallado
- Actualizado `docs/CONTRATO_TECNICO.md` con la sección obligatoria de histórico
- Definido formato estándar para entradas de commits
- Establecido flujo de trabajo: actualizar histórico antes de cada commit

Archivos afectados:
- `docs/historico_commits.md` (nuevo)
- `docs/CONTRATO_TECNICO.md` (modificado - nueva sección "Histórico de Commits")

---
