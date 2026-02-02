# Instrucciones de Desarrollo Iterativo Nubemsystems

Sigue estas instrucciones para implementar funcionalidades en un proyecto existente.

---

## ANTES DE EMPEZAR

1. **Verificar rama actual:**
   ```bash
   git branch --show-current
   ```

2. **Si estás en `main` o `staging` → BLOQUEAR:**
   ```
   ⛔ BLOQUEO DE SEGURIDAD

   Estás en la rama `[main/staging]`, que es una rama protegida.
   NO puedo escribir código directamente aquí.

   Voy a crear: `feature/[descripcion-de-la-tarea]`

   ¿Procedo?
   ```

3. **Leer el Contrato Técnico:**
   ```bash
   cat docs/CONTRATO_TECNICO.md
   ```

---

## FASE 1: Análisis

### 1.1 Evaluar la especificación

Analiza la funcionalidad solicitada:

- ¿Es coherente con la arquitectura del Contrato Técnico?
- ¿Qué componentes/módulos se ven afectados?
- ¿Se necesitan nuevas dependencias?
- ¿Requiere cambios en la base de datos?
- ¿Qué tests serán necesarios?

### 1.2 Evaluar impacto en el Contrato Técnico

Si la funcionalidad requiere cambios que afectan al Contrato:

- Identificar qué sección se vería afectada
- Justificar por qué es necesario el cambio
- Proponer la modificación concreta
- **Esperar aprobación del usuario antes de continuar**

Cambios que requieren modificación del contrato:
- Nueva dependencia principal
- Cambio en la estructura de carpetas
- Nuevo patrón de diseño
- Cambio en la estrategia de testing

### 1.3 Presentar plan de implementación

Presenta al usuario:
- Resumen de lo que vas a implementar
- Archivos que se crearán o modificarán
- Dependencias nuevas (si las hay)
- Tests que se añadirán
- Cambios propuestos al Contrato Técnico (si los hay)

**Espera confirmación del usuario antes de continuar.**

---

## FASE 2: Implementación

### 2.1 Crear rama de trabajo

```bash
git checkout staging
git pull origin staging
git checkout -b feature/nombre-descriptivo
```

### 2.2 Implementar la funcionalidad

- Sigue estrictamente la arquitectura del Contrato Técnico
- Respeta las convenciones de nombrado
- Escribe código limpio
- Implementa los tests definidos en el plan

### 2.3 Commits

Formato: `<tipo>: <descripción en imperativo>`

| Tipo | Uso |
|------|-----|
| `feat` | Nueva funcionalidad |
| `fix` | Corrección de bug |
| `docs` | Documentación |
| `refactor` | Refactorización |
| `test` | Tests |
| `chore` | Mantenimiento |

Reglas:
- Máximo ~50 caracteres
- Usar imperativo: "añadir", "corregir" (no "añadido")
- Sin punto final
- Commits pequeños y atómicos

### 2.4 Actualizar Contrato Técnico (si aplica)

Si se aprobaron cambios al Contrato:
```bash
# Editar docs/CONTRATO_TECNICO.md
git add docs/CONTRATO_TECNICO.md
git commit -m "docs: actualizar contrato técnico"
```

### 2.5 Verificación local

Antes de subir:
```bash
# Ejecutar tests
npm test  # o el comando correspondiente

# Ejecutar linter
npm run lint  # o el comando correspondiente

# Verificar Docker (si aplica)
docker-compose up --build
```

---

## FASE 3: Pull Request a Staging

### 3.1 Subir la rama

```bash
git push -u origin feature/nombre-descriptivo
```

### 3.2 Crear el Pull Request

```bash
gh pr create --base staging --title "feat: descripción breve" --body "$(cat <<'EOF'
## Qué se ha hecho
[Descripción de los cambios]

## Cómo probarlo
[Pasos para verificar]

## Checklist
- [ ] Tests añadidos/actualizados
- [ ] Código sigue el Contrato Técnico
- [ ] Probado en local
EOF
)"
```

### 3.3 Verificar CI y mergear

Si el CI pasa:
```bash
# Aprobar y mergear (staging no requiere aprobación manual)
gh pr merge --squash --delete-branch
```

### 3.4 Informar al usuario

Proporciona:
- URL del Pull Request
- Resumen de los cambios
- URL del entorno staging para validar
- Indica que para producción se necesita PR a main (requiere aprobación manual)

---

## REGLAS CRÍTICAS

| Acción | main | staging | feature/* | hotfix/* |
|--------|------|---------|-----------|----------|
| Escribir código | ❌ | ❌ | ✅ | ✅ |
| Hacer commits | ❌ | ❌ | ✅ | ✅ |
| Push directo | ❌ | ❌ | ✅ | ✅ |
| Leer código | ✅ | ✅ | ✅ | ✅ |

- **SIEMPRE** ejecutar guardia pre-código (verificar rama actual)
- **NUNCA** push directo a staging o main
- **NUNCA** modificar el Contrato Técnico sin aprobación
- **SIEMPRE** leer el Contrato Técnico antes de implementar
- **SIEMPRE** trabajar en una rama feature

---

## FLUJO DE HOTFIX (Errores urgentes en producción)

Solo para bugs críticos que afectan a usuarios en producción:

```bash
# 1. Crear rama desde MAIN (no staging)
git checkout main
git pull origin main
git checkout -b hotfix/descripcion-del-bug

# 2. Implementar corrección mínima

# 3. PR directo a main (requiere aprobación manual urgente)
gh pr create --base main --title "fix: descripción del bug"

# 4. Tras mergear, sincronizar staging
git checkout staging
git pull origin main
git push origin staging
```
