from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import mission_to_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def index():
    mars_mission = mongo.db.mars.find_one()
    return render_template("index.html", mars_mission=mars_mission)


@app.route("/scrape")
def scraper():
    mars_mission = mongo.db.mars
    mars_mission_data = mission_to_mars.scrape()
    mars_mission.update({}, mars_mission_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)