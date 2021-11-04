import React from 'react'
import api from "../../utils/api";
import './question.scss'

class Question extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {
            uuid: '',
            quid: '',
            answer: '',
            user_answer: '',
            is_equal: '',
            score: ''
        }

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleAnswerSubmit = this.handleAnswerSubmit.bind(this);
    }

    componentDidMount() {
        const session_token = window.localStorage.getItem('session_token');
        this.setState((state) => ({
            ...state, session_token: session_token
        }))
    }

    handleQuestionSubmit() {
        // const session_token = window.localStorage.getItem('session_token')
        const session_token = '40b39433-f0a5-4d89-abf2-7649fdcf2e7b'
        const questionConfig = {
            first_language: window.localStorage.getItem('firstLanguage'),
            second_language: window.localStorage.getItem('secondLanguage'),
            level: window.localStorage.getItem('level'),
        }
        api.post('/question', questionConfig, { headers: { session_token: `${session_token}` } })
            .then((response) => {
                console.log(response.data);
                const { question, quid } = response.data
                window.localStorage.setItem('question', question)
                window.localStorage.setItem('quid', quid)
            })
            .catch((error) => {
                console.log(error);
            });
        this.setState({ isAnswer: false});
    }

        async handleAnswerSubmit() {
        const data = {
            quid: window.localStorage.getItem('quid'),
            user_answer: this.state.user_answer
        }
        // const session_token = window.localStorage.getItem('session_token')
        const session_token = '40b39433-f0a5-4d89-abf2-7649fdcf2e7b'
        api.patch('/answer', data, { headers: { session_token: `${session_token}`}})
            .then((response) => {
                const question = response.data.question
                const answer = response.data.answer
                const answer_user = response.data.answer_user
                const is_equal = response.data.is_equal
                const score = response.data.score
                const differences = response.data.differences
                this.setState({ question, answer, answer_user, is_equal, score, differences });
            })
            .catch((error) => {
                console.log(error);
            });
        this.setState({ isAnswer: true});
    }

    handleInputChange(event) {
        this.setState({user_answer: event.target.value});
    }

    renderQuestion() {
        const question = window.localStorage.getItem('question');
        return (
            <div className="vh-100">
                <div className="centered-element">
                    <h2>Translate: {question}</h2>
                    <form onSubmit={this.handleAnswerSubmit}>
                        <div className="input-group mb-3">
                            <input 
                                type="string" 
                                className="form-control" 
                                placeholder="Enter text" 
                                autoComplete="off"
                                onChange={this.handleInputChange}
                            />
                            <div className="input-group-append">
                                <button className="btn btn-secondary" type="submit" onClick={this.handleAnswerSubmit}>Enter</button>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        );
    }

    renderAnswer() {
        const { question, answer, user_answer, score, is_equal } = this.state
        return (
            <div className="vh-100">
                <div className="centered-element w-100">
                    <table className="custom-table text-white-50">
                        <tbody>
                        <tr>
                            <td className="table-header">Translate:</td>
                            <td className="table-text table-text_translate">{question}</td>
                        </tr>
                        <tr>
                            <td className="table-header ">Answer:</td>
                            <td className="table-text table-text_answer">{user_answer}</td>
                        </tr>
                        <tr>
                            <td className="table-header">Correct answer:</td>
                            <td className="table-text table-text_correct-answer">{answer}</td>
                        </tr>
                        <tr>
                            <td className="table-header">Is equal:</td>
                            <td className="table-text table-text_correct-answer">{is_equal}</td>
                        </tr>
                        <tr>
                            <td className="table-header">Score:</td>
                            <td className="table-text table-text_correct-answer">{score}</td>
                        </tr>
                        </tbody>
                    </table>
                    <form>
                        <button className="btn btn-success btn-lg" value="Next"  id="next_button" onClick={this.handleQuestionSubmit}>Next</button>
                    </form>
                </div>
            </div>
        );
    }

    render() {
        return !this.state.isAnswer ? this.renderQuestion() : this.renderAnswer()
    }
}


export default Question