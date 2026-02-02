from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_title = request.form.get("task")
        if task_title:
            tasks.append({"title": task_title, "done": False})
        return redirect(url_for("index"))

    filter_type = request.args.get("filter", "all")

    if filter_type == "completed":
        filtered_tasks = [t for t in tasks if t["done"]]
    elif filter_type == "pending":
        filtered_tasks = [t for t in tasks if not t["done"]]
    else:
        filtered_tasks = tasks

    return render_template(
        "index.html",
        tasks=filtered_tasks,
        current_filter=filter_type
    )


@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    if 0 <= task_id < len(tasks):
        tasks[task_id]["done"] = not tasks[task_id]["done"]
    return redirect(request.referrer)


@app.route("/delete/<int:task_id>")
def delete(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)
