from flask import Flask, render_template, request
import requests

app = Flask(__name__)


LANGUAGES = {
    "en": "English",
    "te": "Telugu",
    "hi": "Hindi",
    "ta": "Tamil",
    "kn": "Kannada",
    "ml": "Malayalam"
}


def translate_text(text, source, target):

    # If both languages are same
    if source == target:
        return text

    try:

        url = "https://translate.googleapis.com/translate_a/single"

        params = {
            "client": "gtx",
            "sl": source,
            "tl": target,
            "dt": "t",
            "q": text
        }

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        result = ""

        for item in data[0]:
            if item[0]:
                result += item[0]

        result = result.strip()

        if result:
            return result

    except Exception as e:

        print("Translation error:", e)


    return "Translation unavailable."


@app.route("/", methods=["GET", "POST"])
def home():

    # Default values for first page load
    original_text = ""
    translation = ""

    source = "en"
    target = "te"


    if request.method == "POST":

        # Get exactly what user submitted
        original_text = request.form.get("text", "")

        source = request.form.get("source", "en")

        target = request.form.get("target", "te")


        if original_text.strip():

            translation = translate_text(
                original_text.strip(),
                source,
                target
            )


    return render_template(
        "index.html",
        original_text=original_text,
        translation=translation,
        selected_source=source,
        selected_target=target,
        languages=LANGUAGES
    )


if __name__ == "__main__":
    app.run(debug=True)