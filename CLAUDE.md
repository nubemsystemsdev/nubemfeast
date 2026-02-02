# CLAUDE.md - [Nombre del Proyecto]

> **Este archivo contiene instrucciones operativas para Claude Code.**
> Para especificaciones técnicas, consultar `docs/CONTRATO_TECNICO.md`.

---

## Contexto del Proyecto

**Fuente de verdad técnica:** @docs/CONTRATO_TECNICO.md

[Descripción breve del proyecto - 1-2 líneas]

---

## Comandos de Desarrollo

```bash
# Instalar dependencias
[comando de instalación]

# Ejecutar en desarrollo
[comando de desarrollo]

# Ejecutar tests
[comando de tests]

# Linting
[comando de lint]

# Build
[comando de build]
```

---

## Reglas de Sesión (OBLIGATORIAS)

### Antes de Escribir Código
1. **Verificar rama actual**: `git branch --show-current`
2. Si es `main` o `staging` → BLOQUEAR y crear rama `feature/xxx`
3. Consultar `docs/CONTRATO_TECNICO.md` para decisiones arquitectónicas

### Al Hacer Commit
1. **Actualizar histórico**: Añadir entrada en `docs/historico_commits.md`
2. **Formato**: `tipo(scope): descripción en español`
3. **Orden**: Histórico primero, luego commit

### Workflow Git
- Nunca push directo a `main` o `staging`
- Todo cambio entra por Pull Request
- Commits en español, formato conventional commits

---

## Variables de Entorno Requeridas

```bash
# Copiar de .env.example
cp .env.example .env

# Variables obligatorias
# [Listar variables críticas sin valores]
```

---

## Estructura del Proyecto

```
/
├── CLAUDE.md                    # Este archivo (instrucciones operativas)
├── docs/
│   ├── CONTRATO_TECNICO.md      # Fuente de verdad técnica
│   └── historico_commits.md     # Registro detallado de commits
├── [estructura específica del proyecto]
```

---

## Referencias Rápidas

| Necesito... | Consultar |
|-------------|-----------|
| Stack tecnológico | `docs/CONTRATO_TECNICO.md#stack-tecnológico` |
| Convenciones de código | `docs/CONTRATO_TECNICO.md#convenciones-de-código` |
| Arquitectura | `docs/CONTRATO_TECNICO.md#arquitectura` |
| Histórico de cambios | `docs/historico_commits.md` |

---

## Notas Específicas del Proyecto

[Añadir aquí cualquier gotcha, comportamiento no obvio, o instrucción específica que Claude necesite saber para trabajar efectivamente en este proyecto]
