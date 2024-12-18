import {UserProfile} from "../models/User"
import {useNavigate} from "react-router-dom"
import React, {createContext, useEffect ,useState} from "react"

type UserContextType = {
	user: UserProfile | null;
	token: string | null; 
	loginUser: (username:string, password:string) => void;
	logout: () => void;
	isLoggedIn: () => boolean;
}

type Props = { children: React.ReactNode};

const UserContext = createContext<UserContextType>({} as UserContextType);

export const UserProvider = ({children}: Props) => {
	const navigate = useNavigate();
	const [token, setToken] = useState<string | null>(null)
	const [user,setUser] = useState<UserProfile | null>(null)
	const [isReady, setIsReady] = useState(false);

	useEffect(() =>{
		const user = sessionStorage.getItem("user");
		const token = sessionStorage.getItem("token");
		if(user && token){
			setUser(JSON.parse(user));
			setToken(token);
		}
		setIsReady(true)
	}, [])

	const loginUser = async (username: string, password: string) => {
		let json = {
			user: username,
			password: password
		}

		const response = await fetch('http://localhost:8080/login', {method: 'POST',headers: {'content-type':'application/json'}, body: JSON.stringify(json)})
		if(response.ok){
			const content = await response.text()
			const userObj = {
				userName: username,
			}
			sessionStorage.setItem("user",JSON.stringify(userObj))
			sessionStorage.setItem("token",content)
			setToken(content)
			setUser(userObj!)
			navigate("/")
		}

	}

	const isLoggedIn = () => {
		console.log(user)
		return !!user;
	}

	const logout = () => {
		sessionStorage.removeItem("token")
		sessionStorage.removeItem("user")
		setUser(null)
		setToken(null)
		navigate("/")
	}

	return(
		<UserContext.Provider value={{ loginUser, user, token, logout, isLoggedIn}}>{isReady ? children : null} </UserContext.Provider>
	)
}

export const useAuth = () => React.useContext(UserContext)
