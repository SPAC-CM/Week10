import React from 'react'
import { useState } from "react"
function ClipboardImage() {
	const [imageSrc, setImageSrc] = useState('');
	const [demonId, setDemonId] = useState('');
	const [demonIdError, setDemonIdError] = useState('');
	const imageUrlToBase64 = async (url:string) => {
		const response = await fetch(url);
		const blob = await response.blob();
		return new Promise((onSuccess, onError) => {
			try {
				const reader = new FileReader() ;
				reader.onload = function(){ onSuccess(this.result) } ;
				reader.readAsDataURL(blob);
			} catch(e) {
				onError(e);
			}
		});
	};
	const handlePaste = async (event: React.ClipboardEvent) => {
		try {
			if (!navigator.clipboard) {
				console.error("Clipboard API not available");
				return;
			}
		const clipboardItems = await navigator.clipboard.read();
		for (const clipboardItem of clipboardItems) {
			const imageTypes = clipboardItem.types.find(type => type.startsWith('image/'));
			if (imageTypes) {
				const val = await clipboardItem.getType(imageTypes);
				const url = URL.createObjectURL(val);
				setImageSrc(url);
				break; // Assuming we need the first image
			}
		}
		} catch (err) {
			console.error("Failed to read clipboard:", err);
		}
	}

	const onButtonClick = async () => {
		if("" === imageSrc){
			setDemonIdError("You must paste an image ya goose")
			return
		}
		const data = await imageUrlToBase64(imageSrc)
		if("" === demonId){
			setDemonIdError("You must provide an id for the demon")
		}

		let json = {
			id:demonId,
			data : data
		}
		const response = await fetch('http://localhost:8080/image', {method: 'POST',headers: {'content-type':'application/json'}, body: JSON.stringify(json)})

		if(!response.ok){
			const content = await response.text()
			console.log(content)
		}
	}


	return (
		<>
			<div className="create-box">
				<h2>Upload demon image</h2>
				<form>
					<div className="box">
						<input
						value={demonId}
						placeholder='Enter demon id here'
						onChange={ev=> setDemonId(ev.target.value)}
						className={"box"}
						/>

						<label className='errorLabel'>{demonIdError}</label>
						<input placeholder="Paste image here" onPaste={handlePaste} />
					</div>
					{imageSrc && <img src={imageSrc} alt="Pasted" />}
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

export default ClipboardImage
