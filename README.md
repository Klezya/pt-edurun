# Edurun

Plataforma educativa para la ejecución y evaluación automatizada de código Python, integrada con sistemas LMS (Learning Management Systems) mediante el protocolo LTI 1.3.

## 📋 Descripción

Edurun es una herramienta diseñada para docentes y estudiantes que permite:

- **Docentes**: Crear tareas y evaluaciones con tests automatizados usando Pytest
- **Estudiantes**: Escribir y ejecutar código Python directamente en el navegador
- **Evaluación automática**: Calificación instantánea basada en tests unitarios
- **Integración LMS**: Compatible con Canvas, Moodle y otras plataformas LTI 1.3

## 🏗️ Arquitectura

El proyecto está compuesto por tres componentes principales:

```
pt-edurun/
├── frontend/          # Aplicación Vue.js 3 + TypeScript
├── backend/           # API FastAPI + Python
└── ltijs/             # Servidor LTI 1.3 (basado en ltijs)
```

### Frontend
- **Framework**: Vue.js 3 con Composition API
- **Lenguaje**: TypeScript
- **Estilos**: Tailwind CSS
- **Editor de código**: CodeMirror 6
- **Build tool**: Vite

### Backend
- **Framework**: FastAPI
- **Base de datos**: Supabase (PostgreSQL)
- **Ejecución de código**: AWS Lambda / Docker
- **Testing**: Pytest

### LTI Provider
- **Librería**: [ltijs](https://github.com/Cvmcosta/ltijs) - Proyecto open source de [@Cvmcosta](https://github.com/Cvmcosta)
- **Base de datos**: MongoDB
- **Protocolo**: LTI 1.3 Advantage

## 🚀 Instalación

### Requisitos previos
- Node.js 18+
- Python 3.11+
- MongoDB
- Docker (opcional, para ejecución local de código)

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
# Configurar variables de entorno
npm run dev
```

### Backend

```bash
cd backend/app
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows
pip install -r ../requirements.txt
cp example.env .env
# Configurar variables de entorno
uvicorn main:app --reload
```

### LTI Server

```bash
cd ltijs
npm install
cp example.env .env
# Configurar variables de entorno
npm start
```

## ⚙️ Variables de Entorno

### Frontend (`.env`)
```env
VITE_API_BASE_URL=http://localhost:8000
VITE_LTI_BASE_URL=http://localhost:3000
```

### Backend (`.env`)
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
FRONTEND_URL=http://localhost:5173
LAMBDA_API_URL=your_lambda_api_url
```

### LTI Server (`.env`)
```env
LTI_KEY=your_lti_secret_key
MONGO_URL=mongodb://localhost:27017/ltidb
FRONTEND_URL=http://localhost:5173
SELF_URL=http://localhost:3000
PORT=3000
```

## 📚 Funcionalidades

### Para Docentes
- Crear y gestionar tareas de práctica
- Crear evaluaciones con calificación automática
- Escribir tests con Pytest para validar código
- Revisar entregas de estudiantes
- Integración con Deep Linking para vincular actividades al LMS

### Para Estudiantes
- Editor de código Python integrado
- Ejecución de código en tiempo real
- Feedback inmediato con resultados de tests
- Visualización de errores y sugerencias

## 🔗 Integración LTI

El proyecto implementa LTI 1.3 Advantage con soporte para:
- **Core Launch**: Inicio de sesión desde el LMS
- **Deep Linking**: Selección de recursos desde el LMS
- **Assignment and Grade Services**: Envío automático de calificaciones

### Plataformas compatibles
- Moodle
- Canvas LMS
- Cualquier plataforma compatible con LTI 1.3

## 🛠️ Desarrollo

### Estructura del Frontend
```
frontend/src/
├── core/              # Configuraciones globales
├── features/          # Módulos por funcionalidad
│   ├── assestment/    # Tareas y evaluaciones
│   ├── lti_protocol/  # Servicios LTI
│   └── platform_management/
└── router/            # Rutas de la aplicación
```

### Estructura del Backend
```
backend/app/
├── configs/           # Configuraciones (pytest_plugin)
├── functions/         # Lógica de negocio
├── models/            # Modelos Pydantic
└── router/            # Endpoints API
```

## 📄 Licencia

Copyright © 2025 Klezya. Todos los derechos reservados.

Este software es propietario y confidencial. Queda estrictamente prohibido copiar, modificar, fusionar, publicar, distribuir, sublicenciar y/o vender copias del software sin la autorización expresa y por escrito del autor.

Para consultas sobre licencias comerciales, contactar al autor.

> **Nota**: Este proyecto utiliza [ltijs](https://github.com/Cvmcosta/ltijs) (MIT License) como dependencia para la implementación del protocolo LTI.

## 🙏 Agradecimientos

- [ltijs](https://github.com/Cvmcosta/ltijs) por [@Cvmcosta](https://github.com/Cvmcosta) - Librería LTI 1.3 para Node.js
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web para Python
- [Vue.js](https://vuejs.org/) - Framework JavaScript progresivo
- [CodeMirror](https://codemirror.net/) - Editor de código para el navegador

---

© 2025 Edurun. Todos los derechos reservados.