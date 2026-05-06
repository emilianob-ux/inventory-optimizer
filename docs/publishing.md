# Publishing

## GitHub Pages (ready)

Este repo usa el workflow `Docs` (`.github/workflows/docs.yml`) para publicar en GitHub Pages.

- URL publica: `https://emilianob-ux.github.io/inventory-optimizer/`
- Build type: `workflow` (GitHub Actions)
- Trigger: push a `main` o `workflow_dispatch`

## PyPI con Trusted Publisher (sin tokens)

El workflow `Publish to PyPI` (`.github/workflows/publish.yml`) ya esta preparado.

### 1) Configurar publisher en PyPI

En PyPI:

1. Login en `https://pypi.org`
2. Cuenta -> **Publishing**
3. **Add a new pending publisher**
4. Completar con:
   - Project name: `inventory-optimizer`
   - Owner: `emilianob-ux`
   - Repository name: `inventory-optimizer`
   - Workflow name: `publish.yml`
   - Environment name: `pypi`

### 2) Verificar environment en GitHub

En GitHub repo:

1. Settings -> Environments
2. Crear `pypi` (si no existe)
3. (Opcional) Required reviewers para aprobacion manual

### 3) Publicar

Opciones:

- Crear tag `v*` y push (ej. `v0.1.2`) para disparo automatico
- O ejecutar manualmente `Publish to PyPI` desde Actions

### 4) Validar

- Verificar paquete en `https://pypi.org/project/inventory-optimizer/`
- Probar instalacion:

```bash
pip install inventory-optimizer
```
