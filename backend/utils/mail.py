from flask_mail import Message
from extensions import mail


def send_otp_email(to_email: str, otp: str):
    """Send OTP verification email synchronously via Flask-Mail."""
    try:
        msg = Message(
            subject="TrashTreasure — Your Verification Code",
            recipients=[to_email],
            html=f"""
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
              <p style="color: #9ca3af; font-size: 12px; text-align: center; margin-top: 24px;">
                If you didn't request this, you can safely ignore this email.
              </p>
            </div>
            """,
        )
        mail.send(msg)
        print(f"[Mail] OTP sent to {to_email}")
        return True
    except Exception as e:
        print(f"[Mail Error] Failed to send to {to_email}: {e}")
        return False
