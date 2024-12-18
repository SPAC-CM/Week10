import React from 'react'
import { useState } from "react"
import "../../styles/CreateBox.css" 
import CreateDemon from "../create_boxes/CreateDemon"
import ClipboardImage from "../ImageClipboard"
import DemonTableGen from "../DemonTable"
import {useAuth} from "../../context/useAuth"


const DemonTab = () => {
	const [showDemonBoxState, setShowDemonBoxState] = useState(false)
	const [showImageUploadBoxState, setShowImageUploadBoxState] = useState(false)
	
	const {isLoggedIn} = useAuth()
	const setShowDemonBox = () => {
		setShowDemonBoxState(!showDemonBoxState)
		setShowImageUploadBoxState(false)
	}
	
	const setShowImageUploadBox = () => {
		setShowImageUploadBoxState(!showImageUploadBoxState)
		setShowDemonBoxState(false)
	}

	var [toggle,settoggle] = React.useState(0.5)

	return (
		<>
			<DemonTableGen/>
			{isLoggedIn() &&
				<div>
					<div>
						<input onClick={setShowDemonBox}
						className={"inputButton"}
						type="button"      
						value={"Create Demon"}
						/>
						{showDemonBoxState && <CreateDemon />}
					</div>
					<div>
						<input onClick={setShowImageUploadBox}
						className={"inputButton"}
						type="button"      
						value={"Upload Image"}
						/>
						{showImageUploadBoxState && <div className="shouldBlur"><ClipboardImage  /></div>}
					</div>
				</div>
			}
		</>
	)
}
export default DemonTab
