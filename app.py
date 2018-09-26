from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
marsNews = mongo.db.mars_db

@app.route("/")
def home():

    marsPull =  marsNews.find_one(); #//list(marsNews.find_one())
    #marsHemis = list(marsNews.aggregate([{'$unwind' : '$mars_hemis'}, {'$project' : {'mars_hemis_title' : '$mars_hemis.title'}}]))
    #marsFacts = list(marsNews.aggregate([{'$unwind' : '$mars_facts'}, {'$project' : {'ED' : '$mars_facts.Value.Equatorial Diameter:', 'Moons' : '$mars_facts.Value.Moons:'}}])
    return render_template("index.html", marsPull=marsPull)
@app.route("/scrape")
def scrape():
    marsData_results = scrape_mars.scrape()
    marsInfo = {
        "mars_news": marsData_results["Mars News Title"],
        "mars_news_p": marsData_results["Mars News"],
        "mars_feat_image": marsData_results["Mars Featured Image"],
        "mars_weather": marsData_results["Mars Weather"],
        "mars_facts": marsData_results["Mars Facts"],
        "mars_hemis": marsData_results["Mars Hemispheres"]
    }
    marsNews.update({},marsInfo, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True) 