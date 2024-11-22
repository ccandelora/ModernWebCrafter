from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required
from models import TeamMember
from app import db
from routes.utils.error_handlers import handle_exceptions, log_route_access
from routes.utils.upload import handle_file_upload
from routes.utils.validation import validate_team_member_data

team_bp = Blueprint('admin_team', __name__)

@team_bp.route('/', methods=['GET', 'POST'])
@login_required
@log_route_access('admin_team')
@handle_exceptions
def manage_team():
    """Manage team members with proper error handling and logging."""
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        bio = request.form.get('bio')
        
        if not all([name, role, bio]):
            flash('All fields are required', 'error')
            return redirect(url_for('admin.admin_team.manage_team'))
        
        try:
            member = TeamMember()
            member.name = name.strip()
            member.role = role.strip()
            member.bio = bio.strip()
            member.order = int(request.form.get('order', 0))
            member.is_active = bool(request.form.get('is_active'))
            
            # Handle image upload
            image = request.files.get('image')
            if image and image.filename:
                try:
                    image_path = handle_file_upload(image)
                    member.image_url = image_path
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('admin.admin_team.manage_team'))
                except Exception as e:
                    flash(f'Error uploading image: {str(e)}', 'error')
                    return redirect(url_for('admin.admin_team.manage_team'))
            
            db.session.add(member)
            db.session.commit()
            flash('Team member added successfully', 'success')
            
        except ValueError as e:
            flash(f'Invalid data: {str(e)}', 'error')
            return redirect(url_for('admin.admin_team.manage_team'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding team member: {str(e)}', 'error')
            return redirect(url_for('admin.admin_team.manage_team'))
        
        return redirect(url_for('admin.admin_team.manage_team'))

    team_members = TeamMember.query.order_by(TeamMember.order.asc()).all()
    return render_template('admin/team.html', team_members=team_members)

@team_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@log_route_access('edit_team_member')
@handle_exceptions
def edit_team_member(id):
    member = TeamMember.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        role = request.form.get('role')
        bio = request.form.get('bio')
        
        if not all([name, role, bio]):
            flash('All fields are required', 'error')
            return redirect(url_for('admin.admin_team.edit_team_member', id=id))
        
        member.name = name.strip()
        member.role = role.strip()
        member.bio = bio.strip()
        member.order = int(request.form.get('order', 0))
        member.is_active = bool(request.form.get('is_active'))
        
        image = request.files.get('image')
        if image and image.filename:
            try:
                new_image_path = handle_file_upload(image, old_file_path=member.image_url)
                member.image_url = new_image_path
            except Exception as e:
                flash(str(e), 'error')
                return redirect(url_for('admin.admin_team.manage_team'))
        
        db.session.commit()
        flash('Team member updated successfully', 'success')
        return redirect(url_for('admin.admin_team.manage_team'))
    
    return render_template('admin/edit_team.html', member=member)
    if request.method == 'POST':
        # Validate form data
        error = validate_team_member_data(request.form)
        if error:
            flash(error, 'error')
            return redirect(url_for('admin.team'))

        try:
            # Create new team member
            member = TeamMember()
            name = request.form.get('name')
            role = request.form.get('role')
            bio = request.form.get('bio')
            
            if not all([name, role, bio]):
                raise ValueError("Name, role, and bio are required fields")
                
            member.name = name.strip()
            member.role = role.strip()
            member.bio = bio.strip()
            member.order = int(request.form.get('order', 0))
            member.is_active = bool(request.form.get('is_active'))
            
            # Handle image upload
            image = request.files.get('image')
            if image and image.filename:
                try:
                    image_path = handle_file_upload(image)
                    member.image_url = image_path
                except ValueError as e:
                    flash(str(e), 'error')
                    return redirect(url_for('admin.team'))
                except Exception as e:
                    flash(f'Error uploading image: {str(e)}', 'error')
                    return redirect(url_for('admin.team'))
            
            db.session.add(member)
            db.session.commit()
            flash('Team member added successfully', 'success')
            
        except ValueError as e:
            flash(f'Invalid data: {str(e)}', 'error')
            return redirect(url_for('admin.team'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding team member: {str(e)}', 'error')
            return redirect(url_for('admin.team'))
            
        return redirect(url_for('admin.team'))

    team_members = TeamMember.query.order_by(TeamMember.order.asc()).all()
    return render_template('admin/team.html', team_members=team_members)

@team_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
@log_route_access('delete_team_member')
@handle_exceptions
def delete_team_member(id):
    member = TeamMember.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Team member deleted successfully', 'success')
    return redirect(url_for('admin.team'))