from flask import Flask,render_template, request, redirect, url_for
from git import Repo
import os
from urllib.parse import urlparse
from pathlib import Path

app = Flask(__name__)


def parser(full_path):

    path = full_path

    files = []
# r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        for file in f:
            if '.md' in file:
                if 'README.md' not in file:
#                    files.append(os.path.join(r, file))
                    root = r.replace(path,"")
                    url_path = root + "/" + file.replace('.md', '')
                    path = str(url_path)
                    print(path)


def create_dir(gh_url):
 #    from ipdb import set_trace;set_trace()

    git_url = gh_url

    git_dir = git_url.strip('/').split('/')
    git_dir = git_dir[-1]

    if not os.path.exists(git_dir):
        os.mkdir(git_dir)

    home = Path(Path.home())
    new_dir = "new_dir"

    if not os.path.exists(new_dir):
        os.mkdir(new_dir)

    path = os.path.join(home, new_dir)

    full_path = os.path.join(path, git_dir)

    Repo.clone_from(git_url, full_path)
    
    parser(full_path)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == 'POST':
        gh_url  = request.form['gh_url']
        
        if len(gh_url) == 0:
            message = "Please enter the github repo"
        else:
            create_dir(gh_url)
#            message = message
    return render_template('index.html', title='Index Page')                

app.run(debug=True)

