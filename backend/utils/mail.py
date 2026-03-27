import socket
import os
import resend
from flask import current_app
from flask_mail import Message
from extensions import mail

# Fix for Render Free Tier blocking: 
# Force SMTP socket to give up in 5 seconds if using standard mail.
socket.setdefaulttimeout(5.0)

def send_otp_email(to_email: str, otp: str):
    """Send OTP verification email via Resend (Production) or Flask-Mail (Dev)."""
    print(f"[DEBUG] OTP for {to_email}: {otp}")
    
    # Priority 1: Resend (Best for Render Production)
    resend_key = current_app.config.get("RESEND_API_KEY")
    if resend_key:
        try:
            resend.api_key = resend_key
            params = {
                "from": "TrashTreasure <onboarding@resend.dev>",
                "to": [to_email],
                "subject": "TrashTreasure — Your Verification Code",
                "html": f"""
                <div style="font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 32px; background: #f8fafb; border-radius: 16px;">
                  <div style="text-align: center; margin-bottom: 24px;">
                    <span style="font-size: 48px;">♻️</span>
                    <h2 style="color: #1a1a2e; margin: 8px 0;">TrashTreasure</h2>
                    <p style="color: #6b7280; font-size: 14px;">Email Verification</p>
                  </div>
                  <div style="background: white; border-radius: 12px; padding: 32px; text-align: center; border: 1px solid #e5e7eb;">
                    <p style="color: #374151; margin: 0 0 16px;">Your verification code is:</p>
                    <div style="background: #f0fdf4; border: 2px solid #4ade80; border-radius: 12px; padding: 20px; margin: 16px 0;">
                      <span style="font-size: 36px; font-weight: bold; letter-spacing: 12px; color: #16a34a; font-family: monospace;">{otp}</span>
                    </div>
                    <p style="color: #9ca3af; font-size: 13px; margin-top: 16px;">This code expires in <strong>10 minutes</strong>.</p>
                  </div>
                </div>
                """
            }
            resend.Emails.send(params)
            print(f"[Resend] OTP sent to {to_email}")
            return True
        except Exception as e:
            print(f"[Resend Error] Failed to send: {e}")
            # Fall through to SMTP if Resend fails

    # Priority 2: Flask-Mail (SMTP fallback)
    try:
        msg = Message(
            subject="TrashTreasure — Your Verification Code",
            recipients=[to_email],
            html=f"Your code is: <b>{otp}</b>"
        )
        mail.send(msg)
        print(f"[Mail] OTP sent to {to_email}")
        return True
    except Exception as e:
        print(f"[Mail Error] Critical Failure: {e}")
        return False
