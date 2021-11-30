import React from 'react'
import { Router, Switch, Route, Redirect } from 'react-router-dom'
import Question from '../Question/Question'
import HomePage from '../HomePage/HomePage'
import RegistrationPage from '../RegistrationPage/RegistrationPage'
import LoginPage from '../LoginPage/LoginPage'

import { history } from "../helpers/history"

import './currentpage.scss'

class CurrentPage extends React.Component {
    render() {
        return (
            <div className="h-100 text-center text-white bg-dark base-container">
                <Router history={history}>
                    <Switch>
                        <Route path="/home" component={HomePage} />
                        <Route path="/question" component={Question} />
                        <Route path="/registration" component={RegistrationPage} />
                        <Route path="/login" component={LoginPage} />
                        <Redirect from='/' to='/home'/>
                    </Switch>
                </Router>
            </div>
        );
    }
};

export default CurrentPage