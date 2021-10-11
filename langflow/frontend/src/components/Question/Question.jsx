import React from 'react'
import axios from 'axios'
import './question.scss'
const querystring = require('querystring');

class Question extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {
            uuid: '',
            answer_user: '',
        }

        this.handleEmailChange = this.handleEmailChange.bind(this);
        this.handleQuestionSubmit = this.handleQuestionSubmit.bind(this);
        this.handleAnswerSubmit = this.handleAnswerSubmit.bind(this);
        this.handleAnswerSubmitFirst = this.handleAnswerSubmitFirst.bind(this);
    }

    componentDidMount() {
        console.log('check');
    }

    handleQuestionSubmit() {
        const data = {
            uuid: this.state.uuid,
            answer_user: this.state.answer_user
        }
        axios.post(`http://localhost:6767/answer?uuid=${data.uuid}&second_language_phrase_answer=${data.answer_user}`, querystring.stringify(data))
            .then((response) => {
                const answer = response.data
                this.setState({ answer });
            })
            .catch((error) => {
                console.log(error);
            });
        this.setState({ isAnswer: true});
    }

    handleAnswerSubmit() {
        axios.get(`http://localhost:6767/question`)
            .then(res => {
                const question = res.data.question;
                const uuid = res.data.uuid;
                this.setState({ question, uuid});
        })
        this.setState({ isAnswer: false});
    }

    handleAnswerSubmitFirst() {
        axios.get(`http://localhost:6767/question`)
            .then(res => {
                const question = res.data.question;
                const uuid = res.data.uuid;
                this.setState({ question, uuid});
        })
    }

    handleEmailChange(event) {
        this.setState({answer_user: event.target.value});
    }

    renderQuestion() {
        const { question } = this.state
        console.log(this.state);
        return (
            <div className="vh-100">
                <div className="centered-element">
                    <h2>Translate: {question}</h2>
                    <form onSubmit={this.handleQuestionSubmit}>
                        <div className="input-group mb-3">
                            <input 
                                type="string" 
                                className="form-control" 
                                placeholder="Enter text" 
                                autoComplete="off"
                                onChange={this.handleEmailChange}
                            />
                            <div className="input-group-append">
                                <button className="btn btn-secondary" type="submit" onClick={this.handleQuestionSubmit}>Enter</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        );
    }

    renderAnswer() {
        // const { answer } = this.state.answer
        console.log(this.state.answer);
        return (
            <div className="vh-100">
                <div class="centered-element w-100">
                    <table class="custom-table text-white-50">
                        <tbody>
                        <tr>
                            <td class="table-header">Translate:</td>
                            <td class="table-text table-text_translate">{}</td>
                        </tr>
                        <tr>
                            <td class="table-header ">Answer:</td>
                            <td class="table-text table-text_answer">{}</td>
                        </tr>
                        <tr>
                            <td class="table-header">Correct answer:</td>
                            <td class="table-text table-text_correct-answer">{}</td>
                        </tr>
                        <tr>
                            <td class="table-header">Is equal:</td>
                            <td class="table-text table-text_correct-answer">{}</td>
                        </tr>
                        <tr>
                            <td class="table-header">Score:</td>
                            <td class="table-text table-text_correct-answer">{}</td>
                        </tr>
                        </tbody>
                    </table>
                    <form>
                        <button className="btn btn-success btn-lg" value="Next"  id="next_button" onClick={this.handleAnswerSubmit}>Next</button>
                    </form>
                </div>
            </div>
        );
    }

    render() {
        return !this.state.isAnswer ? this.renderQuestion() : this.renderAnswer()
    }
}


export default Question;