This is my full-stack web application to assist UNC students with personalized meal planning based on dietary needs and preferences, using OpenAI API, my web app is able to generate meals based of the user's preferences.
Built using Vite + React for my frontend, Flask for my backend, and MongoDB for my database.

Users can register using their name, email, and password, to login users need their email and password. After passing authentication, it would lead them to their dashboard where they would be able to add their preferances such as nutritional goals, meal time, sex, age, etc.
At the bottom of the dashboard, the user has the option to "Generate Meal" (using AI) or "View Saved Meals" 
<img width="626" alt="Screenshot 2024-06-16 at 3 13 46 AM" src="https://github.com/vluis26/ChapelEats/assets/111467809/f96dad08-e6f1-47d7-bca4-b25ea632f95f">
<img width="626" alt="Screenshot 2024-06-16 at 3 16 40 AM" src="https://github.com/vluis26/ChapelEats/assets/111467809/5f583eab-b8d0-4011-9b07-12d6090131d5">

Here the user can see the meal the AI created using their preferences. It displayes each food item with its respective nutritional information. The user also has the option to save that meal if they would want to use it in the future.
<img width="688" alt="Screenshot 2024-06-16 at 3 19 11 AM" src="https://github.com/vluis26/ChapelEats/assets/111467809/07ab7595-ad44-4da8-9c20-137364b7916a">

The user is able to view all of the meals that they saved after the meal was generated
<img width="688" alt="Screenshot 2024-06-16 at 3 21 17 AM" src="https://github.com/vluis26/ChapelEats/assets/111467809/0858b843-f039-4d21-bd47-0097c2eb8950">


Deployed Frontend with Netlify and Backend with Railway
