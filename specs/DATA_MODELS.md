# Data Models - NubemFeast

> Especificación completa de entidades y schemas
> Versión: 1.0.0

---

## 1. Entidades de Base de Datos (SQLModel)

### 1.1 Scan

Representa un escaneo/recorrido de un espacio.

```python
class Scan(SQLModel, table=True):
    __tablename__ = "scans"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    location: str | None = Field(default=None, max_length=500)
    status: ScanStatus = Field(default=ScanStatus.PENDING)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    images: list["Image"] = Relationship(back_populates="scan")
    analysis_result: "AnalysisResult" | None = Relationship(back_populates="scan")
    guide: "Guide" | None = Relationship(back_populates="scan")
```

**Índices:**
- `ix_scans_status` en `status`
- `ix_scans_created_at` en `created_at`

---

### 1.2 Image

Imagen individual dentro de un scan.

```python
class Image(SQLModel, table=True):
    __tablename__ = "images"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    scan_id: uuid.UUID = Field(foreign_key="scans.id")

    filename: str = Field(max_length=255)
    original_filename: str = Field(max_length=255)
    file_path: str = Field(max_length=500)
    file_size: int  # bytes
    mime_type: str = Field(max_length=50)

    # Metadatos de imagen
    width: int | None = None
    height: int | None = None

    # Orden en el recorrido
    sequence_order: int = Field(default=0)

    # Descripción opcional del usuario
    user_description: str | None = Field(default=None, max_length=500)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    scan: Scan = Relationship(back_populates="images")
    barriers: list["Barrier"] = Relationship(back_populates="image")
```

**Índices:**
- `ix_images_scan_id` en `scan_id`
- Unique constraint en `(scan_id, sequence_order)`

---

### 1.3 AnalysisResult

Resultado consolidado del análisis de accesibilidad de un scan.

```python
class AnalysisResult(SQLModel, table=True):
    __tablename__ = "analysis_results"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    scan_id: uuid.UUID = Field(foreign_key="scans.id", unique=True)

    # Estado del análisis
    status: AnalysisStatus = Field(default=AnalysisStatus.PENDING)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    error_message: str | None = None

    # Métricas globales
    total_images_analyzed: int = Field(default=0)
    total_barriers_found: int = Field(default=0)
    accessibility_score: float | None = None  # 0-100

    # Modelo de mundo serializado (JSON del grafo NetworkX)
    world_model_json: str | None = None

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    scan: Scan = Relationship(back_populates="analysis_result")
```

---

### 1.4 Barrier

Barrera de accesibilidad detectada en una imagen.

```python
class Barrier(SQLModel, table=True):
    __tablename__ = "barriers"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    image_id: uuid.UUID = Field(foreign_key="images.id")

    # Tipo y severidad
    barrier_type: BarrierType
    severity: BarrierSeverity

    # Descripción generada por Vision AI
    description: str = Field(max_length=1000)

    # Posición en la imagen (coordenadas normalizadas 0-1)
    bbox_x: float | None = None
    bbox_y: float | None = None
    bbox_width: float | None = None
    bbox_height: float | None = None

    # Medidas estimadas (en cm)
    estimated_width_cm: float | None = None
    estimated_height_cm: float | None = None
    estimated_depth_cm: float | None = None

    # Recomendación
    recommendation: str | None = Field(default=None, max_length=500)

    # Confidence de la detección (0-1)
    confidence: float = Field(default=0.0)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    image: Image = Relationship(back_populates="barriers")
```

**Índices:**
- `ix_barriers_image_id` en `image_id`
- `ix_barriers_barrier_type` en `barrier_type`
- `ix_barriers_severity` en `severity`

---

### 1.5 Guide

Guía de navegación generada para un scan.

```python
class Guide(SQLModel, table=True):
    __tablename__ = "guides"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    scan_id: uuid.UUID = Field(foreign_key="scans.id", unique=True)

    # Perfil de silla de ruedas usado
    wheelchair_profile_id: uuid.UUID | None = Field(
        default=None,
        foreign_key="wheelchair_profiles.id"
    )

    # Contenido de la guía
    title: str = Field(max_length=255)
    summary: str = Field(max_length=2000)

    # Pasos de navegación (JSON serializado)
    navigation_steps_json: str

    # Alertas y recomendaciones
    alerts_json: str  # Lista de alertas críticas

    # Ruta recomendada (nodos del grafo)
    recommended_path_json: str | None = None

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    scan: Scan = Relationship(back_populates="guide")
    wheelchair_profile: "WheelchairProfile" | None = Relationship()
```

