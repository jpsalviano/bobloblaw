/* eslint-disable react/no-array-index-key */
/* eslint-disable guard-for-in */
/* eslint-disable no-restricted-syntax */
import React, {useState } from 'react';
import { Form, Button, Container, Row, Col } from 'react-bootstrap';
import Header from './components/Header'

export default function Login() {
  return (
    <>
      <Header titulo="Login" subtitulo="Entre com seu usuário e senha." />
      <Container>
        <Row className="justify-content-center mt-5">
          <Col xs={6}>
            <LoginForm />
          </Col>
        </Row>
      </Container>
    </>
  );
}

function LoginForm() {
  const [usuario, setUsuario] = useState();
  const [senha, setSenha] = useState();
  const [validated, setValidated] = useState(false);

  const sendForm = (e) => {
    e.preventDefault();
    e.stopPropagation();
    console.log("login form sent");
  };

  return (
    <Form onSubmit={sendForm} noValidate validated={validated}>
      <Form.Group controlId="formBasicEmail">
        <Form.Label>Email</Form.Label>
        <Form.Control
          placeholder="Digite o email..."
          onChange={(e) => setUsuario(e.target.value)}
          required
          type="email"
        />
      </Form.Group>
      <Form.Group controlId="formBasicPassword">
        <Form.Label>Senha</Form.Label>
        <Form.Control
          placeholder="Digite a senha..."
          onChange={(e) => setSenha(e.target.value)}
          required
          type="password"
        />
      </Form.Group>
      <Button type="submit">
        Entrar
      </Button>
      <Button variant="secondary" className="ml-1" href="/cadastrar">
        Cadastre-se
      </Button>
    </Form>
  );
}