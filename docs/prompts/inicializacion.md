# Instrucciones de Inicialización de Proyecto Nubemsystems

Sigue estas instrucciones paso a paso para inicializar un nuevo proyecto.

---

## FASE 1: Recopilar Información

Antes de crear nada, obtén del usuario:

1. **¿Qué problema resuelve el proyecto?**
2. **¿Quiénes son los usuarios objetivo?**
3. **¿Funcionalidades principales?** (MVP)
4. **¿Integraciones con otros sistemas?**
5. **¿Preferencias de stack técnico?**

**REGLA:** No continúes si la descripción es vaga. Pregunta hasta tener claridad.

---

## FASE 2: Proponer Nombre

Convención: `Nubem` + `NombreDescriptivo` (PascalCase)

Ejemplos:
- `NubemInvoice` — Facturación
- `NubemDataVault` — Gestión de datos
- `NubemSmartFlow` — Automatización

**Acción:** Propón 2-3 nombres y espera aprobación del usuario.

---

## FASE 3: Generar Contrato Técnico

Basándote en los requisitos, genera el Contrato Técnico definiendo:

- Lenguaje y versión
- Framework principal
- Base de datos (si aplica)
- Patrón de arquitectura (con justificación)
- Estructura de carpetas
- Dependencias principales
- Framework de testing
- Convenciones de nombrado

Usa la plantilla de `docs/CONTRATO_TECNICO.md` del template como base.

**Acción:** Presenta el Contrato Técnico y espera aprobación explícita.

---

## FASE 4: Crear Proyecto Local

Una vez aprobado nombre y contrato:

```bash
# Crear carpeta del proyecto
mkdir -p [RUTA_TRABAJO]/[NOMBRE_PROYECTO]
cd [RUTA_TRABAJO]/[NOMBRE_PROYECTO]
```

---

## FASE 5: Descargar Template

```bash
# Clonar template (sin historial)
gh repo clone nubemsystemsdev/nubem-template . -- --depth 1

# Eliminar .git del template
rm -rf .git
```

---

## FASE 6: Personalizar Proyecto

### 6.1 Reemplazar placeholders

En todos los archivos (.md, .yml, .json, Dockerfile):
- `[NOMBRE_PROYECTO]` → nombre real del proyecto
- `[FECHA]` → fecha actual (YYYY-MM-DD)

### 6.2 Actualizar CONTRATO_TECNICO.md

Reemplazar el contenido de `docs/CONTRATO_TECNICO.md` con el Contrato Técnico aprobado en Fase 3.

### 6.3 Generar estructura específica

Crear carpetas y archivos según la arquitectura definida en el Contrato Técnico.

### 6.4 Eliminar carpeta prompts

```bash
# Los prompts son solo para el agente, no van en el proyecto final
rm -rf docs/prompts
```

---

## FASE 7: Crear Repositorio en GitHub

```bash
# Inicializar git
git init

# Crear repo en GitHub (privado, org nubemsystemsdev)
gh repo create nubemsystemsdev/[NOMBRE_PROYECTO] --private --source . --push

# Añadir team con permisos
gh api --method PUT orgs/nubemsystemsdev/teams/nubemsystems/repos/nubemsystemsdev/[NOMBRE_PROYECTO] \
  -f permission="push"
```

---

## FASE 8: Configurar Ramas

```bash
# Crear rama staging
git checkout -b staging
git push -u origin staging

# Volver a main
git checkout main
```

---

## FASE 9: Configurar Protecciones

### Main (requiere aprobación humana)

```bash
gh api --method PUT repos/nubemsystemsdev/[NOMBRE_PROYECTO]/branches/main/protection \
  -H "Accept: application/vnd.github+json" \
  --input - << 'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["✅ CI"]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

### Staging (sin aprobación, solo CI)

```bash
gh api --method PUT repos/nubemsystemsdev/[NOMBRE_PROYECTO]/branches/staging/protection \
  -H "Accept: application/vnd.github+json" \
  --input - << 'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": ["✅ CI"]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

---

## FASE 10: Configurar Environments

```bash
# Crear environments
gh api --method PUT repos/nubemsystemsdev/[NOMBRE_PROYECTO]/environments/staging
gh api --method PUT repos/nubemsystemsdev/[NOMBRE_PROYECTO]/environments/production

# Variables para staging
gh api --method POST repos/nubemsystemsdev/[NOMBRE_PROYECTO]/environments/staging/variables \
  -f name="GCP_PROJECT_ID" -f value="nubem-staging"
gh api --method POST repos/nubemsystemsdev/[NOMBRE_PROYECTO]/environments/staging/variables \
  -f name="GCP_REGION" -f value="europe-west1"

# Variables para production
gh api --method POST repos/nubemsystemsdev/[NOMBRE_PROYECTO]/environments/production/variables \
  -f name="GCP_PROJECT_ID" -f value="nubem-prod"
gh api --method POST repos/nubemsystemsdev/[NOMBRE_PROYECTO]/environments/production/variables \
  -f name="GCP_REGION" -f value="europe-west1"
```

---

## FASE 11: Confirmar Finalización

Informa al usuario:

1. **Ruta local:** `[RUTA_TRABAJO]/[NOMBRE_PROYECTO]`
2. **URL GitHub:** `https://github.com/nubemsystemsdev/[NOMBRE_PROYECTO]`
3. **Ramas:** main (producción), staging (integración)
4. **Protecciones:** Activas en ambas ramas
5. **Próximo paso:** Crear `feature/xxx` desde staging para empezar a desarrollar

---

## REGLAS CRÍTICAS

- ❌ No avanzar de fase sin aprobación explícita del usuario
- ❌ No crear repo sin Contrato Técnico aprobado
- ✅ Todas las decisiones técnicas deben estar justificadas
- ✅ El Contrato Técnico es la fuente de verdad