---

### 1.6 WheelchairProfile

Perfil de silla de ruedas para personalizar guías.

```python
class WheelchairProfile(SQLModel, table=True):
    __tablename__ = "wheelchair_profiles"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)

    # Dimensiones (en cm)
    width_cm: float  # Ancho total
    length_cm: float  # Largo total
    min_door_width_cm: float  # Ancho mínimo de puerta para pasar

    # Capacidades
    max_step_height_cm: float = Field(default=2.0)  # Altura máxima de escalón superable
    max_slope_percent: float = Field(default=8.0)  # Pendiente máxima (%)
    can_handle_gravel: bool = Field(default=False)
    can_handle_grass: bool = Field(default=False)

    # Tipo
    wheelchair_type: WheelchairType = Field(default=WheelchairType.MANUAL)

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Es perfil predeterminado del sistema
    is_default: bool = Field(default=False)
```

---

## 2. Enums

```python
from enum import Enum

class ScanStatus(str, Enum):
    PENDING = "pending"           # Creado, sin imágenes o análisis
    UPLOADING = "uploading"       # Subiendo imágenes
    READY = "ready"               # Imágenes subidas, listo para análisis
    ANALYZING = "analyzing"       # Análisis en progreso
    COMPLETED = "completed"       # Análisis completado
    FAILED = "failed"             # Error en el proceso

class AnalysisStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class BarrierType(str, Enum):
    STEP = "step"                 # Escalón
    STAIRS = "stairs"             # Escalera
    NARROW_DOOR = "narrow_door"   # Puerta estrecha
    NARROW_PASSAGE = "narrow_passage"  # Pasillo estrecho
    STEEP_RAMP = "steep_ramp"     # Rampa empinada
    UNEVEN_SURFACE = "uneven_surface"  # Superficie irregular
    OBSTACLE = "obstacle"         # Obstáculo (mueble, etc.)
    HEAVY_DOOR = "heavy_door"     # Puerta pesada
    REVOLVING_DOOR = "revolving_door"  # Puerta giratoria
    THRESHOLD = "threshold"       # Umbral/desnivel
    GRAVEL = "gravel"            # Gravilla
    GRASS = "grass"              # Césped
    SLOPE = "slope"              # Pendiente
    OTHER = "other"              # Otro

class BarrierSeverity(str, Enum):
    LOW = "low"           # Superable con precaución
    MEDIUM = "medium"     # Superable con dificultad/ayuda
    HIGH = "high"         # No superable, requiere alternativa
    CRITICAL = "critical" # Bloquea completamente el acceso

class WheelchairType(str, Enum):
    MANUAL = "manual"
    ELECTRIC = "electric"
    SPORT = "sport"
    PEDIATRIC = "pediatric"
    BARIATRIC = "bariatric"
```

---

## 3. Schemas Pydantic (Request/Response)

### 3.1 Scan Schemas

```python
# Request
class ScanCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    location: str | None = Field(default=None, max_length=500)

class ScanUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    location: str | None = Field(default=None, max_length=500)

# Response
class ScanResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    location: str | None
    status: ScanStatus
    image_count: int
    created_at: datetime
    updated_at: datetime

class ScanDetailResponse(ScanResponse):
    images: list["ImageResponse"]
    analysis_result: "AnalysisResultResponse" | None
    has_guide: bool
```

### 3.2 Image Schemas

```python
class ImageResponse(BaseModel):
    id: uuid.UUID
    filename: str
    original_filename: str
    file_size: int
    mime_type: str
    width: int | None
    height: int | None
    sequence_order: int
    user_description: str | None
    created_at: datetime
    barrier_count: int

class ImageUploadResponse(BaseModel):
    uploaded: int
    failed: int
    images: list[ImageResponse]
    errors: list[str]
```

### 3.3 Analysis Schemas

