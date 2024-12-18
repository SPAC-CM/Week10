import React from 'react'
import { useState } from "react"

function CreateAlignment() {
	const [alignmentName, setAlignmentName] = useState("")
	const [alignmentNameError, setAlignmentNameError] = useState("")
	const [postError, setPostError] = useState("")

	const onButtonClick = async () =>{
    		setAlignmentNameError("")
		setPostError("")
		if("" === alignmentName){
			setAlignmentNameError("Please enter the name of the alignment")
			return
		}
		
		let json = {
			table_name: "alignment",
			name: alignmentName,
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
				<h2>Create an alignment</h2>
				<form>
					<div className="box">
						<input
						value={alignmentName}
						placeholder='Enter name of the alignment here'
						onChange={ev=> setAlignmentName(ev.target.value)}
						className={"box"}
						/>

						<label className='errorLabel'>{alignmentNameError}</label>
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

export default CreateAlignment
