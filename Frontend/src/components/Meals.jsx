import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './Meals.css';
import axios from 'axios';

const Meals = ({userEmail}) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { email, meal_description = "No meal description available", nutritional_info = {} } = location.state || {};

  if (!email) {
    return <div>Error: Email is required to save meals.</div>;
  }

  const handleSave = async () => {
    const mealData = {
      email,
      meal_description,
      nutritional_info
    };

    try {
      const response = await axios.post('https://chapeleats.onrender.com/save-meal', mealData);
      if (response.status === 201) {
        navigate('/dashboard/meals/saved-meals', {state: {email:userEmail}});
      } else {
        console.error('Failed to save meal');
      }
    } catch (error) {
      console.error('Error saving meal:', error);
    }
  };

  return (
    <div className='meals-container'>
      <h2>Generated Meal</h2>
      <p>{meal_description}</p>
      <button className='meals-button' onClick={handleSave}>Save Meal</button>
    </div>
  );
};

export default Meals;
