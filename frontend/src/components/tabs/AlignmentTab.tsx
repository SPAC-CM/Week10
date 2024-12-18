import React from 'react'
import { useState } from "react"
import "../../styles/CreateBox.css" 
import CreateAlignment from "../create_boxes/CreateAlignment"
import TableGen from "../TableGen"
import {useAuth} from "../../context/useAuth"

const RaceTab = () => {
	const [showAlignmentBoxState, setShowAlignmentBoxState] = useState(false)
	const {isLoggedIn} = useAuth()
	const setShowAlignmentBox = () => {
		setShowAlignmentBoxState(!showAlignmentBoxState)
	}
	return (
		<>
			<TableGen name={"alignment"}/>
			{ isLoggedIn() &&
			<div>
				<input onClick={setShowAlignmentBox}
				className={"inputButton"}
				type="button"      
				value={"Create Alignment"}
				/>
				{showAlignmentBoxState && <CreateAlignment />}
			</div>}
		</>
	)
}
export default RaceTab
