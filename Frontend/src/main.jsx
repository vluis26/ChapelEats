import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import Meals  from './components/Meals'
import SavedMeals from './components/SavedMeals';
import './index.css';

const App = () => {
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [userName, setUserName] = React.useState('');
  const [userEmail, setUserEmail] = React.useState('')

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login setIsLoggedIn={setIsLoggedIn} setUserName={setUserName} setUserEmail={setUserEmail} />} />
        <Route path="/dashboard" element={isLoggedIn ? <Dashboard setIsLoggedIn={setIsLoggedIn} userName={userName} userEmail={userEmail} /> : <Navigate to="/" />} />
        <Route path="/dashboard/meals" element={isLoggedIn ? <Meals /> : <Navigate to="/" />} />
        <Route path="/dashboard/meals/saved-meals" element={isLoggedIn ? <SavedMeals userEmail={userEmail} /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
};

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
