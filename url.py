from flask import Flask, request, send_file
import os

app = Flask(__name__)

@app.route('/')
def upload_form():
    return '''
    <!doctype html>
    <title>Upload user:pass File</title>
    <h1>Upload user:pass File (pxl.txt) and Base URL</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <label for="url">Enter Base URL (e.g., http://king4k.one:80):</label><br>
        <input type="text" name="url" required><br><br>
        <input type="file" name="file" required><br><br>
        <input type="submit" value="Upload and Generate URLs">
    </form>
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
