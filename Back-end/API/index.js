const mysql = require('mysql2/promise');
const express = require('express');
const app = express();

const dbConfig = {
  host: 'localhost',
  user: 'root',
  password: '211228',
  database: 'sniffer2'
};

// Ruta para obtener todos los paquetes
app.get('/paquetes', async (req, res) => {
  try {
    const conn = await mysql.createConnection(dbConfig);
    const [rows] = await conn.execute('SELECT * FROM packets');
    conn.end();
    res.json(rows);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error al obtener los paquetes');
  }
});

app.listen(3000, () => {
  console.log('API en ejecución en el puerto 3000');
});