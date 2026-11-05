# Mapa base propio de la SNGR

Mapa base vectorial de todo el Ecuador para la app **Registro de afectaciones, SNGR**, con descarga por cantón o por provincia para trabajar sin señal.

- **Datos:** © colaboradores de OpenStreetMap (licencia ODbL), a través de la compilación pública de Protomaps.
- **Formato:** PMTiles (un archivo por provincia, zooms 0 a 15, y `pais.pmtiles` con zooms 0 a 9). La app los lee por rangos desde GitHub Pages y guarda en el teléfono lo que el técnico descarga.
- **Índice:** `indice.json` indica la versión vigente, la caja y el peso de cada provincia. La app siempre lee este archivo primero.

## Actualización (cada 3 a 6 meses)

1. En un computador con Python 3 e internet: `python generar_mapa.py`. Descarga la herramienta `pmtiles`, la última compilación de Protomaps y genera la carpeta `AAAAMMDD/` con los 25 archivos, y actualiza `indice.json`.
2. Publique **solo** la carpeta nueva, `indice.json`, este README y el script, en un commit sin historia (rama huérfana con `git checkout --orphan`, y `git push --force`). Así el repositorio no crece con cada actualización.
3. Los teléfonos que ya descargaron un cantón siguen usando su copia sin señal; la app les avisa que hay un mapa más reciente para volver a descargar.

## Límites de GitHub que se respetan

- Ningún archivo supera 100 MB (el mayor es Guayas, unos 45 MB).
- El sitio completo pesa unos 420 MB, por debajo del límite de 1 GB de GitHub Pages.
