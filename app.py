from flask import Flask, render_template, url_for
import subprocess
import logging

app = Flask(__name__, static_folder='static')

logging.basicConfig(level=logging.INFO)

def run_notebook(notebook_path):
    try:
       
        script_path = notebook_path.replace('.ipynb', '.py')
        subprocess.run(['jupyter', 'nbconvert', '--to', 'script', notebook_path])

        result = subprocess.run(['python', script_path], capture_output=True, text=True)

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except FileNotFoundError:
        return False, "Notebook file not found."
    except subprocess.CalledProcessError as ex:
        return False, f"Error running notebook: {ex}"
    except Exception as e:
        return False, f"An unexpected error occurred: {e}"

@app.route('/')
def index():
  
    notebook_path = 'DAVPROJECT.ipynb'

    
    success, output = run_notebook(notebook_path)

    if success:
       
        return render_template('index.html', success=True, output=output)
    else:
     
        return render_template('index.html', success=False, output=output)

@app.route('/dav_project')
def dav_project():
    return render_template('DAVPROJECT.html')

@app.route('/dav_project1')
def dav_project1():
    return render_template('tree.html')

@app.route('/dav_project2')
def dav_project2():
    return render_template('force.html')

@app.route('/dav_project3')
def dav_project3():
    return render_template('last.html')


@app.route('/dav_project4')
def dav_project4():
    return render_template('scatter.html')


if __name__ == '__main__':
    app.run(debug=False)
