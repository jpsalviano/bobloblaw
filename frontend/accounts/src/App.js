import React from 'react'


class App extends React.Component {
  constructor(props) {
    super(props);
    this.username = {value: ''};
    this.email = {value: ''};
    this.password1 = {value: ''};
    this.password2 = {value: ''};

    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleChange(event) {
    this.setState({value: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
  }

  render() {
    return (
      <form 
      className="sign-up-form"
      onSubmit={this.handleSubmit}
      noValidate
      >
        <label>
          Sign Up!
          <input type="text" value={this.username.value} onChange={(e) => this.setState({username: e.target.value})} />
          <input type="email" value={this.email.value} onChange={(e) => this.setState({email: e.target.value})} />
          <input type="password" value={this.password1.value} onChange={(e) => this.setState({password1: e.target.value})} />
          <input type="password" value={this.password2.value} onChange={(e) => this.setState({password2: e.target.value})} />
        </label>
        <input type="submit" value="Submit" />
      </form>
    );
  }
}

export default App;
