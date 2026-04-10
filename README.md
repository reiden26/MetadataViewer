# Metadata

Una aplicación de escritorio moderna y minimalista para visualizar metadatos EXIF de imágenes, incluyendo datos de la cámara y ubicación GPS.

![Metadata Viewer](screenshot.png)

## ¿Qué hace?

- Extrae metadatos EXIF de fotografías
- Muestra información de la cámara (marca, modelo, ISO, apertura, etc.)
- Detecta y visualiza coordenadas GPS
- Abre la ubicación directamente en Google Maps
- Interfaz moderna y minimalista con sombras suaves

## Requisitos de las fotos

Para obtener **datos de ubicación**, las fotos deben cumplir:

### Requisitos técnicos:
- **GPS activado** en el celular/cámara al momento de la foto
- **Permiso de ubicación** concedido a la app de cámara
- **Esperar 10-15 segundos** tras abrir la cámara antes de tomar la foto (para que el GPS fije la posición)

### Fotos que NO tendrán ubicación:
- Capturas de pantalla
- Fotos descargadas de redes sociales (WhatsApp, Instagram, Facebook eliminan metadatos)
- Fotos enviadas por mensajería (se comprimen y pierden EXIF)
- Fotos con GPS vacío (el campo existe pero no tiene coordenadas)

## Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/reiden26/MetadataViewer.git
cd MetadataViewer
```

2. Instala las dependencias:
```bash
pip install Pillow geopy
```

3. Ejecuta la aplicación:
```bash
python ubi_fotos_gui.py
```

## Dependencias

- **Pillow** - Procesamiento de imágenes y extracción de EXIF
- **geopy** - Geocodificación inversa (coordenadas → dirección)

## Uso

1. Abre la aplicación
2. Haz clic en "Seleccionar imagen"
3. Selecciona una foto de tu cámara
4. La app mostrará automáticamente:
   - Vista previa de la imagen
   - Información del archivo
   - Datos de la cámara (si están disponibles)
   - Ubicación en mapa (si la foto tiene GPS)

## Características de la interfaz

- Diseño minimalista y moderno
- Tarjetas con sombras suaves
- Botones redondeados
- Scrollbar estilizado
- Indicador de carga animado

## Formato de salida

### Metadatos mostrados:
- Nombre del archivo
- Tamaño
- Dimensiones (px)
- Marca y modelo del dispositivo
- Fecha de captura
- Configuración de la cámara (ISO, apertura, exposición)
- Coordenadas GPS (latitud/longitud)
- Dirección aproximada
- Enlace directo a Google Maps

## Notas importantes

- **Privacidad**: Las fotos con GPS contienen tu ubicación exacta. Ten cuidado al compartirlas.
- **WhatsApp**: Las fotos enviadas por WhatsApp pierden los metadatos GPS por seguridad.
- **Señal GPS**: Si no hay suficientes satélites visibles, la cámara puede guardar el campo GPS vacío.

## Licencia

MIT License - Libre para usar y modificar.

---

Desarrollado con ❤️ para visualizar metadatos de forma sencilla.
