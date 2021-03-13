/* eslint-disable no-undef */
import React from 'react';
import Cadastrar from './Cadastrar';
import Login from './Login';

function App() {
  if (window.location.href === 'http://localhost:3000/cadastrar') return <Cadastrar />;
  return <Login />;
}

export default App;