import React, { useState } from 'react';
import { Form, Button, Container } from 'react-bootstrap';
import { registerUser } from './services';
import Header from './components/Header';

export default function Cadastrar() {
  const [usuario, setUsuario] = useState('');
  const [email, setEmail] = useState('');
  const [confirmaEmail, setConfirmaEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [confirmaSenha, setConfirmaSenha] = useState('');

/*  const limpaForm = () => {
    setUsuario('');
    setEmail('');
    setConfirmaEmail('');
    setSenha('');
    setConfirmaSenha('');
  };*/

  const enviaCadastro = () => {
    return console.log("cadastro enviado");
  }

  return (
    <>
      <Header titulo="Cadastrar" subtitulo="Preencha os dados para cadastrar seu usuário."/>
      <Container>
        <Form onSubmit={enviaCadastro()}>
          <Form.Group>
            <Form.Label>Usuário
            <Form.Control
                value={usuario}
                placeholder="Digite o nome de usuário"
                onChange={(e) => setUsuario(e.target.value)}
            />
            </Form.Label>
          </Form.Group>
          <Form.Group>
            <Form.Label>Email
            <Form.Control
              value={email}
              type="email"
              placeholder="Digite o seu email"
              onChange={(e) => setEmail(e.target.value)}
            />
            </Form.Label>
          </Form.Group>
          <Form.Group>
            <Form.Label>Confirmação de email
            <Form.Control
              value={confirmaEmail}
              type="email"
              placeholder="Confirme o seu email"
              onChange={(e) => setConfirmaEmail(e.target.value)}
            />
            </Form.Label>
          </Form.Group>
          <Form.Group>
            <Form.Label>Senha
            <Form.Control
              value={senha}
              type="password"
              placeholder="Digite a sua senha"
              onChange={(e) => setSenha(e.target.value)}
            />
            </Form.Label>
          </Form.Group>
          <Form.Group>
            <Form.Label>Confirmação de senha
            <Form.Control
              value={confirmaSenha}
              type="password"
              placeholder="Confirme a sua senha"
              onChange={(e) => setConfirmaSenha(e.target.value)}
            />
            </Form.Label>
          </Form.Group>
          <Button type="submit">
            Cadastrar
          </Button>
          <Button variant="secondary" href="/">
            Voltar
          </Button>
        </Form>
      </Container>
    </>
    );
}