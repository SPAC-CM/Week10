import DemonInterface from "../interfaces/DemonInterface"
import React, { useState, useEffect } from 'react'
import {Buffer} from 'buffer'
function ImageFromDatabase({id} : DemonInterface){

	const[imageSrc, setImageSrc] = useState("")

	useEffect(() => {
		const get_image = async() => {
			const json = {
				id : id
			}
			
			const response = await fetch("http://localhost:8080/demon-pic", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(json)})

			if(response.ok){
				const content = await response.text()
				console.log(content)
				let base64_to_imgsrc = Buffer.from(content,"base64").toString()
				setImageSrc(content)
			}
		}
		get_image()
	}, [id,setImageSrc])

	return(
		<img src={"data:image/png;base64, " + imageSrc} />
	)
}
export default ImageFromDatabase
