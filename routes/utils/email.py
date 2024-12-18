from flask import current_app
from extensions import mail
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_mail import Message

def send_test_email():
    """Send a test email to verify configuration."""
    try:
        # First test the connection
        if not test_email_connection():
            raise Exception("Failed to establish email connection")

        # Create the message
        msg = Message(
            subject="Test Email - Wood Products Unlimited",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
            recipients=["chris.candelora@gmail.com"],
            body="This is a test email to verify the email configuration is working.",
            html="<h1>Test Email</h1><p>This is a test email to verify the email configuration is working.</p>"
        )

        current_app.logger.info('Attempting to send test email...')
        
        # Try sending with Flask-Mail
        try:
            # Get the mail instance from current_app
            if not hasattr(current_app, 'extensions') or 'mail' not in current_app.extensions:
                raise Exception("Mail extension not properly initialized")
            
            mail.send(msg)
            current_app.logger.info('Test email sent successfully using Flask-Mail')
            return True, "Test email sent successfully"
        except Exception as mail_error:
            current_app.logger.error(f'Flask-Mail send failed: {str(mail_error)}')
            
            # Fallback to direct SMTP
            try:
                with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                    server.set_debuglevel(1)  # Enable SMTP debug output
                    if current_app.config['MAIL_USE_TLS']:
                        server.starttls()
                    server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                    
                    # Create message
                    message = MIMEMultipart('alternative')
                    message['Subject'] = msg.subject
                    message['From'] = current_app.config['MAIL_DEFAULT_SENDER']
                    message['To'] = msg.recipients[0]
                    message.attach(MIMEText(msg.html, 'html'))
                    
                    # Send email
                    server.send_message(message)
                    current_app.logger.info('Test email sent successfully using direct SMTP')
                    return True, "Test email sent successfully using direct SMTP"
            except Exception as smtp_error:
                error_msg = f"Both Flask-Mail and direct SMTP failed. Last error: {str(smtp_error)}"
                current_app.logger.error(error_msg)
                return False, error_msg
    except Exception as e:
        error_msg = f"Error sending test email: {str(e)}"
        current_app.logger.error(error_msg)
        return False, error_msg

def test_email_connection():
    """Test the email connection and configuration."""
    try:
        current_app.logger.info('Testing email connection...')
        current_app.logger.info(f'Server: {current_app.config["MAIL_SERVER"]}')
        current_app.logger.info(f'Port: {current_app.config["MAIL_PORT"]}')
        current_app.logger.info(f'Username: {current_app.config["MAIL_USERNAME"]}')
        
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
            server.set_debuglevel(1)  # Enable SMTP debug output
            if current_app.config['MAIL_USE_TLS']:
                current_app.logger.info('Starting TLS...')
                server.starttls()
            current_app.logger.info('Attempting login...')
            server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
            current_app.logger.info('Email connection test successful')
            return True
    except Exception as e:
        current_app.logger.error(f'Email connection test failed: {str(e)}')
        return False

def send_contact_email(form_data):
    try:
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not form_data.get(field):
                raise ValueError(f'Missing required field: {field}')

        # Log configuration and attempt
        current_app.logger.info('Email Configuration:')
        current_app.logger.info(f'MAIL_SERVER: {current_app.config.get("MAIL_SERVER")}')
        current_app.logger.info(f'MAIL_PORT: {current_app.config.get("MAIL_PORT")}')
        current_app.logger.info(f'MAIL_USE_TLS: {current_app.config.get("MAIL_USE_TLS")}')
        current_app.logger.info(f'MAIL_USERNAME: {current_app.config.get("MAIL_USERNAME")}')
        current_app.logger.info(f'MAIL_DEFAULT_SENDER: {current_app.config.get("MAIL_DEFAULT_SENDER")}')
        
        # Test connection first
        if not test_email_connection():
            raise Exception("Failed to establish email connection. Please check email server settings.")

        current_app.logger.info('Attempting to send contact email')
        msg = Message(
            subject="New Contact Form Submission - Wood Products Unlimited",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
            recipients=["info@woodproductsunlimited.com"],
            html=f"""
            <h2>New Contact Form Submission</h2>
            <h3>Contact Information:</h3>
            <ul>
                <li><strong>Name:</strong> {form_data['name']}</li>
                <li><strong>Email:</strong> {form_data['email']}</li>
                <li><strong>Company:</strong> {form_data.get('company', 'Not provided')}</li>
                <li><strong>Industry:</strong> {form_data.get('industry', 'Not provided')}</li>
                <li><strong>Package Type:</strong> {form_data.get('package_type', 'Not provided')}</li>
            </ul>
            <h3>Message:</h3>
            <p>{form_data['message']}</p>
            """
        )
        current_app.logger.debug(f'Email message created with subject: {msg.subject}')
        
        try:
            mail.send(msg)
            current_app.logger.info('Contact email sent successfully using Flask-Mail')
        except Exception as mail_error:
            current_app.logger.error(f'Flask-Mail send failed: {str(mail_error)}')
            
            # Log detailed error information
            current_app.logger.error('Flask-Mail Configuration:')
            for key in current_app.config:
                if key.startswith('MAIL_') and 'PASSWORD' not in key:
                    current_app.logger.error(f'{key}: {current_app.config[key]}')
            
            # Fallback to direct SMTP if Flask-Mail fails
            current_app.logger.info('Attempting fallback to direct SMTP...')
            try:
                with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                    server.set_debuglevel(1)  # Enable SMTP debug output
                    if current_app.config['MAIL_USE_TLS']:
                        server.starttls()
                    server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                    
                    # Create message
                    message = MIMEMultipart('alternative')
                    message['Subject'] = msg.subject
                    message['From'] = current_app.config['MAIL_DEFAULT_SENDER']
                    message['To'] = msg.recipients[0]
                    message.attach(MIMEText(msg.html, 'html'))
                    
                    # Send email
                    server.send_message(message)
                    current_app.logger.info('Contact email sent successfully using direct SMTP')
            except Exception as smtp_error:
                current_app.logger.error(f'Direct SMTP send failed: {str(smtp_error)}')
                raise Exception(f'Both Flask-Mail and direct SMTP failed. Last error: {str(smtp_error)}')
                
    except Exception as e:
        current_app.logger.error(f'Error sending contact email: {str(e)}')
        current_app.logger.exception('Full traceback:')
        raise

