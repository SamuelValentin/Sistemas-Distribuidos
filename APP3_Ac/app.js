import React from 'react';
import './App.css';
import axios from 'axios'
// npm start

class App extends React.Component {
  constructor() {
    super()
    this.state = {
      nome: '',
      nomecomp: '',
      data: '',
      horario: '',
      convidado: '',
      cadastro: false,
      novo: false,
      teste: true
    };
    this.eventSource = new EventSource("http://localhost:5000/stream"); // sse eu acho

    this.evento = this.evento.bind(this)
    this.evento2 = this.evento2.bind(this)
    this.CadastrarNovoUsuario = this.CadastrarNovoUsuario.bind(this)
    this.Busca = this.Busca.bind(this)
    this.cadastroAgenda = this.cadastroAgenda.bind(this)
    this.CadColega = this.CadColega.bind(this)
    this.Cancel = this.Cancel.bind(this)
    this.CancelAlert = this.CancelAlert.bind(this)
  }

  CadastrarNovoUsuario() {

    this.eventSource.addEventListener('cadastronovousuario' + this.state.nome, function (event) {
      var data = JSON.parse(event.data);
      alert(data.message)
      console.log("The server says: " + data.message);

    }, false);

    axios.post('http://localhost:5000/cadastro',
      {
        nome: this.state.nome,
      },
      {
        headers: { 'Access-Control-Allow-Origin': '*' }
      }).then((resposta) => {
        console.log(resposta)
        this.setState({
          cadastro: true
        })

      }
      )



  }
  Busca() {

    this.eventSource.addEventListener('agenda' + this.state.nome, function (event) {
      var data = JSON.parse(event.data);
      alert(data.message)
      console.log("The server says: " + data.message);

    }, false);

    axios.post('http://localhost:5000/busca',
      {
        nome: this.state.nome,
        nomecomp: this.state.nomecomp,
        data: this.state.data,
      },
      {
        headers: { 'Access-Control-Allow-Origin': '*' }
      }).then((resposta) => {
        console.log(resposta)
        this.setState({
          cadastro: true
        })

      }
      )

  }

  cadastroAgenda() {

    this.eventSource.addEventListener('cadastroag' + this.state.nome, function (event) {
      var data = JSON.parse(event.data);
      alert(data.message)
      console.log("The server says: " + data.message);

    }, false);

    axios.post('http://localhost:5000/cadastroag',
      {
        nome: this.state.nome,
        nomecomp: this.state.nomecomp,
        data: this.state.data,
        horario: this.state.horario,
        convidado: this.state.convidado,
      },
      {
        headers: { 'Access-Control-Allow-Origin': '*' }
      }).then((resposta) => {
        console.log(resposta)

      }
      )
  }

  CadColega() {

    this.eventSource.addEventListener('cadastroag' + this.state.nome, function (event) {
      var data = JSON.parse(event.data);
      alert(data.message)
      console.log("The server says: " + data.message);

    }, false);

    axios.post('http://localhost:5000/cadcog',
      {
        nome: this.state.nome,
        nomecomp: this.state.nomecomp,
        data: this.state.data,
        horario: this.state.horario,
        convidado: this.state.convidado,
      },
      {
        headers: { 'Access-Control-Allow-Origin': '*' }
      }).then((resposta) => {
        console.log(resposta)
      }
      )
  }

  Cancel() {

    this.eventSource.addEventListener('cadastroag' + this.state.nome, function (event) {
      var data = JSON.parse(event.data);
      alert(data.message)
      console.log("The server says: " + data.message);

    }, false);

    axios.post('http://localhost:5000/cancel',
      {
        nome: this.state.nome,
        nomecomp: this.state.nomecomp,
        data: this.state.data,
        horario: this.state.horario,
        convidado: this.state.convidado,
      },
      {
        headers: { 'Access-Control-Allow-Origin': '*' }
      }).then((resposta) => {
        console.log(resposta)
      }
      )
  }


  CancelAlert() {

    this.eventSource.addEventListener('cadastroag' + this.state.nome, function (event) {
      var data = JSON.parse(event.data);
      alert(data.message)
      console.log("The server says: " + data.message);

    }, false);

    axios.post('http://localhost:5000/cancelalert',
      {
        nome: this.state.nome,
        nomecomp: this.state.nomecomp,
        data: this.state.data,
        horario: this.state.horario,
        convidado: this.state.convidado,
      },
      {
        headers: { 'Access-Control-Allow-Origin': '*' }
      }).then((resposta) => {
        console.log(resposta)
      }
      )
  }


  evento() {
    this.setState({
      teste: true
    })
  }

  evento2() {
    this.setState({
      teste: false
    })
  }


  render() {
    if (!this.state.cadastro) {
      return (
        <div>
          <div className="formulario">
            <h1>Cadastrar um novo usuário</h1>
            <div>
              <label for='nome'>Nome</label>
              <input type="text" id='nome' onChange={(event) => { this.setState({ nome: event.target.value }) }} value={this.state.nome} />
            </div>
            <button onClick={this.CadastrarNovoUsuario}>Cadastrar Usuário</button>
          </div>
        </div>
      )
    }
    if (this.state.teste) {
      return (
        <div className="App">
          <h3>{this.teste}</h3>
          <h1>Hello1</h1>
          <div>
            <label>Nome do compromisso</label>
            <input type="text" id='nomecomp' onChange={(event) => { this.setState({ nomecomp: event.target.value }) }} value={this.state.origem} />
          </div>

          <div>
            <label>Data</label>
            <input type="date" id='data' onChange={(event) => { this.setState({ data: event.target.value }) }} value={this.state.dataDaCarona} />
          </div>
          <div>
            <label>horario</label>
            <input type="time" id='horario' onChange={(event) => { this.setState({ horario: event.target.value }) }} value={this.state.destino} />
          </div>
          <div>
            <label>convidados</label>
            <input type="text" id='convidados
            ' onChange={(event) => { this.setState({ convidado: event.target.value }) }} value={this.state.destino} />
          </div>
          <button onClick={this.cadastroAgenda}>cadastrar na agenda</button>
          <button onClick={this.CadColega}>Entrar na agenda do colega</button>
          <button onClick={this.Cancel}>Cancelar compromisso</button>
          <button onClick={this.CancelAlert}>Cancelar alerta</button>
          <button onClick={this.Busca}>busca</button>
          <div>
          <button onClick={this.evento2}>Sair</button>
          </div>
        </div>

      )
    }

  }
}


export default App;