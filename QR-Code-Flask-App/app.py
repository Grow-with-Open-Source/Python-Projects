from flask import Flask, render_template, request, send_file
import qrcode
import io

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    qr_ready = False

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if url:
            # Add https:// if the user forgot it
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            qr_ready = True
            return render_template("index.html", qr_ready=qr_ready, url=url)

    return render_template("index.html", qr_ready=qr_ready, url="")


@app.route("/download")
def download():
    """Generates the QR code image on the fly and sends it to the browser as a download."""
    url = request.args.get("url", "")

    if not url:
        return "No URL provided", 400

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save image to memory instead of disk, so it can be sent straight to the browser
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="image/png",
        as_attachment=True,
        download_name="qr.png",
    )


if __name__ == "__main__":
    app.run(debug=True)
