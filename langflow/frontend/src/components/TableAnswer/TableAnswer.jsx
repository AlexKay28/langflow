import React from 'react';

class TableAnswer extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {}
        this.handleAnswerSubmit = props.handleAnswerSubmit

    }    

    render() {
        return (
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
                <form>
                    <button className="btn btn-success btn-lg" value="Next"  id="next_button" onClick={this.handleAnswerSubmit}>Next</button>
                </form>
            </table>
        )
    }
};

export default TableAnswer;