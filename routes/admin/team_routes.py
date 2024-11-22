from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from models import TeamMember
from app import db
from routes.utils.error_handlers import handle_exceptions, log_route_access

team_bp = Blueprint('admin_team', __name__)

@team_bp.route('/', methods=['GET', 'POST'])
@login_required
@log_route_access('admin_team')
@handle_exceptions
def team():
    """Manage team members with proper error handling and logging."""
    try:
        team_members = TeamMember.query.order_by(TeamMember.order.asc()).all()
        return render_template('admin/team.html', team_members=team_members)
    except Exception as e:
        current_app.logger.error(f'Team management error: {str(e)}')
        flash('Error loading team members', 'error')
        return redirect(url_for('admin.dashboard'))
