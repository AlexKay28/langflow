import React from 'react';

class FormQuestion extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {}
        this.handleQuestionSubmit = props.handleQuestionSubmit
        this.question = props.question
    }    

    render() {
        return (
            <>
            <h2>Translate: {this.question}</h2>
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
            </>
        )
    }
};

export default FormQuestion;