# Bases de datos espaciales con Postgres, PostGIS y QGIS

Repositorio preparado como libro interactivo en Quarto, inspirado en la plantilla `GEEMAP`. Incluye portada con el logo de Fedearroz y capítulos sobre SQL, PostGIS y QGIS.

Visite la versión publicada: [https://famartinezal.github.io/libro-postgis/](https://famartinezal.github.io/libro-postgis/).

## Requisitos

- [Quarto](https://quarto.org/) 1.4+
- PostgreSQL 15 y PostGIS 3
- QGIS 3.34

## Estructura

- `_quarto.yml`: configuración del libro.
- `index.qmd`: portada y presentación.
- `fundamentos_sql.qmd` a `recursos.qmd`: capítulos propuestos.
- `assets/`: logo de Fedearroz, portada y recursos compartidos.
- `styles.css`: estilos copiados y adaptados del proyecto `GEEMAP`.

## Renderizado local

```bash
quarto render
```

El sitio generado se almacena en `_book`. Abra `_book/index.html` para navegar.

## Publicación en GitHub Pages

1. Cree un repositorio público en GitHub, por ejemplo `famartinezal/libro-postgis`.
2. Copie el contenido de `libro_postgis/` a la raíz del repositorio.
3. Ejecute `quarto publish gh-pages` o configure GitHub Actions:
   - `on: push` a `main`.
   - Acción `quarto-dev/quarto-actions/publish@v2` con `target: gh-pages`.
4. Habilite GitHub Pages en la pestaña *Settings → Pages* apuntando a la rama `gh-pages`.

## Próximas mejoras

- Agregar datos de ejemplo en `data/` (GeoPackage con veredas).
- Incluir capturas de pantalla de QGIS en los capítulos correspondientes.
- Definir scripts de validación automatizados (`BEGIN; ... ROLLBACK;`).

## Licencia

Sugerido: Creative Commons Attribution-ShareAlike 4.0.
