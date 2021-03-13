/* eslint-disable react/no-array-index-key */
/* eslint-disable guard-for-in */
/* eslint-disable no-restricted-syntax */
import React, { useState } from 'react';
import { Form, Button, Container, Alert } from 'react-bootstrap';
import { registerUser } from './services';
import Header from './components/Header';

export default function Cadastrar() {
  const [usuario, setUsuario] = useState('');
  const [email, setEmail] = useState('');
  const [confirmaEmail, setConfirmaEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [confirmaSenha, setConfirmaSenha] = useState('');
  const [errors, setErrors] = useState([]);

  const limpaForm = () => {
    setUsuario('');
    setEmail('');
    setConfirmaEmail('');
    setSenha('');
    setConfirmaSenha('');
  };

  const enviaCadastro = async (e) => {
    e.preventDefault();
    const data = { username: usuario, email, password: senha, password2: confirmaSenha };
  
    if (email !== confirmaEmail) {
      setErrors(['Emails não coincidem']);
      return limpaForm();
    }

  try {
    const requisicao = await registerUser(data);
    if (requisicao.status === 201) {
      console.log("usuário registrado na API");
    }
  } catch (error) {
    const errorsCadastro = [];
    for (const key in error.response.data) {
      error.response.data[key].map((err) => errorsCadastro.push(err));
    }
    setErrors(errorsCadastro);
  }

    return limpaForm();
  }

  return (
    <>
      <Header titulo="Cadastrar" subtitulo="Preencha os dados para cadastrar seu usuário."/>
      <Container>
        <Form onSubmit={enviaCadastro}>
          <Form.Group>
            <Form.Label htmlFor="campoUsuario">Usuário
            </Form.Label>
            <Form.Control
                id="campoUsuario"
                value={usuario}
                placeholder="Digite o nome de usuário"
                onChange={(e) => setUsuario(e.target.value)}
            />
          </Form.Group>
          <Form.Group>
            <Form.Label htmlFor="campoEmail">Email</Form.Label>
            <Form.Control
              id="campoEmail"
              value={email}
              type="email"
              placeholder="Digite o seu email"
              onChange={(e) => setEmail(e.target.value)}
            />
          </Form.Group>
          <Form.Group>
            <Form.Label htmlFor="campoConfirmaEmail">Confirmação de email</Form.Label>
            <Form.Control
              id="campoConfirmaEmail"
              value={confirmaEmail}
              type="email"
              placeholder="Confirme o seu email"
              onChange={(e) => setConfirmaEmail(e.target.value)}
            />
          </Form.Group>
          <Form.Group>
            <Form.Label htmlFor="campoSenha">Senha</Form.Label>
            <Form.Control
              id="campoSenha"
              value={senha}
              type="password"
              placeholder="Digite a sua senha"
              onChange={(e) => setSenha(e.target.value)}
            />
          </Form.Group>
          <Form.Group>
            <Form.Label htmlFor="campoConfirmaSenha">Confirmação de senha</Form.Label>
            <Form.Control
              id="campoConfirmaSenha"
              value={confirmaSenha}
              type="password"
              placeholder="Confirme a sua senha"
              onChange={(e) => setConfirmaSenha(e.target.value)}
            />
          </Form.Group>
          <div className="d-flex" style={{ flexDirection: 'row-reverse' }}>
            <Button type="submit" className="ml-1">
              Cadastrar
            </Button>
            <Button variant="secondary" href="/">
              Voltar
            </Button>
          </div>
        </Form>
        { errors !== [] &&
          errors.map((error, index) => (
            <Alert
              onClose={() => setErrors([])}
              key={index}
              variant="danger"
              className="mt-2"
              dismissible
            >
              {error}
            </Alert>
            ))}
      </Container>
    </>
  );
}