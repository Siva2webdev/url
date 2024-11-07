from flask import Flask, request, send_file, make_response
import io

app = Flask(__name__)

@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <title>Bindaas</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="icon" type="image/png" href="https://i.postimg.cc/hGDHgyzD/Bindaas.png">
        <style>
            /* Disco animation for the title */
            @keyframes disco {
                0% { color: #FF0000; }
                20% { color: #FF7F00; }
                40% { color: #FFFF00; }
                60% { color: #00FF00; }
                80% { color: #0000FF; }
                100% { color: #8B00FF; }
            }
            @keyframes disco1 {
                0% { color: #FF0000; }
                20% { color: #FF7F00; }
                40% { color: #515103; }
                60% { color: #090909; }
                80% { color: #0000FF; }
                100% { color: #8B00FF; }
            }

            /* Responsive page layout */
            body {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #000;
                color: #fff;
            }

            h1 {
                font-size: 3em;
                animation: disco 1s infinite;
                margin-top: 10px;
                text-align: center;
            }

            h2 {
                font-size: 1.5em;
                text-align: center;
                color: #666;
                margin-top: 20px;
            }

            form {
                background-color: #f0f0f0;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
                width: 90%;
                max-width: 400px;
                text-align: left;
            }

            label {
                font-size: 1em;
                font-weight: bold;
                color: #333;
            }

            input[type="text"],
            input[type="file"] {
                width: 100%;
                padding: 8px;
                margin: 8px 0 16px;
                box-sizing: border-box;
                border: 1px solid #ccc;
                border-radius: 4px;
            }

            input[type="submit"] {
                width: 100%;
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 4px;
                font-size: 1em;
                cursor: pointer;
            }

            a {
                color: #0000FF;
                text-decoration: none;
            }

            @media (max-width: 600px) {
                h1 {
                    font-size: 2.5em;
                }

                h2 {
                    font-size: 1em;
                }

                form {
                    width: 90%;
                    padding: 15px;
                }
            }
        </style>
    </head>
    <body>
        <h1>Bindaas</h1>
        <h2 style="font-size: 2em; background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet); -webkit-background-clip: text; color: transparent; margin-top: 10px; text-align: center;">
    Combo to M3U Link Converter
</h2>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="url">Enter URL (e.g., http://playtv44.com:8080)</label><br>
            <input type="text" name="url" required><br>
            <label for="url">Upload combo File Here</label><br>
            <input type="file" name="file" required><br>
            <input type="submit" value="Upload and Generate URLs">
        </form>
        <span style="display: flex; align-items: center; gap: 10px;">
            <h4>Telegram: <a style="animation: disco1 0.5s infinite;" href="https://t.me/Bindaa_ss" target="_blank">Join</a></h4>
            <h4>M3U Status Checker: <a style="animation: disco1 0.5s infinite;" href="https://m3uhost.vercel.app/" target="_blank">Click Here</a></h4>
        </span>
    </body>
    </html>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or 'url' not in request.form:
        return "No file or URL provided."

    file = request.files['file']
    base_url = request.form['url']
    if file.filename == '':
        return "No selected file."

    if file:
        # Use in-memory buffer instead of saving to disk
        output_buffer = io.StringIO()

        # Process the uploaded file to generate URLs
        for line in file.stream:
            line = line.decode().strip()
            if ':' in line:
                user, password = line.split(':', 1)
                url = f"{base_url}/get.php?username={user}&password={password}&type=m3u_plus"
                output_buffer.write(url + '\n')

        # Move buffer pointer to start
        output_buffer.seek(0)

        # Send the buffer as a downloadable file
        response = make_response(send_file(
            io.BytesIO(output_buffer.getvalue().encode()),
            as_attachment=True,
            download_name="output_urls.txt",
            mimetype="text/plain"
        ))
        return response

    return "File processing failed."

if __name__ == '__main__':
    app.run(debug=True)
