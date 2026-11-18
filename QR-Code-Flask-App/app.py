from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
import io

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        #using strip() to remove any leading/trailing whitespace from the URL
        url = request.form.get('url', '').strip()
        #using if not url: to check if the URL is empty or None, and redirecting to the index page if it is
        if not url:
            return redirect(url_for('index'))
        return redirect(url_for('index', url=url))

    url = request.args.get('url', '')
    qr_ready = bool(url)
    return render_template('index.html', url=url, qr_ready=qr_ready)

@app.route('/download')
def download():
    url = request.args.get('url', '')
    preview = request.args.get('preview')
    
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