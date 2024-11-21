from app import app, db
from models import TeamMember

with app.app_context():
    # Clear existing team members if any
    TeamMember.query.delete()
    db.session.commit()
    
    # Add sample team members
    # Create sample team members
    john = TeamMember()
    john.name = "John Smith"
    john.role = "CEO & Founder"
    john.bio = "30+ years of expertise in custom industrial packaging solutions and international shipping."
    john.order = 1
    john.is_active = True

    sarah = TeamMember()
    sarah.name = "Sarah Johnson"
    sarah.role = "Operations Director"
    sarah.bio = "25+ years of manufacturing and industrial packaging operations expertise."
    sarah.order = 2
    sarah.is_active = True

    michael = TeamMember()
    michael.name = "Michael Brown"
    michael.role = "Engineering Manager"
    michael.bio = "20+ years of custom wood crating and export packaging design experience."
    michael.order = 3
    michael.is_active = True

    sample_team = [john, sarah, michael]
    for member in sample_team:
        db.session.add(member)
    db.session.commit()
    print("Team members added successfully!")
