import {useAuth} from "../context/useAuth"
import {useEffect} from "react"

const Logout = () => {
	const {logout} = useAuth()
	useEffect(()=>{logout()},[logout])
	return (
		<></>
	)
}
export default Logout
