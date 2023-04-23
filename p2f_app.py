from flask import Flask, request, render_template_string
import re

app = Flask(__name__)

# The template for rendering the Python code as a web app
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Python Code Web App</title>
</head>
<body>
    <h1>Python Code Web App</h1>
    <form method="post">
        <label for="code">Enter Python code:</label><br>
        <textarea name="code" id="code" cols="80" rows="20">{{ code }}</textarea><br>
        <input type="submit" value="Run">
    </form>
    <hr>
    <h2>Output:</h2>
    {{ output }}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the Python code from the form data
        code = request.form['code']
        # Remove any HTML tags to prevent XSS attacks
        code = re.sub('<[^<]+?>', '', code)
        # Evaluate the code to get the output
        try:
            output = eval(code)
        except Exception as e:
            output = f"Error: {e}"
        # Render the template with the code and output
        return render_template_string(TEMPLATE, code=code, output=output)
    else:
        # Render the template with default code and no output
        return render_template_string(TEMPLATE, code='', output='')

if __name__ == '__main__':
    app.run(debug=True)
