import React from 'react';
import { useLocation } from 'react-router-dom';
import './Meals.css';

const Meals = () => {
  const location = useLocation();
  const { meal_description, recipes_info } = location.state || {};

  console.log('Location State:', location.state);

  if (!meal_description) {
    return <div>No meal description available.</div>;
  }

  return (
    <div className='meals-container'>
      <h1>Generated Meal Plan</h1>
      <p>{meal_description}</p>
      <h2>Recipe Details</h2>
      {recipes_info && recipes_info.length > 0 ? (
        recipes_info.map((recipe, index) => (
          <div key={index} className='recipe'>
            <h3>{recipe.recipe_name}</h3>
            <p><strong>Allergens:</strong> {recipe.allergens}</p>
            <h4>Nutritional Information</h4>
            <ul>
              {Object.entries(recipe.nutrition_info).map(([nutrient, amount], idx) => (
                <li key={idx}>{nutrient}: {amount}</li>
              ))}
            </ul>
          </div>
        ))
      ) : (
        <p>No recipes information available.</p>
      )}
    </div>
  );
};

export default Meals;