def send_quote_email(form_data):
    try:
        # Test connection first
        if not test_email_connection():
            raise Exception("Failed to establish email connection")

        current_app.logger.info('Attempting to send quote email')
        package_types = {
            'export_crate': 'ISPM 15 Export Crate',
            'cushioned_crate': 'Cushioned Crate',
            'skidmate': 'Export Skidmate',
            'cushion_skid': 'Cushion Skid with Ramp',
            'oversize': 'Oversize Crate'
        }

        requirement_names = {
            'moisture_barrier': 'Moisture Barrier Protection',
            'shock_absorption': 'Shock Absorption System',
            'custom_foam': 'Custom Foam Interior',
            'ramp_system': 'Loading Ramp System'
        }

        requirements_html = ""
        if form_data.get('requirements'):
            requirements_html = "<h3>Special Requirements:</h3><ul>"
            for req in form_data['requirements']:
                requirements_html += f"<li>{requirement_names.get(req, req)}</li>"
            requirements_html += "</ul>"

        # Format dimensions
        dimensions = f"{form_data.get('length', 'N/A')}L x {form_data.get('width', 'N/A')}W x {form_data.get('height', 'N/A')}H"
        
        # Format shipping type
        shipping_type = form_data.get('shipping_type', 'Not provided').capitalize()

        msg = Message(
            subject="New Quote Request - Wood Products Unlimited",
            sender=current_app.config.get('MAIL_DEFAULT_SENDER'),
            recipients=["info@woodproductsunlimited.com"],
            html=f"""
            <h2>New Quote Request</h2>
            <h3>Contact Information:</h3>
            <ul>
                <li><strong>Name:</strong> {form_data.get('name', 'Not provided')}</li>
                <li><strong>Email:</strong> {form_data.get('email', 'Not provided')}</li>
                <li><strong>Phone:</strong> {form_data.get('phone', 'Not provided')}</li>
            </ul>
            <h3>Package Details:</h3>
            <ul>
                <li><strong>Package Type:</strong> {package_types.get(form_data.get('package_type', ''), 'Not provided')}</li>
                <li><strong>Dimensions:</strong> {dimensions}</li>
                <li><strong>Weight:</strong> {form_data.get('weight', 'Not provided')} lbs</li>
                <li><strong>Shipping Type:</strong> {shipping_type}</li>
            </ul>
            {requirements_html}
            <h3>Special Instructions:</h3>
            <p>{form_data.get('special_instructions', 'None provided')}</p>
            """
        )
        
        try:
            mail.send(msg)
            current_app.logger.info('Quote email sent successfully using Flask-Mail')
        except Exception as mail_error:
            current_app.logger.error(f'Flask-Mail send failed: {str(mail_error)}')
            
            # Fallback to direct SMTP
            try:
                with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as server:
                    server.set_debuglevel(1)  # Enable SMTP debug output
                    if current_app.config['MAIL_USE_TLS']:
                        server.starttls()
                    server.login(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
                    
                    # Create message
                    message = MIMEMultipart('alternative')
                    message['Subject'] = msg.subject
                    message['From'] = current_app.config['MAIL_DEFAULT_SENDER']
                    message['To'] = msg.recipients[0]
                    message.attach(MIMEText(msg.html, 'html'))
                    
                    # Send email
                    server.send_message(message)
                    current_app.logger.info('Quote email sent successfully using direct SMTP')
            except Exception as smtp_error:
                current_app.logger.error(f'Direct SMTP send failed: {str(smtp_error)}')
                raise Exception(f'Both Flask-Mail and direct SMTP failed. Last error: {str(smtp_error)}')
                
    except Exception as e:
        current_app.logger.error(f'Error sending quote email: {str(e)}')
        current_app.logger.exception('Full traceback:')
        raise