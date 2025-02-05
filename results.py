from flask import render_template, request, redirect, url_for
from flask.views import MethodView
import re

class Results(MethodView):
    def get(self):
        """
        Render the results page;
        """
        breed = request.args.get('breed')
        image = request.args.get('image')
        recommendation = request.args.get('recommendation')

        # Split the recommendation into a list bullet points
        recommendation_list = re.split(r"\*(?!\*)", recommendation)

        return render_template('results.html', breed=breed, image=image, recommendation=recommendation_list[1:])