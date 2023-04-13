import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './assets/Style/App.css'

function App() {
  const [paquetes, setPaquetes] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const response = await axios.get('http://localhost:3000/paquetes');
      setPaquetes(response.data);
    }
    fetchData();
  }, []);

  return (
    <div>
      <h1 className='text-center text-white'>Reportando </h1>
      <br/>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>IP de origen</th>
            <th>IP de destino</th>
            <th>URL</th>
            <th>Usuario y contraseña</th>
         
          </tr>
        </thead>
        <tbody>
          {paquetes.map((paquete) => (
            <tr key={paquete.id}>
              <td className='text-white'>{paquete.id}</td>
              <td className='text-white'>{paquete.ip_src}</td>
              <td className='text-white'>{paquete.ip_dst}</td>
              <td className='text-white'>{paquete.url}</td>
              <td className='text-white'>{paquete.data || '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
