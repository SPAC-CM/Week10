import React from 'react'
import { useState } from "react"

function CreateRace() {
	const [raceName, setRaceName] = useState("")
	const [raceNameError, setRaceNameError] = useState("")
	const [raceAlignment, setRaceAlignment] = useState("")
	const [raceAlignmentError, setRaceAlignmentError] = useState("")
	const [postError, setPostError] = useState("")

	const onButtonClick = async () =>{
    		setRaceNameError("")
    		setRaceAlignmentError("")
		setPostError("")
		if("" === raceName){
			setRaceNameError("Please enter the name of the race")
			return
		}

		if("" === raceAlignment){
			setRaceAlignmentError("Please enter an alignment name")
			return
		}
		
		let json = {
			table_name: "race",
			name: raceName,
			alignment: raceAlignment,
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
				<h2>Create a race</h2>
				<form>
					<div className="box">
						<input
						value={raceName}
						placeholder='Enter name of the race here'
						onChange={ev=> setRaceName(ev.target.value)}
						className={"box"}
						/>

						<label className='errorLabel'>{raceNameError}</label>
					</div>
					<div className="box">
						<input
						type="number"
						value={raceAlignment}
						placeholder='Enter demon alignment here'
						onChange={ev=> setRaceAlignment(ev.target.value)}
						className={"box"}
						/>

						<label className='errorLabel'>{raceAlignmentError}</label>
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

export default CreateRace
