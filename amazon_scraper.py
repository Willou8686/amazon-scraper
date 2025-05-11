from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/extract", methods=["GET"])
def extract():
    url = request.args.get("url")
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.find(id="productTitle")
        image = soup.find(id="landingImage")
        price = soup.find("span", {"class": "a-offscreen"})
        rating = soup.select_one("span.a-icon-alt")
        reviews = soup.select_one("#acrCustomerReviewText")

        return jsonify({
            "title": title.get_text(strip=True) if title else None,
            "image": image["src"] if image else None,
            "price": price.get_text(strip=True) if price else None,
            "rating": rating.get_text(strip=True) if rating else None,
            "reviews": reviews.get_text(strip=True) if reviews else None,
            "url": url
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
