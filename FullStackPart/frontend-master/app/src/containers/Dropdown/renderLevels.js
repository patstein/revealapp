import React from 'react'
import "./index.css";
export const renderLevel = (level, onLevel, option) => {
        return (
            <div key={option.id}
                 onClick={() => onLevel(option)}
                 className={level.id === option.id ? "dropdown-cell-selected" : "dropdown-cell"}
                 style={{backgroundColor: option.color}}>{option.name}</div>
        )
    };

export const selectedLevel = (levelOption, levelSelected, onLevelSelected, tag) => {
        return (
            Object.keys(levelOption).length > 0
            ? <div className="dropdown-colum">
                  {levelSelected.name ? <p style={{fontSize: '10px'}}>{tag}: {levelSelected.name.substr(0, 9)}...</p> : null}
                  {levelOption.map(option => renderLevel(levelSelected, onLevelSelected, option))}
            </div>
            : null
        )
};

// return (
//           <div className="dropdown-colum">
//               {this.state.level1Selected.name ? <p style={{fontSize: '10px'}}>Tag1: {this.state.level1Selected.name.substr(0, 9)}...</p> : null}
//               {level1Tags.map(option => renderLevel(this.state.level1Selected, this.onLevel1Selected, option))}
//           </div>
//         )