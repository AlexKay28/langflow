import React from 'react'
import axios from 'axios'
import './answer.scss'

class Answer extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {
            uuid: '',
            answer_user: ''
        }

        this.handleEmailChange = this.handleEmailChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    componentDidMount() {
        axios.get(`http://localhost:6767/question`)
            .then(res => {
                const question = res.data.question;
                const uuid = res.data.uuid;
                this.setState({ question, uuid });
        })
    }

    handleSubmit() {
        const data = {
            uuid: this.state.uuid,
            answer_user: this.state.answer_user
        }
        console.log(data);
        axios.post('http://localhost:6767/answer', (data))
            .then((response) => {
                console.log(response);
            })
            .catch((error) => {
                console.log(error);
            });
    }

    handleEmailChange(event) {
        this.setState({answer_user: event.target.value});
    }

    render() {
        const { question } = this.state
        return (
            <div className="vh-100">
                <div className="centered-element">
                    <h2>Translate: {question}</h2>
                    <form onSubmit={this.handleSubmit}>
                        <input 
                            type="string" 
                            className="form-control" 
                            placeholder="Enter text" 
                            autocomplete="off"
                            onChange={this.handleEmailChange}
                        />
                    </form>
                </div>
            </div>
        );
    }
}


export default Answer;