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
            answer_user: '',
            is_equal: '',
            score: ''
        }

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleAnswerSubmit = this.handleAnswerSubmit.bind(this);
    }

    componentDidMount() {
        const data = JSON.parse(window.localStorage.getItem('dataUuid'));
        this.setState((state) => ({
            ...state, uuid: data.uuid
        }))
        api.post(`/question?uuid=${data.uuid}`, JSON.stringify(data.uuid))
            .then(res => {
                const question = res.data.question;
                const uuid = data.uuid;
                const quid = res.data.quid;
                this.setState({ question, uuid, quid});
        })
    }

    handleAnswerSubmit() {
        const data = {
            uuid: this.state.uuid,
            quid: this.state.quid,
            answer_user: this.state.answer_user
        }
        api.post(`/answer?uuid=${data.uuid}&quid=${data.quid}&second_language_phrase_answer=${data.answer_user}`, JSON.stringify(data))
            .then((response) => {
                const answer = response.data.answer
                const is_equal = response.data.is_equal
                const score = response.data.score
                const differences = response.data.differences
                this.setState({ answer, is_equal, score, differences });
            })
            .catch((error) => {
                console.log(error);
            });
        this.setState({ isAnswer: true});
    }

    handleInputChange(event) {
        this.setState({answer_user: event.target.value});
    }

    renderQuestion() {
        const { question } = this.state
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
        const { question, answer, answer_user, score, is_equal } = this.state
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
                            <td className="table-text table-text_answer">{answer_user}</td>
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


export default Question