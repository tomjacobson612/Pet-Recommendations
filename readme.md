# Program Description
This program allows users to upload an image either from the web or from their local storage. The program then analyzes the image to determine the breed of dog present and sends that breed information to an AI that constructs personalized pet recommendations. The recommendation prompt can be further edited by the user via a web based form. 

# How to run locally
- Run "python3 -m venv venv" in your terminal to create a virtual environment folder named venv.

- Activate the virtual environment: venv\Scripts\activate

- Optional: Generate requirements.txt if it does not already exist. 
    - pip freeze > requirements.txt

- Install dependencies: pip install -r /path/to/requirements.txt

- Set API Key 
    - This application uses google Gemini and reuquires an API key. To run locally you will need to go to https://aistudio.google.com/app/apikey to generate an API key. 
    - Select "create API key" and in the search bar look for Gemini API
    - Copy this key and set it is an environment variable named "GOOGLE_API_KEY". 
        - Windows: $env:GOOGLE_API_KEY = YOUR_KEY
        - Linux: export GOOGLE_API_KEY= YOUR_KEY

- Run the application locally: python app.py
