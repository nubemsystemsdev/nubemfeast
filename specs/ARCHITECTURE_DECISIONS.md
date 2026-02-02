# Architecture Decisions - NubemFeast

> Registro de decisiones arquitectónicas (ADR)
> Versión: 1.0.0

---

## ADR-001: Arquitectura en Capas + Repository Pattern

**Estado:** Aceptada
**Fecha:** 2026-02-02

### Contexto

Necesitamos definir la arquitectura base para el POC de NubemFeast. Las opciones consideradas fueron:
- Arquitectura en Capas simple
- Hexagonal Architecture (Ports & Adapters)
- Domain-Driven Design (DDD)
- Clean Architecture

### Decisión

Adoptamos **Arquitectura en Capas + Repository Pattern**.

### Justificación

1. **Simplicidad para POC**: Permite iterar rápidamente sin overhead de abstracciones complejas
2. **Separación clara**: API → Services → Repositories → Data mantiene responsabilidades claras
3. **Testabilidad**: Repository Pattern facilita mocking en tests
4. **Escalabilidad futura**: Si el POC tiene éxito, se puede evolucionar a Hexagonal sin reescribir

### Consecuencias

- (+) Desarrollo más rápido
- (+) Curva de aprendizaje baja
- (-) Menor flexibilidad que arquitecturas más complejas
- (-) Posible acoplamiento si no se mantiene disciplina

---

## ADR-002: SQLite para desarrollo, PostgreSQL para producción

**Estado:** Aceptada
**Fecha:** 2026-02-02

### Contexto

Necesitamos una base de datos que permita desarrollo rápido pero sea escalable en producción.

### Decisión

- **Desarrollo local**: SQLite con aiosqlite
- **Staging/Producción**: PostgreSQL

### Justificación

1. **SQLite para dev**: Cero configuración, archivo único, ideal para desarrollo rápido
2. **PostgreSQL para prod**: Concurrencia, escalabilidad, features avanzados
3. **SQLModel/SQLAlchemy**: Abstrae diferencias, mismo código funciona en ambos

### Consecuencias

- (+) Setup local instantáneo
- (+) Producción robusta
- (-) Pequeñas diferencias de comportamiento entre motores
- (-) Requiere testing en PostgreSQL antes de deploy

---

## ADR-003: OpenAI GPT-4o Vision como motor principal de análisis

**Estado:** Aceptada
**Fecha:** 2026-02-02

### Contexto

Necesitamos un servicio de Vision AI capaz de:
- Analizar imágenes de espacios
- Detectar barreras de accesibilidad
- Estimar medidas aproximadas
- Generar descripciones útiles

### Decisión

- **Principal**: OpenAI GPT-4o Vision
- **Backup**: Google Gemini 1.5 Pro

### Justificación

1. **GPT-4o Vision**: Mejor rendimiento en análisis espacial según benchmarks
2. **Estimación de medidas**: GPT-4o muestra mejor capacidad de estimación dimensional
3. **Gemini como backup**: Menor costo, útil si se exceden límites de presupuesto

### Consecuencias

- (+) Alta calidad de análisis
- (-) Costo por llamada relativamente alto (~$0.01-0.03/imagen)
- (-) Dependencia de servicio externo

---

## ADR-004: NetworkX para modelo de mundo

**Estado:** Aceptada
**Fecha:** 2026-02-02

### Contexto

Necesitamos representar espacios conectados y calcular rutas accesibles.

### Decisión

Usar NetworkX para crear y manipular el grafo de espacios.

### Justificación

1. **Madurez**: Librería probada con amplia documentación
2. **Algoritmos incluidos**: Pathfinding (Dijkstra, A*), análisis de conectividad
3. **Serialización**: Fácil exportar/importar JSON
4. **Python nativo**: Sin dependencias externas complejas

### Consecuencias

- (+) Implementación rápida de modelo de mundo
- (+) Algoritmos de pathfinding listos para usar
- (-) Todo en memoria, no escala a grafos muy grandes
- (-) Para producción a gran escala, considerar Neo4j

---

## ADR-005: TanStack Query para estado del servidor en frontend

**Estado:** Aceptada
**Fecha:** 2026-02-02

### Contexto

Necesitamos manejar:
- Fetching de datos del API
- Cache de respuestas
- Estados de loading/error
- Sincronización con el servidor

### Decisión

Usar TanStack Query (React Query) para toda la interacción con el API.

### Justificación

1. **Cache inteligente**: Evita re-fetches innecesarios
2. **Devtools**: Excelente para debugging
3. **Patterns establecidos**: useQuery, useMutation bien documentados
4. **Background refetch**: Mantiene datos frescos automáticamente

### Consecuencias

- (+) Menos boilerplate que Redux para datos del servidor
- (+) Mejor UX con cache y estados optimistas
- (-) Otra librería que aprender
- (-) No reemplaza estado local complejo (si lo hubiera)

---

## ADR-006: Framer Motion para animaciones del recorrido virtual

**Estado:** Aceptada
**Fecha:** 2026-02-02

### Contexto

El recorrido virtual necesita transiciones suaves entre imágenes y animaciones para alertas.

### Decisión

Usar Framer Motion para todas las animaciones de la interfaz.

### Justificación

1. **API declarativa**: Fácil de usar con React
2. **Performance**: Optimizado para 60fps
3. **AnimatePresence**: Perfecto para transiciones entre vistas
4. **Gestures**: Soporta swipe para navegación móvil

### Consecuencias

- (+) Animaciones fluidas y profesionales
- (+) Código legible y mantenible
- (-) Bundle size adicional (~30KB gzipped)

---

## ADR-007: Cloud Run para deployment

**Estado:** Aceptada
**Fecha:** 2026-02-02

### Contexto

Necesitamos infraestructura para hosting que sea:
- Económica para POC (bajo tráfico inicial)
- Escalable si crece
- Fácil de desplegar con CI/CD

### Decisión

Usar Google Cloud Run para backend y frontend.

### Justificación

1. **Pay-per-use**: Solo pagamos por requests procesados
2. **Scale to zero**: Sin costo cuando no hay tráfico
3. **Contenedores**: Portabilidad con Docker
4. **Integración GCP**: Infraestructura existente nubemsystems

### Consecuencias

- (+) Costo mínimo para POC
- (+) Escalado automático
- (-) Cold starts (mitigable con min instances)
- (-) Vendor lock-in moderado

---

## ADR-008: Almacenamiento de imágenes local (POC) → Cloud Storage (prod)

**Estado:** Aceptada
**Fecha:** 2026-02-02

### Contexto

Las imágenes subidas necesitan almacenamiento persistente.

### Decisión

- **Desarrollo**: Sistema de archivos local (`./data/uploads/`)
- **Producción**: Google Cloud Storage

### Justificación

1. **Desarrollo simple**: Sin configuración de cloud storage
2. **Producción escalable**: Cloud Storage es económico y duradero
3. **Abstracción en service**: Upload service abstrae el storage backend

### Consecuencias

- (+) Desarrollo sin dependencias cloud
- (+) Producción con storage ilimitado y CDN
- (-) Diferente comportamiento dev/prod
- (-) URLs de imágenes diferentes por entorno

---

## Historial de Cambios

| Fecha | ADR | Descripción |
|-------|-----|-------------|
| 2026-02-02 | 001-008 | Decisiones iniciales del proyecto |
