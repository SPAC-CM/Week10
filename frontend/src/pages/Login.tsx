import { useState } from "react"
import React from 'react'
import {useAuth} from "../context/useAuth"
import "./../styles/Login.css" 
import { useNavigate } from "react-router-dom"
import MyNavbar from "../components/MyNavbar"

const Login = () => {
	const { loginUser} = useAuth();
	const [user, setUser] = useState("")
	const [password, setPassword] = useState("")
	
	const [userError, setUserError] = useState("")
	const [passwordError, setPasswordError] = useState("")

	const [postError, setPostError] = useState("")
	const onButtonClick = async () =>{
    		setUserError("")
    		setPasswordError("")

		if("" === user){
			setUserError("Please enter a user name")
			return
		}

		if("" === password){
			setPasswordError("Please enter a password")
			return
		}
		
		loginUser(user,password)

	}
	

	return(
		<>
		<MyNavbar />
		<div className="login-box">
			<h2>Login</h2>
			<form>
				<div className="user-box">
					<input  
					value={user}
					placeholder='Enter user name here' 
					onChange={ev=> setUser(ev.target.value)}
					className={"user-box"}      
					/>
		      
					<label className='errorLabel'>{userError}</label>
				</div>
				<div className="user-box">
					<input
					type="password"
					value={password}
					placeholder='Enter password here'
					onChange={ev=>setPassword(ev.target.value)}
					className={'user-box'}
		      
					/>
					<label className='errorLabel'>{passwordError}</label>
				</div>
				<label className='errorLabel'>{postError}</label>
				<input onClick={onButtonClick}
				className={"inputButton"}
				type="button"      
				value={"Submit"}
				/>
			</form>
		</div>     
		</>
        
	)
}

export default Login
