const express = require('express');
const swaggerUi = require('swagger-ui-express');
const cors = require('cors');
const courseRoutes = require('./routes/courseRoutes');

const app = express();
app.use(express.json());
app.use(cors());

const swaggerDocument = {
    openapi: '3.0.0',
    info: {
    title: 'API Gestión de Cursos - Examen',
    version: '1.0.0',
    description: 'API REST para gestión de cursos y categorías'
    },
    paths: {
    '/login': {
        post: {
        summary: 'Iniciar sesión',
        requestBody: {
            content: { 'application/json': { schema: { type: 'object', properties: { username: { type: 'string' }, password: { type: 'string' } } } } }
        },
        responses: { 200: { description: 'Login exitoso' } }
        }
    },
    '/courses': {
        get: {
        summary: 'Listar cursos con filtros',
        parameters: [
            { name: 'categoria', in: 'query', schema: { type: 'integer' } },
            { name: 'fecha_inicio', in: 'query', schema: { type: 'string', format: 'date' } },
            { name: 'fecha_fin', in: 'query', schema: { type: 'string', format: 'date' } }
        ],
        responses: { 200: { description: 'Lista de cursos' } }
        },
        post: {
        summary: 'Crear un curso',
        requestBody: {
            content: { 'application/json': { schema: { type: 'object', properties: { nombre: { type: 'string' }, descripcion: { type: 'string' }, categoria_id: { type: 'integer' }, precio: { type: 'number' }, fecha_creacion: { type: 'string' } } } } }
        },
        responses: { 201: { description: 'Curso creado' } }
        }
    },
    '/courses/categories': {
        post: {
        summary: 'Crear categoría',
        requestBody: {
            content: { 'application/json': { schema: { type: 'object', properties: { nombre: { type: 'string' } } } } }
        },
        responses: { 201: { description: 'Categoría creada' } }
        }
    }
    }
};

app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocument));

// --- LOGIN ---
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (username === 'admin' && password === '1234') {
    return res.json({ message: "Login exitoso", token: "jwt-123" });
    }
    res.status(401).json({ error: "Credenciales incorrectas" });
});

// --- RUTAS ---
app.use('/courses', courseRoutes);

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`✅ Servidor en puerto ${PORT}`);
    console.log(`📖 Swagger: http://localhost:${PORT}/api-docs`);
});