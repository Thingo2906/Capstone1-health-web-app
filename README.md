# Goal of Project:
Creating a website where users can use the BMI tool to calculate their body mass index (BMI), and share their tips to maintain a healthy body. Also, users can find many recipes for their diet plans that fit their unique food preferences. 
# Database Schema:
![Schema](https://user-images.githubusercontent.com/93515126/210734304-fee45794-5095-4d4b-85b0-cc60b510b4b4.png)

# API Using:
- Used the fitness calculator API to calculate the BMI, calculate the daily calorie requirement for different goals:
https://fitness-calculator.p.rapidapi.com/bmi

The fitness calculator API doesn’t have the data for users who weigh more than 160 kg.

- Used spoonacular to find a recipe for users who love to cook at home.
https://api.spoonacular.com/recipes/random?
- Used the Youtube API to show some favorite videos related to eating healthy. 
https://youtube.googleapis.com/youtube/v3/search?
+ The videos can only from 1 channel, and projects that enable the YouTube Data API have a default quota allocation of 10,000 units per day, an amount sufficient for the overwhelming majority of our API users. 

# Technology Stack:
- Frontend: HTML5, CSS3, ES6, JavaScript
- Backend: Python, Flask, SQLAlchemy, Postgres
- Libraries & modules: WTForms, Bcrypt, requests, unittest
- Templating engine: Jinja
- Cloud service platform: Heroku
# Heroku:
https://health-plan-web-app.herokuapp.com/
# Web App Outlook:
## Main page:
<img width="918" alt="initial_page" src="https://user-images.githubusercontent.com/93515126/210743961-1f352fae-8d5a-4367-9665-e75dca96bfa8.png">
## Home page:
<img width="905" alt="home" src="https://user-images.githubusercontent.com/93515126/210744576-59572201-4ef3-4995-9a18-01bcee321e1d.png">
## Profile page:
<img width="918" alt="profile" src="https://user-images.githubusercontent.com/93515126/210744959-f0961749-fef3-46eb-9105-fc7217cfa11f.png">
## BMI result page:
<img width="922" alt="bmi_result" src="https://user-images.githubusercontent.com/93515126/210745780-d3e6342e-0b07-4cde-b0ef-e1225215737c.png">

