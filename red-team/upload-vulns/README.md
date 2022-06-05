# Upload Vulnerabilities

## Python

Some simple ways to do client-side doc type filtering are by specifying an `accept` tag on the requested "input".
```html
<input type="file" name="doc_file" accept=".doc,.docx">
<input type="file" name="image_file" accept="image/*">
```

The app as it is is vulnerable to a vast array of upload vulnerabilities
- you could override any file the app uses (e.g., `templates/home.html`)
- you could override system files (e.g., `../../.bashrc`)
- many others

**Improvements**

Limit the size of uploads
```python
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 # 1mb, anything bigger results in a 413.
```

Before `uploaded.save(uploaded.filename)` you could[should] also include some code to verify
file extensions and file types by using magic numbers.

Also think about storing the file with a filename you control. If you want to keep track of the user's filename, make sure
to sanitize it. An option for this, the Flask documentation advocates for it, is
```python
>>> from werkzeug.utils import secure_filename
>>> secure_filename("/some/path/file.jpeg.php")
'some_path_file.jpeg.php'
>>> secure_filename("../../../.bashrc")
'bashrc'
```
Not perfect but very great was of sanitizing file names.

One last thing, make sure to have a dedicated folder for uploads
```python
app.config['UPLOAD_FOLDER'] = "/path/to/the/uploads"
```

References
- [Digitalocean tutorials: how to make a web application using flask in python3](https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3)
- [Flask documentation: Uploading Files](https://flask.palletsprojects.com/en/2.1.x/patterns/fileuploads/)
- [Handling File Uploads With Flask](https://blog.miguelgrinberg.com/post/handling-file-uploads-with-flask)
