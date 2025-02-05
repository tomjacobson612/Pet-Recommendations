from flask import render_template, request, redirect, url_for
from flask.views import MethodView
import requests, json, os, time, random
import google.generativeai as genai

class Query(MethodView):
    def get(self):
        """
        Render the form. 
        """
        return render_template('query.html')

    def post(self):
        """
        Accepts POST requests and processes uploaded image or URL;
        Redirect to results when completed.
        """
        
        #Dog breed classifier "https://www.nyckel.com/console/pretrained/dog-breed-identifier"
        classifier = 'https://www.nyckel.com/v1/functions/dog-breed-identifier/invoke'

        #Process Form Fields
        url = request.form['url']
        image_file = request.files.get('image file')

        #Process Optional Fields
        age = request.form['age']
        activity = request.form['activity_level']
        additional_info = request.form['additional_info']

        #Process image upload and redirect to results
        if image_file:

            #Set upload path and create directory if non-existant
            upload_folder = os.path.join('static', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)

            #Clean filename to prevent conflicts by appending timestamp and random number to a standard naming convention.
            cleaned_filename = f"{int(time.time())}_{random.randint(0, 1000)}_user_upload.jpg"
            filename = os.path.join(upload_folder, cleaned_filename)
            image_file.save(filename)

            #Detect Breed using classifier
            with open(filename, 'rb') as img:
                result = requests.post(classifier, files={"data": img})
                result = json.loads(result.text)
                breed = result["labelName"]
            
            #Generate a recommendation using Gemini
            recommendation = self.generate_recommendations(breed, age, activity, additional_info)

            return redirect(url_for('results', breed=breed, image=url_for('static', filename='uploads/' + cleaned_filename), recommendation=recommendation))

        #If url provided and no image uploaded, process url and redirect to results
        if url:
            result = requests.post(classifier, json={"data":url})
            result = json.loads(result.text)
            breed = result["labelName"]
            
            #Generate a recommendation using Gemini
            recommendation = self.generate_recommendations(breed, age, activity, additional_info)

            return redirect(url_for('results', breed=breed, image=url, recommendation=recommendation))

            
        
    def generate_recommendations(self, breed, age, activity, additional_info):
        GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        #Default prompt
        prompt = f"""I am thinking about adopting a new dog. The dog is an {breed}.
        Could you provide me with a succint bulleted list of care recommendations
        for my new dog? Please provide breed specific advice."""

        #Optional Fields
        if age:
            prompt += f"The dog is {age} years old."
        if activity:
            prompt += f"The dog has a {activity} level."
        if additional_info:
            prompt += f"Some additional information to consider is as follows {additional_info}"

        #Additional formatting parameters to be included in the query.
        formatting_parameters = "Do not bold anything."

        response = model.generate_content(prompt + formatting_parameters)
        return response.text