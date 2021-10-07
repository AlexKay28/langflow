import React from 'react'
import { Switch, Route, Redirect } from 'react-router-dom'
import Answer from '../Answer/Answer'
import HomePage from '../HomePage/HomePage'
import './currentpage.scss'

class CurrentPage extends React.Component {
    constructor(props) {
        super(props)
    
        this.state = {}
    }

    render() {
        return (
            <div className="h-100 text-center text-white bg-dark base-container">
                <Switch>
                    <Route path="/home" component={HomePage} />
                    <Route path="/answer" component={Answer} />
                    <Redirect from='/' to='/home'/>
                </Switch>
            </div>
        );
    }
};

export default CurrentPage;