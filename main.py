import requests
from Analysis import covid19Data
import json

def geturl():
    try:
        url = "https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/index.json"
        get_url = requests.get(url)
        get_content = get_url.content
        jsonString  = json.loads(get_content)
        tempURL =  jsonString["basePath"] + jsonString["regions"]["en-us"]["csvPath"]

        finalURL  = "https://covid19-static.cdn-apple.com" + tempURL
        return finalURL

    except Exception as e:
        print(e.__class__)
        print("Couldn't found URL")

def main():

    try:
        # url = "https://covid19-static.cdn-apple.com/covid19-mobility-data/2017HotfixDev9/v3/en-us/applemobilitytrends-2020-09-19.csv"
        url = geturl()
        get_url = requests.get(url)

        # get the type of content.
        type = get_url.headers.get('content-type')

        if(type == "text/csv"):

            # create a object
            obj = covid19Data(get_url)
            obj.run()

        else:
            print("Found other format")

    except Exception as e:
        print(e.__class__)
        print("Data not found(May be timeout)")

if __name__ == "__main__":
    main()












