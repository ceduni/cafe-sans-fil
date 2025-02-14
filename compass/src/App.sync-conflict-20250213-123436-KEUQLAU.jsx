import { useState, MouseEvent } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [zoom_lvl, setZoom] = useState(3)
  const [angle, setAngle] = useState(90)

  const dragCompass = (MouseEvent) => console.log(MouseEvent);

  return (
    <>
      {/*Define controls for UI here*/}
      <div className="controls">
        <div className="zoom">
          <button 
            onClick={() => setZoom(
              (zoom_lvl) => zoom_lvl > 1 ? zoom_lvl - 1 : zoom_lvl = 1
            )}>
            -
          </button>
          <button 
            onClick={() => setZoom(
              (zoom_lvl) => zoom_lvl < 5 ? zoom_lvl + 1 : zoom_lvl = 5
            )}>
            +
          </button><p>zoom is {zoom_lvl}</p>
        </div>
        <div className="rotate">
          <button 
            onClick={() => setAngle((angle) => (angle + 30) % 360
            )}>
            
          </button>
          <button 
            onClick={() => setAngle(
              (angle) => (angle - 30) % 360
            )}>
            
          </button><p>angle is {angle}</p>
        </div>
      </div>
      <div className='echelons' style={{border: "3px solid red" }}>
        <svg>
          <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
          <circle  r="50" stroke="yellow" stroke-width="4" fill="green" />
        </svg>
      </div>
    </>
  )
}

export default App
