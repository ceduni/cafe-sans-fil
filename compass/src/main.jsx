import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import Compass from './Compass.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Compass />
  </StrictMode>,
)
