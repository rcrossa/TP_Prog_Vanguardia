# Markmap Vendor (Offline)

Este directorio contiene las dependencias JavaScript necesarias para renderizar el mapa mental (Markmap) sin depender de CDNs.

## Estructura

- `d3.min.js`
- `markmap-view.min.js`
- `markmap-lib.min.js`

## Cómo obtener/actualizar

Use el script:

```bash
./scripts/fetch_markmap_vendor.sh
```

Requisitos: `curl` o `wget`.

## Integración

Las plantillas deben referenciar estos archivos así:

```html
<script src="/static/js/vendor/markmap/d3.min.js"></script>
<script src="/static/js/vendor/markmap/markmap-view.min.js"></script>
<script src="/static/js/vendor/markmap/markmap-lib.min.js"></script>
```

Mantenga las versiones alineadas en el script para reproducibilidad.
