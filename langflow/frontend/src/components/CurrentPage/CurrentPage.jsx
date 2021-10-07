import React from "react";
import { Switch, Route, Redirect } from "react-router-dom";
import Answer from "../Answer/Answer";
import HomePage from "../HomePage/HomePage";

class CurrentPage extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {}
    }

    render() {
        return (
            <Switch>
                <Route path="/home" component={HomePage} />
                <Route path="/answer" component={Answer} />
                <Redirect from='/' to='/home'/>
            </Switch>
        );
    }
};

export default CurrentPage;