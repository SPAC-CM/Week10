import React, { useState} from 'react'
import "../../styles/Tabs.css"
import DemonTab from "./DemonTab"
import RaceTab from "./RaceTab"
import AlignmentTab from "./AlignmentTab"
import TableGen from "../TableGen"

const Tabs = () => {
	const [toggleState, setToggleState] =useState(1)
	const [tab, setTab] =useState(<DemonTab/>)
	const toggleTab = (index:number) => {
		setToggleState(index)
	}
	function clickHandler(event : string){
		if(event === "demon"){
			toggleTab(1)
			setTab(<DemonTab/>)
		}
		else if(event === "race"){
			toggleTab(2)
			setTab(<RaceTab/>)
		}
		else{
			toggleTab(3)
			setTab(<AlignmentTab/>)
		}
	}

	return (
		<>
			<div className="TabsContainer">
				<div className="TabsCategories">
					<button className={toggleState === 1? "Tabs active-tab" : "Tabs"} onClick = {() => clickHandler("demon")}>Demon</button>
					<button className={toggleState === 2? "Tabs active-tab" : "Tabs"} onClick = {() => clickHandler("race")}>Race</button>
					<button className={toggleState === 3? "Tabs active-tab" : "Tabs"} onClick = {() => clickHandler("alignment")}>Alignment</button>
				</div>
				<div className="OutPut">{tab}</div>
			</div>
		</>
	)
}

export default Tabs