```python
class AnalysisResponse(BaseModel):
    id: uuid.UUID
    scan_id: uuid.UUID
    status: AnalysisStatus
    started_at: datetime | None
    completed_at: datetime | None
    error_message: str | None
    total_images_analyzed: int
    total_barriers_found: int
    accessibility_score: float | None

class BarrierResponse(BaseModel):
    id: uuid.UUID
    image_id: uuid.UUID
    barrier_type: BarrierType
    severity: BarrierSeverity
    description: str
    bbox_x: float | None
    bbox_y: float | None
    bbox_width: float | None
    bbox_height: float | None
    estimated_width_cm: float | None
    estimated_height_cm: float | None
    recommendation: str | None
    confidence: float
```

### 3.4 Navigation Schemas

```python
class NavigationStep(BaseModel):
    step_number: int
    image_id: uuid.UUID
    image_url: str
    title: str
    description: str
    barriers: list[BarrierResponse]
    alerts: list[str]
    recommendations: list[str]

class GuideResponse(BaseModel):
    id: uuid.UUID
    scan_id: uuid.UUID
    title: str
    summary: str
    accessibility_score: float | None
    navigation_steps: list[NavigationStep]
    critical_alerts: list[str]
    wheelchair_profile: "WheelchairProfileResponse" | None
    created_at: datetime

class WorldModelNode(BaseModel):
    id: str
    image_id: uuid.UUID
    label: str
    barriers: list[BarrierResponse]
    accessibility_score: float

class WorldModelEdge(BaseModel):
    source: str
    target: str
    traversable: bool
    difficulty: str  # easy, moderate, difficult, impassable

class WorldModelResponse(BaseModel):
    scan_id: uuid.UUID
    nodes: list[WorldModelNode]
    edges: list[WorldModelEdge]
    recommended_path: list[str] | None
```

### 3.5 Wheelchair Profile Schemas

```python
class WheelchairProfileCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    width_cm: float = Field(gt=0)
    length_cm: float = Field(gt=0)
    min_door_width_cm: float = Field(gt=0)
    max_step_height_cm: float = Field(default=2.0, ge=0)
    max_slope_percent: float = Field(default=8.0, ge=0)
    can_handle_gravel: bool = False
    can_handle_grass: bool = False
    wheelchair_type: WheelchairType = WheelchairType.MANUAL

class WheelchairProfileResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    width_cm: float
    length_cm: float
    min_door_width_cm: float
    max_step_height_cm: float
    max_slope_percent: float
    can_handle_gravel: bool
    can_handle_grass: bool
    wheelchair_type: WheelchairType
    is_default: bool
```

---

## 4. Modelo de Mundo (NetworkX)

El modelo de mundo se representa como un grafo dirigido donde:

- **Nodos**: Espacios/ubicaciones (cada imagen representa un nodo)
- **Aristas**: Conexiones entre espacios (navegabilidad)

### 4.1 Estructura del Nodo

```python
{
    "id": "node_1",
    "image_id": "uuid",
    "label": "Entrada principal",
    "space_type": "entrance",  # entrance, corridor, room, stairway, elevator, etc.
    "barriers": [...],
    "accessibility_score": 85.0,
    "features": {
        "has_ramp": true,
        "has_handrails": false,
        "lighting": "good",
        "floor_type": "tile"
    }
}
```

### 4.2 Estructura de la Arista

```python
{
    "source": "node_1",
    "target": "node_2",
    "traversable": true,
    "difficulty": "moderate",
    "barriers_in_path": [...],
    "distance_estimate": "short",  # short, medium, long
    "notes": "Puerta de 80cm, pasa justo"
}
```

---

## 5. Perfiles de Silla de Ruedas Predeterminados

| Nombre | Ancho | Largo | Min Puerta | Max Escalón | Max Pendiente |
|--------|-------|-------|------------|-------------|---------------|
| Manual Estándar | 65cm | 105cm | 75cm | 2cm | 8% |
| Eléctrica Estándar | 70cm | 120cm | 80cm | 5cm | 12% |
| Deportiva | 60cm | 90cm | 70cm | 2cm | 10% |
| Pediátrica | 55cm | 85cm | 65cm | 2cm | 8% |
| Bariátrica | 80cm | 130cm | 90cm | 3cm | 6% |

---

## Historial de Cambios

| Fecha | Versión | Descripción |
|-------|---------|-------------|
| 2026-02-02 | 1.0.0 | Versión inicial |
