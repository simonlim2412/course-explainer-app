from flask import render_template
from models import courses

def index():
    return render_template('index.html', courses=courses)

def course(course_id):
    # Convert course_id to int and handle 1-based indexing for simplicity in this example
    idx = int(course_id) - 1
    if 0 <= idx < len(courses):
        return render_template('course.html', course=courses[idx])
    return "Course not found", 404