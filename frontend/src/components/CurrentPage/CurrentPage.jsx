import React from 'react'
import { Router, Switch, Route, Redirect } from 'react-router-dom'
import { connect } from 'react-redux';
import Question from '../Question/Question'
import HomePage from '../HomePage/HomePage'
import RegisterPage from '../RegisterPage/RegisterPage'
import LoginPage from '../LoginPage/LoginPage'

import { history } from '../helpers/history';
import { alertActions } from '../actions/alert.action';

import './currentpage.scss'

class CurrentPage extends React.Component {
    constructor(props) {
        super(props);

        history.listen((location, action) => {
            // clear alert on location change
            this.props.clearAlerts();
        });
    }

    render() {
        const { alert } = this.props;
        return (
            <div className="h-100 text-center text-white bg-dark base-container">
                {alert.message && <div className={`alert ${alert.type}`}>{alert.message}</div>}
                <Router history={history}>
                    <Switch>
                        <Route path="/home" component={HomePage} />
                        <Route path="/question" component={Question} />
                        <Route path="/register" component={RegisterPage} />
                        <Route path="/login" component={LoginPage} />
                        <Redirect from='/' to='/home'/>
                    </Switch>
                </Router>
            </div>
        );
    }
};

function mapState(state) {
    const { alert } = state;
    return { alert };
}

const actionCreators = {
    clearAlerts: alertActions.clear
};

export default connect(mapState, actionCreators)(CurrentPage)