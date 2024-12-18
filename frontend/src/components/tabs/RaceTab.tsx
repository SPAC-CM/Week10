import React from 'react'
import { useState } from "react"
import "../../styles/CreateBox.css" 
import CreateRace from "../create_boxes/CreateRace"
import TableGen from "../TableGen"
import {useAuth} from "../../context/useAuth"

const RaceTab = () => {
	const [showRaceBoxState, setShowRaceBoxState] = useState(false)
	
	const {isLoggedIn} = useAuth()
	const setShowRaceBox = () => {
		setShowRaceBoxState(!showRaceBoxState)
	}
	return (
		<>
			<TableGen name={"race"}/>
			{isLoggedIn() &&
				<div>
					<input onClick={setShowRaceBox}
					className={"inputButton"}
					type="button"      
					value={"Create Race"}
					/>
					{showRaceBoxState && <CreateRace />}
				</div>
			}
		</>
	)
}
export default RaceTab
