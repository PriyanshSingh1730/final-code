from flask import Flask, render_template, request, flash # type: ignore
import qrcode # type: ignore
import base64
from io import BytesIO

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'your_secret_key_here'  

def generate_qr(data):
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="#3B82F6", back_color="#ffffff")
        buffer = BytesIO()
        img.save(buffer, "PNG")
        buffer.seek(0)
        return buffer, None  
    except Exception as e:
        return None, str(e)  

@app.route('/', methods=['GET', 'POST'])
def home():
    qr_data = None
    error = None
    if request.method == 'POST':
        data = request.form.get('data')
        if data and data.strip():
            buffer, error = generate_qr(data)
            if not error:
                qr_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
            else:
                flash(f"Error generating QR code: {error}", "error")
        else:
            flash("Please enter some text or a URL to generate a QR code.", "error")
    return render_template('index.html', qr_data=qr_data, input_data=request.form.get('data', ''))

if __name__ == '__main__':
    app.run(debug=True)