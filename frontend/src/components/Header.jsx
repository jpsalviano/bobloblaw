import React from 'react';
import { Jumbotron, Container } from 'react-bootstrap';

export default function Header({ titulo, subtitulo }) {
  return (
    <Jumbotron>
      <Container>
        <h1>{titulo}</h1>
        <p>{subtitulo}</p>
      </Container>
    </Jumbotron>
  );
}