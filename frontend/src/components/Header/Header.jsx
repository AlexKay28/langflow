import { useDispatch } from "react-redux"

import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Container from 'react-bootstrap/Container'
import GoPractice from '../GoPractice/GoPractice'
import logo from '../../images/logo.png'

import { logout } from "../actions/auth"

const Header = () => {
    const dispatch = useDispatch()
    const loggedIn = localStorage.getItem("user");

    const logOut = () => {
        dispatch(logout());
    };
    
    return (
        <Navbar className="d-block" fixed="top" bg="dark" variant="dark">
            <Container className="border-bottom">
                <Navbar.Brand href="/">
                    <img
                        src={logo}
                        alt="langflow logo"
                    />
                </Navbar.Brand>
                <Nav className="me-auto">
                    <Nav.Link href="/">Home</Nav.Link>
                </Nav>
                {!loggedIn ? <Nav>
                    <Nav.Link href="/login">Sign in</Nav.Link>
                    <Nav.Link href="/registration">Sign up</Nav.Link>
                </Nav> :
                <Nav>
                    <Nav.Link href="/login"  onClick={logOut}>Logout</Nav.Link>
                </Nav>}
            </Container>
            <GoPractice/>
        </Navbar>
    );
};

export default Header