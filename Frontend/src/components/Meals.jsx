import React from 'react';
import { useLocation } from 'react-router-dom';
import './Meals.css';

const Meals = () => {
  const location = useLocation();
  const { meal_description } = location.state || {};

  return (
    <div className='meals-container'>
      <h2>Generated Meal</h2>
      <p>{meal_description}</p>
    </div>
  );
};

export default Meals;
