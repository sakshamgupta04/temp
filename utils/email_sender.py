import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
import os

class EmailSender:
    def __init__(self, smtp_server: str, smtp_port: int, 
                 email_address: str, email_password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email_address = email_address
        self.email_password = email_password
    
    def send_confirmation_email(self, recipient_email: str, 
                                candidate_name: str,
                                test_token: str,
                                personality_test_url: str = "http://localhost:8502") -> bool:
        """Send initial confirmation email with personality test link"""
        
        subject = "Application Received - Complete Your Personality Test | people.ai"
        
        # Create test link with token
        personality_test_link = f"{personality_test_url}?token={test_token}"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #667eea; text-align: center;">people.ai</h2>
                <h3>Hello {candidate_name},</h3>
                
                <p>Thank you for submitting your application! We have successfully received and processed your resume.</p>
                
                <p><strong>✅ Application Status:</strong> Preliminary review complete</p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                
                <h3 style="color: #667eea;">🧠 Next Step: Complete Your Personality Assessment</h3>
                
                <p>To finalize your application, please complete our Big Five personality test:</p>
                
                <ul style="color: #666; margin: 15px 0;">
                    <li>📝 50 questions about your personality traits</li>
                    <li>⏱️ Takes approximately 10 minutes</li>
                    <li>🎯 No right or wrong answers - just be honest</li>
                    <li>📊 Your final fitment score will be calculated automatically</li>
                </ul>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{personality_test_link}" 
                       style="background-color: #667eea; color: white; padding: 15px 40px; 
                              text-decoration: none; border-radius: 10px; display: inline-block; font-weight: 600; font-size: 16px;">
                        🧠 Start Personality Test
                    </a>
                </div>
                
                <p style="background-color: #f0f4ff; padding: 15px; border-radius: 8px; border-left: 4px solid #667eea;">
                    <strong>💡 Why This Test?</strong><br>
                    The Big Five personality assessment helps us understand your work style, communication preferences, 
                    and how you might fit within our team culture. This ensures a better match for both you and us!
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                
                <p><strong>🔗 Your Personal Test Link:</strong></p>
                <p style="background-color: #f5f5f5; padding: 12px; border-radius: 5px; font-family: monospace; word-break: break-all; font-size: 13px;">
                    {personality_test_link}
                </p>
                <p style="color: #666; font-size: 13px;">
                    💾 Save this link - you can complete the test anytime within the next 7 days.
                </p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                
                <h4 style="color: #667eea;">What Happens After?</h4>
                <ol style="color: #666;">
                    <li>Complete the personality test</li>
                    <li>Your final fitment score will be calculated</li>
                    <li>Receive detailed results via email</li>
                    <li>Our team reviews your complete profile</li>
                    <li>We contact you if there's a match (5-7 business days)</li>
                </ol>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                
                <p style="color: #888; font-size: 12px; text-align: center;">
                    This is an automated email from people.ai recruitment system.<br>
                    Need help? Reply to this email and we'll assist you.<br><br>
                    © 2025 people.ai - AI-Powered Recruitment
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, body)
    
    def send_fitment_score_email(self, recipient_email: str, 
                                  candidate_name: str,
                                  score_data: Dict[str, Any]) -> bool:
        """Send final fitment score results to candidate"""
        
        subject = f"Your Final Fitment Score: {score_data['overall_fitment_score']:.0f}/100 | people.ai"
        
        # Determine score color and label
        score = score_data['overall_fitment_score']
        if score >= 80:
            score_color = "#10B981"  # Green
            score_label = "Excellent Fit! 🌟"
            score_emoji = "🏆"
        elif score >= 60:
            score_color = "#F59E0B"  # Orange
            score_label = "Good Fit! 👍"
            score_emoji = "✨"
        else:
            score_color = "#6B7280"  # Gray
            score_label = "Developing Profile"
            score_emoji = "📈"
        
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #667eea; text-align: center;">people.ai</h2>
                <h3>Hello {candidate_name},</h3>
                
                <p>Thank you for completing your personality assessment! 🎉</p>
                <p>We've calculated your final fitment score based on your profile and personality traits.</p>
                
                <hr style="border: none; border-top: 2px solid #667eea; margin: 20px 0;">
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 15px; text-align: center; color: white; margin: 20px 0;">
                    <h2 style="margin: 0; opacity: 0.9; font-size: 18px;">Your Final Fitment Score</h2>
                    <h1 style="font-size: 56px; margin: 15px 0; font-weight: 800;">{score_emoji} {score_data['overall_fitment_score']:.0f}/100</h1>
                    <h3 style="margin: 0; font-size: 20px;">{score_label}</h3>
                    <p style="margin-top: 10px; opacity: 0.9;">Category: <strong>{score_data['category']}</strong></p>
                </div>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                
                <h3 style="color: #667eea;">📊 Score Breakdown</h3>
                
                <div style="background-color: #f9fafb; padding: 20px; border-radius: 10px; margin: 15px 0;">
                    <table style="width: 100%; border-collapse: collapse;">
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 10px 0;"><strong>Dataset Score:</strong></td>
                            <td style="text-align: right; padding: 10px 0;"><strong>{score_data['fitment_score']:.2f}/100</strong></td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 10px 0; color: #666; font-size: 13px;">
                                Based on experience, education, research & achievements
                            </td>
                            <td style="text-align: right; padding: 10px 0; color: #666; font-size: 13px;">
                                {score_data['breakdown']['dataset_contribution']}
                            </td>
                        </tr>
                        <tr style="border-bottom: 1px solid #e5e7eb;">
                            <td style="padding: 10px 0;"><strong>Personality Score:</strong></td>
                            <td style="text-align: right; padding: 10px 0;"><strong>{score_data['big5_score']:.2f}/100</strong></td>
                        </tr>
                        <tr>
                            <td style="padding: 10px 0; color: #666; font-size: 13px;">
                                Based on Big Five personality traits
                            </td>
                            <td style="text-align: right; padding: 10px 0; color: #666; font-size: 13px;">
                                {score_data['breakdown']['big5_contribution']}
                            </td>
                        </tr>
                    </table>
                </div>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                
                <h3 style="color: #667eea;">🧬 Your Personality Profile</h3>
                <p style="color: #666; font-size: 14px;">Based on the Big Five personality model:</p>
                
                <div style="background-color: #f9fafb; padding: 15px; border-radius: 10px; margin: 15px 0;">
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span><strong>🎨 Openness</strong></span>
                            <span><strong>{score_data['big5_trait_scores']['O'] * 100:.0f}%</strong></span>
                        </div>
                        <div style="background: #e5e7eb; height: 8px; border-radius: 4px;">
                            <div style="background: #667eea; width: {score_data['big5_trait_scores']['O'] * 100:.0f}%; height: 8px; border-radius: 4px;"></div>
                        </div>
                    </div>
                    
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span><strong>📋 Conscientiousness</strong></span>
                            <span><strong>{score_data['big5_trait_scores']['C'] * 100:.0f}%</strong></span>
                        </div>
                        <div style="background: #e5e7eb; height: 8px; border-radius: 4px;">
                            <div style="background: #667eea; width: {score_data['big5_trait_scores']['C'] * 100:.0f}%; height: 8px; border-radius: 4px;"></div>
                        </div>
                    </div>
                    
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span><strong>🎤 Extraversion</strong></span>
                            <span><strong>{score_data['big5_trait_scores']['E'] * 100:.0f}%</strong></span>
                        </div>
                        <div style="background: #e5e7eb; height: 8px; border-radius: 4px;">
                            <div style="background: #667eea; width: {score_data['big5_trait_scores']['E'] * 100:.0f}%; height: 8px; border-radius: 4px;"></div>
                        </div>
                    </div>
                    
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span><strong>🤝 Agreeableness</strong></span>
                            <span><strong>{score_data['big5_trait_scores']['A'] * 100:.0f}%</strong></span>
                        </div>
                        <div style="background: #e5e7eb; height: 8px; border-radius: 4px;">
                            <div style="background: #667eea; width: {score_data['big5_trait_scores']['A'] * 100:.0f}%; height: 8px; border-radius: 4px;"></div>
                        </div>
                    </div>
                    
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                            <span><strong>😌 Emotional Stability</strong></span>
                            <span><strong>{score_data['big5_trait_scores']['N'] * 100:.0f}%</strong></span>
                        </div>
                        <div style="background: #e5e7eb; height: 8px; border-radius: 4px;">
                            <div style="background: #667eea; width: {score_data['big5_trait_scores']['N'] * 100:.0f}%; height: 8px; border-radius: 4px;"></div>
                        </div>
                    </div>
                </div>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                
                <div style="background-color: #EEF2FF; padding: 20px; border-radius: 10px; border-left: 4px solid #667eea;">
                    <h4 style="margin: 0 0 10px 0; color: #667eea;">📬 What's Next?</h4>
                    <p style="margin: 5px 0;">
                        ✅ Your complete application has been received<br>
                        📊 Our team will review your fitment score and profile<br>
                        📞 If your profile matches our requirements, we'll contact you within <strong>5-7 business days</strong><br>
                        💼 We'll discuss potential opportunities and next steps
                    </p>
                </div>
                
                <p style="margin-top: 20px;">Thank you for your interest in joining our team. We appreciate the time you took to complete your application!</p>
                
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
                
                <p style="color: #888; font-size: 12px; text-align: center;">
                    This is an automated email from people.ai recruitment system.<br>
                    Questions? Reply to this email and we'll be happy to help.<br><br>
                    © 2025 people.ai - AI-Powered Recruitment
                </p>
            </div>
        </body>
        </html>
        """
        
        return self._send_email(recipient_email, subject, body)
    
    def _send_email(self, recipient: str, subject: str, body: str) -> bool:
        """Internal method to send email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_address
            msg['To'] = recipient
            msg['Subject'] = subject
            
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False
    
    def send_comprehensive_results_email(self, recipient_email: str,
                                    candidate_name: str,
                                    fitment_data: Dict[str, Any],
                                    big5_scores: Dict[str, int],
                                    retention_data: Dict[str, Any]) -> bool:
        """Send comprehensive final results with fitment, personality, and retention analysis"""
    
        fitment_score = fitment_data['overall_fitment_score']
        retention_score = retention_data['retention_score']
        retention_risk = retention_data['retention_risk']
    
        subject = f"Complete Assessment Results: Fitment {fitment_score:.0f}/100 | {retention_risk} Retention Risk | people.ai"
    
        # Color coding
        fitment_color = "#10B981" if fitment_score >= 70 else ("#F59E0B" if fitment_score >= 50 else "#6B7280")
        retention_color = "#10B981" if retention_risk == 'Low' else ("#F59E0B" if retention_risk == 'Medium' else "#EF4444")
    
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 700px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
                <h2 style="color: #667eea; text-align: center;">people.ai</h2>
                <h3>Complete Assessment Results for {candidate_name}</h3>
            
                <p>Thank you for completing your comprehensive assessment! Below is your complete profile analysis.</p>
            
                <hr style="border: none; border-top: 2px solid #667eea; margin: 25px 0;">
            
                <!-- FITMENT SCORE -->
                <div style="background: linear-gradient(135deg, {fitment_color} 0%, {fitment_color}dd 100%); padding: 25px; border-radius: 15px; text-align: center; color: white; margin: 20px 0;">
                    <h2 style="margin: 0; opacity: 0.9;">Final Fitment Score</h2>
                    <h1 style="font-size: 48px; margin: 15px 0;">{fitment_score:.0f}/100</h1>
                    <h3>{fitment_data['category']}</h3>
                </div>
            
                <!-- BIG FIVE PERSONALITY -->
                <h3 style="color: #667eea; margin-top: 30px;">🧬 Personality Profile (Big Five)</h3>
                <table style="width: 100%; border-collapse: collapse; margin: 15px 0;">
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 10px;">🎨 Openness</td>
                    <td style="text-align: right; padding: 10px;"><strong>{big5_scores['openness']}/40</strong></td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 10px;">📋 Conscientiousness</td>
                    <td style="text-align: right; padding: 10px;"><strong>{big5_scores['conscientiousness']}/40</strong></td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 10px;">🎤 Extraversion</td>
                    <td style="text-align: right; padding: 10px;"><strong>{big5_scores['extraversion']}/40</strong></td>
                    </tr>
                    <tr style="border-bottom: 1px solid #e5e7eb;">
                    <td style="padding: 10px;">🤝 Agreeableness</td>
                    <td style="text-align: right; padding: 10px;"><strong>{big5_scores['agreeableness']}/40</strong></td>
                    </tr>
                    <tr>
                    <td style="padding: 10px;">😌 Emotional Stability</td>
                    <td style="text-align: right; padding: 10px;"><strong>{40 - big5_scores['neuroticism']}/40</strong></td>
                    </tr>
                </table>
            
                <!-- RETENTION ANALYSIS -->
                <h3 style="color: #667eea; margin-top: 30px;">📊 Retention Risk Analysis</h3>
                <div style="background-color: #f9fafb; padding: 20px; border-radius: 10px; border-left: 4px solid {retention_color};">
                    <p style="margin: 5px 0;"><strong>Retention Score:</strong> {retention_score}/100</p>
                    <p style="margin: 5px 0;"><strong>Risk Level:</strong> <span style="color: {retention_color}; font-weight: bold;">{retention_risk} Risk</span></p>
                    <p style="margin: 5px 0;"><strong>Risk Flags:</strong> {retention_data['flag_count']}</p>
                </div>
            
                <div style="margin: 15px 0;">
                    <strong>Component Scores:</strong>
                    <ul style="color: #666;">
                        <li>Job Stability: {retention_data['component_scores']['stability']}/100</li>
                        <li>Personality Fit: {retention_data['component_scores']['personality']}/100</li>
                        <li>Professional Engagement: {retention_data['component_scores']['engagement']}/100</li>
                        <li>Fitment Factor: {retention_data['component_scores']['fitment_factor']}/100</li>
                    </ul>
                </div>
            
                {f'''
                <div style="background-color: #FEF3C7; padding: 15px; border-radius: 8px; margin: 15px 0;">
                    <strong>⚠️ Risk Flags Identified:</strong>
                    <ul style="margin: 10px 0; color: #92400E;">
                    {''.join([f'<li>{flag}</li>' for flag in retention_data['risk_flags']])}
                    </ul>
                </div>
                ''' if retention_data['risk_flags'] else ''}
            
                <div style="background-color: #EEF2FF; padding: 20px; border-radius: 10px; margin: 20px 0;">
                    <h4 style="margin: 0 0 10px 0;">📝 Key Recommendations:</h4>
                    <ul style="margin: 0; color: #4338CA;">
                    {''.join([f'<li style="margin: 5px 0;">{insight}</li>' for insight in retention_data['insights'][:5]])}
                    </ul>
                </div>
            
                <hr style="border: none; border-top: 1px solid #ddd; margin: 25px 0;">
            
                <div style="background-color: #DBEAFE; padding: 15px; border-radius: 10px;">
                    <p style="margin: 0;"><strong>📬 What's Next?</strong></p>
                    <p style="margin: 10px 0 0 0;">
                    Our recruitment team will review your complete profile. If your qualifications match our current requirements, we'll contact you within 5-7 business days to discuss potential opportunities.
                    </p>
                </div>
            
                <p style="margin-top: 20px;">Thank you for your interest in joining our team. We appreciate the time and effort you invested in this comprehensive assessment!</p>
            
                <hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
            
                <p style="color: #888; font-size: 12px; text-align: center;">
                © 2025 people.ai - AI-Powered Recruitment<br>
                Questions? Reply to this email for assistance.
                </p>
            </div>
        </body>
        </html>
        """
    
        return self._send_email(recipient_email, subject, body)