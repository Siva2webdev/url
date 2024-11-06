from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def upload_form():
    return '''
    <!doctype html>
<html lang="en">
<head>
    <title>Bindaas</title>
</head>
    
<h1 style="font-size: 5em; animation: disco 1s infinite; margin-top: 10px; text-align: center;">
    Bindaas
</h1>

<style>
@keyframes disco {
    0% { color: #FF0000; }   /* Red */
    20% { color: #FF7F00; }  /* Orange */
    40% { color: #FFFF00; }  /* Yellow */
    60% { color: #00FF00; }  /* Green */
    80% { color: #0000FF; }  /* Blue */
    100% { color: #8B00FF; } /* Violet */
}
</style>

    <h1 style="font-size: 2em; background: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet); -webkit-background-clip: text; color: transparent; margin-top: 10px; text-align: center;">
    Combo to M3U Link Converter
</h1>

<body style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; font-family: Arial, sans-serif;  margin: 0; padding: 0; background-color: #000; color: #333;">

    <form action="/upload" method="post" enctype="multipart/form-data" style="background-color: #f0f0f0; padding: 20px; border-radius: 8px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); width: 280px; text-align: left;">
        <label for="url" style="font-size: 1em; font-weight: bold; color: #333;">Enter URL (http://playtv44.com:8080)</label><br>
        <input type="text" name="url" required style="width: 100%; padding: 8px; margin: 8px 0 16px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;"><br>
        <label for="url" style="font-size: 0.8em; font-weight: bold; color: #333;">Upload combo File Here</label><br>   
        <input type="file" name="file" required style="margin: 8px 0 16px;"><br>

        <input type="submit" value="Upload and Generate URL's" style="width: 100%; background-color: #4CAF50; color: white; padding: 10px; border: none; border-radius: 4px; font-size: 1em; cursor: pointer;">
    </form>

    <h2 style="font-size: 1em; color: #666; margin-top: 20px; text-align: center;">
        Join our Telegram: <a href="https://t.me/Bindaa_ss" target="_blank" style="color: #0000FF; text-decoration: none;">https://t.me/Bindaa_ss</a>
    </h2>

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
        # Save the uploaded file
        input_path = 'pxl.txt'
        file.save(input_path)
        
        # Process the file to generate URLs
        output_path = 'output_urls.txt'
        with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
            for line in infile:
                line = line.strip()
                if ':' in line:
                    user, password = line.split(':', 1)
                    url = f"{base_url}/get.php?username={user}&password={password}&type=m3u_plus"
                    outfile.write(url + '\n')
        
        # Provide a download link for the output file
        return '''
        <h2>URLs generated successfully!</h2>
        <a href="/download">Download output file</a>
        '''
    
    return "File processing failed."

@app.route('/download')
def download_file():
    output_path = 'output_urls.txt'
    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
