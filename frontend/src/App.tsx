import React from 'react';
import Home from "./pages/Home";
import Table from "./pages/Table";
import Login from "./pages/Login";
import Logout from "./pages/Logout";
import {UserProvider} from "./context/useAuth"
import { Routes, Route} from "react-router-dom"
import ProtectedRoute from "./components/ProtectedRoute"

function App() {
  return (
	  <>
	  	<UserProvider>
			<Routes>
				<Route path="/" element={<Home />} />
				<Route path="/login" element={<Login/>} />
				<Route path="/table" element={<Table/>} />
				<Route path="/logout" element={<ProtectedRoute> <Logout/></ProtectedRoute>} />
			</Routes>
		</UserProvider>
	  </>
  );
}

export default App;
