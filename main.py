import requests
from Analysis import Covid19Data


def geturl():
    try:
        url = "https://covid19-static.cdn-apple.com/covid19-mobility-data/current/v3/index.json"
        url_data = requests.get(url).json()
        return "https://covid19-static.cdn-apple.com{}{}".format(
            url_data["basePath"],
            url_data["regions"]["en-us"]["csvPath"]
        )
    except Exception as e:
        raise Exception("Error".format(e))


def main():
    try:
        data = requests.get(geturl())
        content_type = data.headers.get('content-type')

        if content_type == "text/csv":
            Covid19Data(data).run()
        else:
            print("Format incorrect: {}".format(content_type))
    except Exception as e:
        raise Exception("Error: {}".format(e))


if __name__ == "__main__":
    main()
