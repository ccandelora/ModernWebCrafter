from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import TeamMember
from app import db

team_bp = Blueprint('team', __name__)

@team_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    # Debug prints
    print("Accessing team index route")
    
    try:
        # Check if we can query the table
        print("Attempting to query TeamMember table...")
        members = TeamMember.query.all()
        print(f"Query successful. Found {len(members)} members")
        for member in members:
            print(f"Member: {member.name} - {member.role}")
    except Exception as e:
        print(f"Error querying team members: {str(e)}")
        members = []
    
    return render_template('admin/team.html', members=members)

@team_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_team_member(id):
    member = TeamMember.query.get_or_404(id)
    
    if request.method == 'POST':
        member.name = request.form.get('name')
        member.role = request.form.get('title')  # Getting 'title' from form but saving as 'role'
        member.bio = request.form.get('bio')
        
        try:
            db.session.commit()
            flash('Team member updated successfully', 'success')
            return redirect(url_for('admin.team_management.index'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating team member: {str(e)}', 'error')
    
    return render_template('admin/edit_team.html', member=member)

@team_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_team_member(id):
    member = TeamMember.query.get_or_404(id)
    try:
        db.session.delete(member)
        db.session.commit()
        flash('Team member deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting team member: {str(e)}', 'error')
    
    return redirect(url_for('admin.team_management.index'))

@team_bp.route('/init', methods=['GET'])
@login_required
def init_team():
    # Check if we already have team members
    if TeamMember.query.count() == 0:
        # Create initial team members
        team_members = [
            TeamMember(
                name="John Wood",
                role="Master Craftsman",
                bio="With over 20 years of experience in custom woodworking, John leads our production team with expertise and passion.",
                image_url="/static/images/avatar-placeholder.svg"
            ),
            TeamMember(
                name="Sarah Miller",
                role="Design Specialist",
                bio="Sarah brings creative vision to every project, specializing in custom designs and client consultations.",
                image_url="/static/images/avatar-placeholder.svg"
            ),
            TeamMember(
                name="Mike Chen",
                role="Production Manager",
                bio="Overseeing our workshop operations, Mike ensures every project meets our high quality standards.",
                image_url="/static/images/avatar-placeholder.svg"
            ),
            TeamMember(
                name="Emma Thompson",
                role="Client Relations",
                bio="Emma works directly with clients to understand their needs and ensure complete satisfaction.",
                image_url="/static/images/avatar-placeholder.svg"
            )
        ]
        
        try:
            for member in team_members:
                db.session.add(member)
            db.session.commit()
            flash('Initial team members added successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding initial team members: {str(e)}', 'error')
    
    return redirect(url_for('admin.team_management.index'))
