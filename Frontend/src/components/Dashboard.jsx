import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './Dashboard.css';

const Dashboard = ({ setIsLoggedIn, userName, }) => {
  const navigate = useNavigate();

  const [nutritionalGoals, setNutritionalGoals] = useState('');
  const [dietaryRestrictions, setDietaryRestrictions] = useState('');
  const [sex, setSex] = useState('');
  const [mealTime, setMealTime] = useState('');
  const [diningHall, setDiningHall] = useState('');
  const [age, setAge] = useState('');
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');
  

  const handleLogout = () => {
    setIsLoggedIn(false);
    navigate('/');
  };

  const handleGenerate = async () => {
    try {
      const response = await axios.post('http://localhost:8080/generate-meal', {
        nutritionalGoals,
        dietaryRestrictions,
        sex,
        mealTime,
        diningHall,
        age,
        height,
        weight,
      });
  
      console.log('Generated Meal Response:', response.data);
      navigate('/dashboard/meals', { state: { meal_description: response.data.meal_description, recipes_info: response.data.recipes_info } });
    } catch (error) {
      console.error('Error generating meal:', error);
    }
  };
  
  

  return (
    <div className='dashboard-container'>
      <div className='dashboard-user-info'>
        <div className='dashboard-user-name'>Hello {userName}!</div>
        <button className='dashboard-logout-button' onClick={handleLogout}>Logout</button>
      </div>
      <div className='dashboard-header'>
        <div className='dashboard-title'>
          <div className='dashboard-text'>ChapelEats</div>
          <div className='dashboard-text'>Dashboard</div>
        </div>
      </div>
      <div className='dashboard-inputs'>
        <div className='dashboard-input'>
          <label>Nutritional Goals</label>
          <select value={nutritionalGoals} onChange={(e) => setNutritionalGoals(e.target.value)}>
            <option value="">Select</option>
            <option value="weight_loss">Weight Loss</option>
            <option value="muscle_gain">Muscle Gain</option>
            <option value="maintenance">Maintenance</option>
          </select>
        </div>
        <div className='dashboard-input'>
          <label>Dietary Restrictions</label>
          <select value={dietaryRestrictions} onChange={(e) => setDietaryRestrictions(e.target.value)}>
            <option value="">Select</option>
            <option value="vegan">Vegan</option>
            <option value="vegetarian">Vegetarian</option>
            <option value="gluten_free">Gluten Free</option>
            <option value="halal">Halal</option>
            <option value="none">None</option>
          </select>
        </div>
        <div className='dashboard-input'>
          <label>Sex</label>
          <select value={sex} onChange={(e) => setSex(e.target.value)}>
            <option value="">Select</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
        </div>
        <div className='dashboard-input'>
          <label>Meal Time</label>
          <select value={mealTime} onChange={(e) => setMealTime(e.target.value)}>
            <option value="">Select</option>
            <option value="breakfast">Breakfast</option>
            <option value="lunch">Lunch</option>
            <option value="dinner">Dinner</option>
          </select>
        </div>
        <div className='dashboard-input'>
          <label>Dining Hall</label>
          <select value={diningHall} onChange={(e) => setDiningHall(e.target.value)}>
            <option value="">Select</option>
            <option value="hall1">Lenoir Dining Hall</option>
            <option value="hall2">Chase Dining Hall</option>
          </select>
        </div>
        <div className='dashboard-input'>
          <label>Age</label>
          <input type='number' value={age} onChange={(e) => setAge(e.target.value)} />
        </div>
        <div className='dashboard-input'>
          <label>Height (in)</label>
          <input type='number' value={height} onChange={(e) => setHeight(e.target.value)} />
        </div>
        <div className='dashboard-input'>
          <label>Weight</label>
          <input type='number' value={weight} onChange={(e) => setWeight(e.target.value)} />
        </div>
      </div>
      <button className='dashboard-button' onClick={handleGenerate}>Generate Meal</button>
    </div>
  );
};

export default Dashboard;
