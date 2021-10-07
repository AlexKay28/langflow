import React from "react";

class Answer extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {}
    }

    render() {
        return (
            <div class="centered-element">
                <h2>Translate: {}</h2>
                {/* <form action="/practice" method="post">
                    <input type="string" name="second_language_phrase_answer" class="form-control" placeholder="Enter text" autocomplete="off" />
                </form> */}
            </div>
        );
    }
};

export default Answer;