from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for
)
import requests

BACKEND_URL = "http://127.0.0.1:5000/tasks"

app = Flask(__name__)

@app.get("/")
def get_index():
    return render_template("index.html")

@app.get("/about")
def get_about():
    me = {
        "first_name": "Andrew",
        "last_name": "McKinnon",
        "hobbies": "Esports"
    }
    return render_template("about.html", user=me)

@app.get("/tasks")
def show_task_list():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template("list.html", tasks=task_list)
    return (
        render_template("error.html", err=response.status_code),
        response.status_code
    )

@app.get("/tasks/edit/<int:pk>")
def edit_form(pk):
    url= "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        task_data = response.json().get("task")
        return render_template("edit.html", task=task_data)
    return (
        render_template("error.html", err=response.status_code),
        response.status_code
    )

@app.post("/tasks/edit/<int:pk>")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    task_data = request.form
    response = requests.put(url, json=task_data)
    if response.status_code == 204:
        return render_template("success.html")
    return (
        render_template("error.html", err=response.status_code),
        response.status_code
    )

@app.get("/tasks/<int:pk>")
def show_task_detail(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        response_body = response.json()
        task_data = response_body.get("task")
        return render_template("detail.html", task=task_data)
    return (
        render_template("error.html", err=response.status_code),
        response.status_code
    )

@app.get("/newtask")
def get_new_task():
    return render_template("newtask.html")

@app.post("/newtask")
def create_new_task():
    task_data = {
        "summary": request.form.get("task"),
        "description": request.form.get("description")
    }

    response = requests.post(BACKEND_URL, json=task_data)

    if response.status_code == 201:
        success_message = "Task created successfully!"
        return render_template("newtask.html", success_message=success_message)
    else:
        return (
            render_template("error.html", err=response.status_code),
            response.status_code
        )

