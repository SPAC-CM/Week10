import React from "react"
import {useAuth} from "../context/useAuth"
import {Navigate, useLocation} from "react-router-dom"

type Props = {children : React.ReactNode}

const ProtectedRoute = ({children}:Props) => {
	const location = useLocation()
	const {isLoggedIn} = useAuth()
	return isLoggedIn() ? (
		<>{children}</> ): (
			<Navigate to = "/login" state ={{from:location}} replace />
	)
}

export default ProtectedRoute
