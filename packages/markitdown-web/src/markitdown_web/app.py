import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from markitdown import MarkItDown # Assuming markitdown is installable/importable

# Define the upload folder and ensure it exists
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp_uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'supersecretkey' # Needed for flash messages

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)

            # Initialize MarkItDown
            md = MarkItDown()
            # Convert the file
            result = md.convert(filepath)
            markdown_content = result.text_content

            # For now, we'll store it in the session or pass it to a new route.
            # Let's assume we'll pass it to a template called 'result.html' (to be created in the next step)
            # We'll use flash to pass the content for now, ideally it would be passed to render_template directly
            # flash(markdown_content, 'markdown_result') # Flashing large content is not ideal.
            # Instead, we will render a new template directly in the next step.
            # For this step, let's just store it in a variable and prepare for the next step.

            # Clean up the uploaded file
            os.remove(filepath)

            # Render the result template
            return render_template('result.html', markdown_content=markdown_content)

        except Exception as e:
            flash(f'An error occurred during conversion: {str(e)}')
            if os.path.exists(filepath):
                os.remove(filepath) # Clean up if an error occurs after saving
            return redirect(url_for('index'))
        
    return redirect(url_for('index'))


@app.route('/hello') # Kept for testing if needed
def hello_world():
    return 'Hello, MarkItDown Web!'

if __name__ == '__main__':
    # Suitable for running in Docker. For local dev, debug=True is fine.
    # The FLASK_ENV=production in Dockerfile would ideally set debug=False,
    # but explicitly setting it here for direct python execution.
    app.run(host='0.0.0.0', port=5000, debug=False)
