import React from 'react'
import { useState } from "react"
interface Props {
      image: string;      
    }

const ImageUpload: React.FC<Props> = ({image}) => {
	return (
		<>
			<img src ={image} alt='icons' />
		</>
	)
}

export default ImageUpload
