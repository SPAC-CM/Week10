import React from 'react'
import {useAuth} from "../context/useAuth"
import Container from 'react-bootstrap/Container';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';
function MyNavbar() {
	const {isLoggedIn} = useAuth()
	return (
		<header className="header">
			<Navbar bg="primary" data-bs-theme="dark">
				<Container>
					<Nav className="navbar">
						<Nav.Link style={{ textDecoration: 'none' }}className="home-item" href="/">Home</Nav.Link>
						{!isLoggedIn() ? ( 
						<Nav.Link style={{ textDecoration: 'none' }}className="login-item" href="/login">Login</Nav.Link>)
						: (
						<Nav.Link style={{ textDecoration: 'none' }}className="login-item" href="/logout">Logout</Nav.Link>)}
						<Nav.Link style={{ textDecoration: 'none' }}className="table-item" href="/table">Table</Nav.Link>
					</Nav>
				</Container>
			</Navbar>
		</header>
	);
}

export default MyNavbar;
