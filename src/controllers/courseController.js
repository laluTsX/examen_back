const db = require('../db');

// Obtener cursos + Filtros (Punto 2)
exports.getAll = async (req, res) => {
    try {
        const { categoria, fecha_inicio, fecha_fin } = req.query;
        let sql = "SELECT * FROM cursos WHERE 1=1";
        const params = [];

        if (categoria) {
            sql += " AND categoria_id = ?";
            params.push(categoria);
        }
        if (fecha_inicio && fecha_fin) {
            sql += " AND fecha_creacion BETWEEN ? AND ?";
            params.push(fecha_inicio, fecha_fin);
        }

        const [rows] = await db.query(sql, params);
        res.json(rows);
    } catch (err) { res.status(500).json({ error: err.message }); }
};

// Crear curso
exports.create = async (req, res) => {
    try {
        const { nombre, descripcion, categoria_id, precio, fecha_creacion } = req.body;
        const [result] = await db.query(
            "INSERT INTO cursos (nombre, descripcion, categoria_id, precio, fecha_creacion) VALUES (?, ?, ?, ?, ?)",
            [nombre, descripcion, categoria_id, precio, fecha_creacion]
        );
        res.status(201).json({ id: result.insertId, message: "Curso creado" });
    } catch (err) { res.status(500).json({ error: err.message }); }
};

// Actualizar curso
exports.update = async (req, res) => {
    try {
        const { id } = req.params;
        await db.query("UPDATE cursos SET ? WHERE id = ?", [req.body, id]);
        res.json({ message: "Curso actualizado" });
    } catch (err) { res.status(500).json({ error: err.message }); }
};

// Eliminar curso
exports.delete = async (req, res) => {
    try {
        await db.query("DELETE FROM cursos WHERE id = ?", [req.params.id]);
        res.status(204).send();
    } catch (err) { res.status(500).json({ error: err.message }); }
};

// Crear Categoría 
exports.createCategory = async (req, res) => {
    try {
        const { nombre } = req.body;
        await db.query("INSERT INTO categorias (nombre) VALUES (?)", [nombre]);
        res.status(201).json({ message: "Categoría creada" });
    } catch (err) { res.status(500).json({ error: err.message }); }
};