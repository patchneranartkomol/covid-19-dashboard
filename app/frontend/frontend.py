from flask import Blueprint, render_template

frontend_bp = Blueprint('frontend', __name__, template_folder='templates')

@frontend_bp.route('/')
def index():
    """
    Main page of the application
    """
    return render_template('main.html')
