import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import Container from 'react-bootstrap/Container'
import logo from '../../images/logo.png'

const Header = (): JSX.Element => {
    return (
        <Navbar fixed="top" bg="dark" variant="dark">
            <Container className="border-bottom">
                <Navbar.Brand href="/">
                    <img
                        src={logo}
                        alt="langflow logo"
                    />
                </Navbar.Brand>
                <Nav className="me-auto">
                    <Nav.Link href="/">Home</Nav.Link>
                    <Nav.Link href="https://github.com/AlexKay28/langflow">Github</Nav.Link>
                </Nav>
            </Container>
        </Navbar>
    );
};

export default Header