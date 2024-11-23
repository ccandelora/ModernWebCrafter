from flask import Blueprint, redirect, url_for, render_template
from utils.decorators import log_route_access, handle_exceptions
from flask_login import login_required

admin = Blueprint('admin', __name__)

@admin.route('/')
@login_required
@log_route_access('admin_index')
@handle_exceptions
def admin_index():
    return redirect(url_for('admin.dashboard'))

@admin.route('/dashboard')
@login_required
@log_route_access('admin_dashboard')
@handle_exceptions
def dashboard():
    return render_template('admin/dashboard.html')
