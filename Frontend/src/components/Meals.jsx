import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useLocation } from 'react-router-dom';

const Meals = () => {
  const location = useLocation();
  const userEmail = location.state?.email;
  const [mealPlan, setMealPlan] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMealPlan = async () => {
      try {
        const response = await axios.post('http://localhost:8080/generate-meal', {
          email: userEmail
        });
        setMealPlan(response.data.meal_plan);
      } catch (error) {
        console.error('Error fetching meal plan:', error);
      } finally {
        setLoading(false);
      }
    };

    if (userEmail) {
      fetchMealPlan();
    }
  }, [userEmail]);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h2>Generated Meal Plan</h2>
      <p>{mealPlan}</p>
    </div>
  );
};

export default Meals;
