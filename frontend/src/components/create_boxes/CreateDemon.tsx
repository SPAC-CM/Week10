import React from 'react'
import { useState } from "react"

function CreateDemon() {
	const [demonName, setDemonName] = useState("")
	const [demonLevel, setDemonLevel] = useState("")
	const [demonAlignment, setDemonAlignment] = useState("")
	const [demonRace, setDemonRace] = useState("")
	const [demonNameError, setDemonNameError] = useState("")
	const [demonLevelError, setDemonLevelError] = useState("")
	const [demonAlignmentError, setDemonAlignmentError] = useState("")
	const [demonRaceError, setDemonRaceError] = useState("")
	const [postError, setPostError] = useState("")

	const onButtonClick = async () =>{
    		setDemonNameError("")
    		setDemonLevelError("")
    		setDemonAlignmentError("")
    		setDemonRaceError("")
		setPostError("")
		if("" === demonName){
			setDemonNameError("Please enter a user name")
			return
		}
		if("" === demonLevel){
			setDemonLevelError("Please enter a level")
			return
		}

		if("" === demonAlignment){
			setDemonAlignmentError("Please enter an alignment name")
			return
		}
		if("" === demonRace){
			setDemonRaceError("Please enter a race")
			return
		}
		
		let json = {
			table_name: "demon",
			name: demonName,
			level: demonLevel,
			alignment: demonAlignment,
			race: demonRace
		}

		const response = await fetch('http://localhost:8080/add', {method: 'POST',headers: {'content-type':'application/json'}, body: JSON.stringify(json)})

		if(!response.ok){
			const content = await response.text()
			console.log(content)
			setPostError(content)
		}


	}

	return (
		<>
			<div className="create-box">
				<h2>Create a demon</h2>
				<form>
					<div className="box">
						<input
						value={demonName}
						placeholder='Enter demon name here'
						onChange={ev=> setDemonName(ev.target.value)}
						className={"box"}
						/>

						<label className='errorLabel'>{demonNameError}</label>
					</div>
					<div className="box">
						<input
						type = "number"
						value={demonLevel}
						placeholder='Enter demon level here'
						onChange={ev=> setDemonLevel(ev.target.value)}
						className={"box"}
						/>

						<label className='errorLabel'>{demonLevelError}</label>
					</div>
					<div className="box">
						<input
						type="number"
						value={demonAlignment}
						placeholder='Enter demon alignment here'
						onChange={ev=> setDemonAlignment(ev.target.value)}
						className={"box"}
						/>

						<label className='errorLabel'>{demonAlignmentError}</label>
					</div>
					<div className="box">
						<input
						type="number"
						value={demonRace}
						placeholder='Enter demon race here'
						onChange={ev=> setDemonRace(ev.target.value)}
						className={"box"}
						/>

						<label className='errorLabel'>{demonRaceError}</label>
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

export default CreateDemon
