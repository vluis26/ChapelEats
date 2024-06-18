import React, { useEffect, useState } from 'react';
import './SavedMeals.css';

const SavedMeals = ({ userEmail }) => {
  const [savedMeals, setSavedMeals] = useState([]);

  useEffect(() => {
    const fetchSavedMeals = async () => {
      try {
        // Include email parameter in the URL
        const response = await fetch(`https://chapeleats.onrender.com/get-saved-meals?email=${userEmail}`);
        if (response.ok) {
          const data = await response.json();
          setSavedMeals(data.savedMeals);
        } else {
          console.error('Failed to fetch saved meals');
        }
      } catch (error) {
        console.error('Error:', error);
      }
    };

    fetchSavedMeals();
  }, [userEmail]);

  return (
    <div className='saved-meals-container'>
      <h2>Saved Meals</h2>
      {savedMeals.length > 0 ? (
        savedMeals.map((meal, index) => (
          <div key={index} className='meal'>
            <p>{meal.meal_description}</p>
          </div>
        ))
      ) : (
        <p>No saved meals.</p>
      )}
    </div>
  );
};

export default SavedMeals;
