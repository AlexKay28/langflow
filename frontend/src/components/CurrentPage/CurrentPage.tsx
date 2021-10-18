import { Switch, Route, Redirect } from 'react-router-dom'
import Question from '../Question/Question'
import HomePage from '../HomePage/HomePage'
import './currentpage.scss'

const CurrentPage = (): JSX.Element => {
    return (
        <div className="h-100 text-center text-white bg-dark base-container">
            <Switch>
                <Route path="/home" component={HomePage} />
                <Route path="/question" component={Question} />
                <Redirect from='/' to='/home'/>
            </Switch>
        </div>
    );
};

export default CurrentPage