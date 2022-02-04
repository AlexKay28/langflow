import './header.scss'

import { useDispatch, useSelector } from 'react-redux'
import { NavLink } from 'react-router-dom'

import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Container from 'react-bootstrap/Container'
import logo from '../../images/logo.png'

import { logout } from '../actions/auth'
import { RootState } from '../store'

const Header = (): JSX.Element => {
    const dispatch = useDispatch()

    const { isLoggedIn } = useSelector((state: RootState) => state.auth)

    const logOut = () => {
        dispatch(logout())
    }
    
    return (
        <Navbar style={{display: 'contents'}} fixed="top">
            <Container className="p-2">
                <a className='header_logo-img' href="/">
                    <img
                        src={logo}
                        alt="langflow logo"
                    />
                </a>
                <Nav className="me-auto">
                    <a className="header_logo" href="/">Langflow</a>
                </Nav>
                <Nav className="header_nav-links">
                    <NavLink className="header_nav-link" activeClassName="header_nav-link-active" to="/home">Home</NavLink>
                    <NavLink className="header_nav-link" activeClassName="header_nav-link-active" to="/ourteam">Our team</NavLink>
                    {!isLoggedIn ? 
                    <>
                        <NavLink className="header_nav-link" activeClassName="header_nav-link-active" to="/login">Sign in</NavLink>
                        <NavLink className="header_nav-link" activeClassName="header_nav-link-active" to="/registration">Sign up</NavLink>
                    </> : 
                    <NavLink className="header_nav-link" activeClassName="header_nav-link-active" to="/login"  onClick={logOut}>Logout</NavLink>}
                </Nav>
            </Container>
        </Navbar>
    )
}

export default Header