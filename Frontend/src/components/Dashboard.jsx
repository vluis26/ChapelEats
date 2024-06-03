import React from 'react'
// import './dashboard.css'
import { useNavigate } from 'react-router-dom'


const Dashboard = ({setIsLoggedIn}) => {
  const navigate = useNavigate()

  const handleLogout = () => {
    setIsLoggedIn(false)
    navigate("/")
  }


  return (
    <div>
      <p>Dashboard</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  )
}

export default Dashboard