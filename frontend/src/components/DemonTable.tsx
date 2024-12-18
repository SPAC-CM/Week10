import TableInterface from "../interfaces/TableInterface"
import ImageFromDatabase from "./ImageFetcher" 
import React, { useState, useEffect } from 'react'

const DemonTableGen = () => {

	const [header, setHeader] = useState<string[]>([])
	const [rows, setRows] = useState<string[][]>([[]])
	useEffect(() => {
		const get_data = async()  =>{
			const json = {
				table_name: "demon"
			}

			const response = await fetch("http://localhost:8080/table", {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(json)})
			if(response.ok){
				let content = await response.json()
				let head : string[] = content[0].replace("[","").replace("]","").split(",")
				let table_values : string[][] = [[]]
				for(let i = 1; i<content.length;i++) {
					var new_value : string[] = content[i].replace("[","").replace("]","").split(",")
					new_value.pop()
					table_values.push(new_value)
				}
				table_values.shift()
				setRows(table_values)
				setHeader(head)
				}

			}
		get_data()

	}, [setHeader, setRows])

	const create_demon_table = (key : string, j : number, i : number, element:string) => {
		if(j-1!==3){
			return <td id={key} key={key}>{element}</td>
		}
		else{
			return <td id={key} key={key}><ImageFromDatabase id={i+1} /> </td>
		}
	}
	let i = 0
	let final_rows = rows.map( (list,index) => { i=i+1; let j=0; return <tr>{list.map((element,index) => {let key = `demon[${i}] ${header[j]}`; j+=1; return create_demon_table(key,j,i,element)})}</tr>})

	return (
		<>
			<table>
				<thead>
					<tr>
						{header.map((element)=>{return <th id={element} key={element}>{element}</th>})}
					</tr>
				</thead>
				<tbody>
					{final_rows}
				</tbody>
			</table>
		</>
	)
}

export default DemonTableGen
