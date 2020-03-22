from flask import Blueprint, render_template

from ..utils.jhu_data import get_country_data, get_global_cases


frontend_bp = Blueprint('frontend', __name__, template_folder='templates')


@frontend_bp.route('/')
def index():
    """
    Main page of the application
    """
    return render_template('main.html')

@frontend_bp.context_processor
def data_processor():
    """
    Merge country data into request context 
    """
    return dict(country_data = get_country_data(),
                global_data = get_global_cases())
