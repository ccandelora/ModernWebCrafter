from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from models import db, TeamMember
from routes.utils.error_handlers import handle_exceptions, log_route_access
from routes.utils.upload import handle_team_photo_upload
from routes.utils.validation import validate_team_member_data

team_bp = Blueprint('admin_team_bp', __name__)


@team_bp.route('/', methods=['GET', 'POST'])
@login_required
@log_route_access('admin_team')
@handle_exceptions
def manage_team():
    """Manage team members with proper error handling and logging."""
    try:
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            role = request.form.get('role', '').strip()
            bio = request.form.get('bio', '').strip()

            if not all([name, role, bio]):
                flash('All fields are required', 'error')
                return redirect(url_for('admin.admin_team_bp.manage_team'))

            try:
                member = TeamMember()
                member.name = name
                member.role = role
                member.bio = bio
                member.order = int(request.form.get('order', 0))
                member.is_active = bool(request.form.get('is_active'))

                # Handle image upload
                image = request.files.get('image')
                if image and image.filename:
                    try:
                        member.image_url = handle_team_photo_upload(image)
                    except ValueError as e:
                        flash(str(e), 'error')
                        return redirect(url_for('admin.admin_team_bp.manage_team'))
                    except Exception as e:
                        current_app.logger.error(f'Error uploading image: {str(e)}')
                        flash('Error uploading image. Please try again.', 'error')
                        return redirect(url_for('admin.admin_team_bp.manage_team'))

                db.session.add(member)
                db.session.commit()
                flash('Team member added successfully', 'success')

            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f'Error adding team member: {str(e)}')
                flash(f'Error adding team member: {str(e)}', 'error')

            return redirect(url_for('admin.admin_team_bp.manage_team'))

        # GET request handling
        current_app.logger.debug('Fetching all team members from database')
        team_members = TeamMember.query.order_by(TeamMember.order.asc()).all()
        current_app.logger.debug(f'Found {len(team_members)} team members')
        
        return render_template('admin/team.html', team_members=team_members)
            
    except Exception as e:
        current_app.logger.error(f'Error in admin team route: {str(e)}')
        current_app.logger.exception('Full traceback:')
        flash('Error loading team members. Please try again later.', 'error')
        return render_template('errors/500.html'), 500


@team_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@log_route_access('edit_team_member')
def edit_team_member(id):
    """Handle editing a team member."""
    try:
        member = TeamMember.query.get_or_404(id)
        if request.method == 'POST':
            try:
                # Validate required fields
                name = request.form.get('name', '').strip()
                role = request.form.get('role', '').strip()
                bio = request.form.get('bio', '').strip()

                if not all([name, role, bio]):
                    flash('All fields are required', 'error')
                    return redirect(url_for('admin.admin_team_bp.edit_team_member', id=id))

                # Update member details
                member.name = name
                member.role = role
                member.bio = bio
                member.order = int(request.form.get('order', 0))
                member.is_active = bool(request.form.get('is_active'))

                # Handle image upload if provided
                image = request.files.get('image')
                if image and image.filename:
                    try:
                        member.image_url = handle_team_photo_upload(image, old_file_path=member.image_url)
                    except ValueError as e:
                        flash(str(e), 'error')
                        return redirect(url_for('admin.admin_team_bp.edit_team_member', id=id))
                    except Exception as e:
                        current_app.logger.error(f'Error uploading image: {str(e)}')
                        flash('Error uploading image. Please try again.', 'error')
                        return redirect(url_for('admin.admin_team_bp.edit_team_member', id=id))

                # Save changes
                db.session.commit()
                flash('Team member updated successfully', 'success')
                return redirect(url_for('admin.admin_team_bp.manage_team'))
                
            except ValueError as e:
                flash(str(e), 'error')
                return redirect(url_for('admin.admin_team_bp.edit_team_member', id=id))
            except Exception as e:
                current_app.logger.error(f'Error updating team member: {str(e)}')
                db.session.rollback()
                flash('Error updating team member. Please try again.', 'error')
                return redirect(url_for('admin.admin_team_bp.edit_team_member', id=id))

        # GET request - show edit form
        return render_template('admin/edit_team.html', member=member)
        
    except Exception as e:
        current_app.logger.error(f'Error accessing team member {id}: {str(e)}')
        flash('Error accessing team member. Please try again.', 'error')
        return redirect(url_for('admin.admin_team_bp.manage_team'))


@team_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@log_route_access('delete_team_member')
@handle_exceptions
def delete_team_member(id):
    try:
        member = TeamMember.query.get_or_404(id)
        db.session.delete(member)
        db.session.commit()
        flash('Team member deleted successfully', 'success')
    except Exception as e:
        current_app.logger.error(f'Error deleting team member {id}: {str(e)}')
        current_app.logger.exception('Full traceback:')
        flash('Error deleting team member. Please try again later.', 'error')
        db.session.rollback()
    return redirect(url_for('admin.admin_team_bp.manage_team'))
