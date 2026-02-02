# Nubem Template

Template oficial de Nubemsystems para proyectos de software. Este repositorio contiene la metodología, plantillas y configuraciones estándar.

---

## Para Agentes IA (Claude Code)

Este template está diseñado para ser usado por agentes IA que asisten en el desarrollo de software siguiendo la metodología Nubemsystems.

### Configuración Inicial (Obligatoria)

El usuario debe instalar el agente Method-Master en su entorno local:

```bash
# Crear carpeta de agents si no existe
mkdir -p ~/.claude/agents

# Descargar el agente Method-Master
curl -sSL https://raw.githubusercontent.com/nubemsystemsdev/nubem-template/main/docs/agents/Method-Master.md \
  -o ~/.claude/agents/Method-Master.md
```

Una vez instalado, el agente Method-Master guiará todo el desarrollo siguiendo la metodología.

---

## Estructura del Template

```
nubem-template/
├── .github/
│   ├── workflows/          # CI/CD pipelines
│   ├── CODEOWNERS          # Propietarios del código
│   ├── ISSUE_TEMPLATE/     # Plantillas de issues
│   ├── pull_request_template.md
│   └── dependabot.yml
├── docs/
│   ├── agents/
│   │   └── Method-Master.md    # Agente guía de metodología
│   ├── prompts/
│   │   ├── inicializacion.md   # Instrucciones para crear proyectos
│   │   └── dev.md              # Instrucciones para desarrollo
│   ├── CONTRATO_TECNICO.md     # Plantilla del contrato técnico
│   └── historico_commits.md    # Registro detallado de commits
├── CLAUDE.md               # Instrucciones operativas para Claude Code
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── .editorconfig
├── .gitignore
└── .nvmrc
```

### Sistema de Documentación Dual

Este template implementa un sistema de dos archivos complementarios:

| Archivo | Propósito | Ubicación |
|---------|-----------|-----------|
| **CLAUDE.md** | Instrucciones operativas (cómo trabajar) | Raíz del proyecto |
| **CONTRATO_TECNICO.md** | Especificaciones técnicas (qué construir) | `docs/` |

**CLAUDE.md** es leído automáticamente por Claude Code al inicio de cada sesión y contiene comandos, workflows y reglas de comportamiento. **CONTRATO_TECNICO.md** es la fuente de verdad técnica con arquitectura, stack y convenciones.

---

## Documentación para Agentes

| Archivo | Propósito | Cuándo consultarlo |
|---------|-----------|-------------------|
| `CLAUDE.md` | Instrucciones operativas para Claude Code | Se carga automáticamente al inicio de sesión |
| `docs/agents/Method-Master.md` | Guía completa de la metodología | Siempre activo como agente |
| `docs/prompts/inicializacion.md` | Instrucciones paso a paso para inicializar proyectos | Cuando el usuario quiere crear un proyecto nuevo |
| `docs/prompts/dev.md` | Instrucciones para desarrollo iterativo | Cuando el usuario quiere implementar funcionalidades |
| `docs/CONTRATO_TECNICO.md` | Plantilla del Contrato Técnico (fuente de verdad) | Al generar el contrato de un nuevo proyecto |
| `docs/historico_commits.md` | Registro detallado de cada commit | Actualizar con cada commit realizado |

---

## Flujos Principales

### 1. Inicializar Proyecto Nuevo

Cuando el usuario indique que quiere crear un nuevo proyecto:

```bash
# Consultar instrucciones detalladas
gh repo clone nubemsystemsdev/nubem-template /tmp/nubem-template -- --depth 1
cat /tmp/nubem-template/docs/prompts/inicializacion.md
```

Seguir las fases descritas en ese archivo.

### 2. Desarrollar Funcionalidad

Cuando el usuario quiera implementar algo en un proyecto existente:

```bash
# Consultar instrucciones detalladas
cat /tmp/nubem-template/docs/prompts/dev.md
```

**CRÍTICO:** Siempre verificar la rama actual antes de escribir código:
```bash
git branch --show-current
```
Si es `main` o `staging` → BLOQUEAR y crear rama `feature/xxx`.

---

## Reglas Fundamentales

### Prohibiciones Absolutas
- ❌ Push directo a `main` o `staging`
- ❌ Escribir código sin verificar rama actual
- ❌ Modificar Contrato Técnico sin aprobación
- ❌ Saltarse el flujo de PRs

### Obligaciones
- ✅ Todo cambio entra por PR
- ✅ Leer Contrato Técnico antes de implementar
- ✅ Tests para toda funcionalidad nueva
- ✅ Commits con formato: `<tipo>: <descripción>`

---

## Convenciones

### Nombres de Repositorio
```
Nubem + NombreDescriptivo (PascalCase)
```
Ejemplos: `NubemInvoice`, `NubemDataVault`, `NubemSmartFlow`

### Commits
```
feat: nueva funcionalidad
fix: corrección de bug
docs: documentación
refactor: refactorización
test: tests
chore: mantenimiento
```

### Ramas
```
main        → Producción
staging     → Integración/pruebas
feature/xxx → Desarrollo de funcionalidades
hotfix/xxx  → Correcciones urgentes
```

---

## Organización GitHub

- **Organización:** `nubemsystemsdev`
- **Team:** `nubemsystems`
- **Template:** Este repositorio

---

## Actualización del Agente

Para actualizar Method-Master a la última versión:

```bash
curl -sSL https://raw.githubusercontent.com/nubemsystemsdev/nubem-template/main/docs/agents/Method-Master.md \
  -o ~/.claude/agents/Method-Master.md
```
