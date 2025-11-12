import viteLogo from '/logo.png'
import BouncingCafes from './pages/Home'
import './App.css'

function App() {
  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
      </div>
      <BouncingCafes />
    </>
  )
}

export default App
