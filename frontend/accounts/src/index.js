import './index.css'
import React from 'react'
import ReactDOM from 'react-dom'

import GenerateSignUpForm from './components/Signup'

/* <h1></h1> -> JSX, sintaxe inspirada em HTML que é interpretada para JavaScript, muito utilizada pelo React */
/* apesar de parecer que o React não esteja sendo usado, ele é necessário para a interpretação do JSX */

ReactDOM.render(
    <GenerateSignUpForm/>,
    document.getElementById('root')
);