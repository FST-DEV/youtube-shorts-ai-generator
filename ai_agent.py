import os
import smtplib
import requests
import json
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from datetime import datetime
import re
from typing import List, Dict

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # This loads the .env file
    print("✅ .env file loaded successfully")
except ImportError:
    print("⚠️  python-dotenv not installed. Using system environment variables only.")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")
    print("Using system environment variables only.")

class AIContentAgent:
    def __init__(self):
        # Hugging Face API settings (free tier)
        self.hf_api_url_text = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
        
        # Try multiple image generation models for better success rate
        self.image_models = [
            # FLUX models (newer, high quality)
    "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell",
    "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev",
    
    # Stable Diffusion variants
    "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
    "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1",
    "https://api-inference.huggingface.co/models/CompVis/stable-diffusion-v1-4",
    "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0",
    
    # Alternative models
    "https://api-inference.huggingface.co/models/prompthero/openjourney-v4",
    "https://api-inference.huggingface.co/models/wavymulder/Analog-Diffusion",
    "https://api-inference.huggingface.co/models/nitrosocke/Ghibli-Diffusion",
    
    # Anime/Illustration styles
    "https://api-inference.huggingface.co/models/hakurei/waifu-diffusion",
    "https://api-inference.huggingface.co/models/andite/anything-v4.0",
        ]
            # "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5",
        self.current_model_index = 0
        
        # Get Hugging Face token from environment variable
        self.hf_token = os.getenv('HUGGING_FACE_TOKEN')
        if not self.hf_token:
            print("Please set HUGGING_FACE_TOKEN environment variable")
            
        # Email settings
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_password = os.getenv('SENDER_APP_PASSWORD')  # Gmail app password
        
        # Handle multiple recipients - can be comma-separated
        recipients_env = os.getenv('RECIPIENT_EMAILS', '')
        if recipients_env:
            # Split by comma and clean up whitespace
            self.recipient_emails = [email.strip() for email in recipients_env.split(',') if email.strip()]
        else:
            # Fallback to single recipient for backward compatibility
            single_recipient = os.getenv('RECIPIENT_EMAIL', '')
            self.recipient_emails = [single_recipient] if single_recipient else []
        
        # Headers for API requests
        self.headers = {"Authorization": f"Bearer {self.hf_token}"}
        
    def generate_text_content(self, topic: str) -> str:
        """Generate text content using Hugging Face free models"""
        
        # Predefined prompt template
        prompt = f"""
        Create comprehensive content about: {topic}

        Please include the following sections:
        1. Introduction and overview
        2. Key concepts and definitions
        3. Main benefits or applications
        4. Step-by-step guide or process
        5. Tips and best practices
        6. Common challenges and solutions
        7. Future trends and developments
        8. Conclusion

        Also, please include 3 image generation prompts in the following format:
        [IMAGE_PROMPT: detailed description for image 1]
        [IMAGE_PROMPT: detailed description for image 2] 
        [IMAGE_PROMPT: detailed description for image 3]

        Make the content informative, engaging, and well-structured.
        """
        
        try:
            # Using a more suitable text generation model
            text_model_url = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 1000,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(text_model_url, headers=self.headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    return generated_text
                else:
                    return f"Generated content about {topic} (simplified due to API limitations)"
            else:
                print(f"Text generation failed: {response.status_code}")
                return self.generate_fallback_content(topic)
                
        except Exception as e:
            print(f"Error generating text: {e}")
            return self.generate_fallback_content(topic)
    
    def generate_fallback_content(self, topic: str) -> str:
        """Generate YouTube Shorts fallback content when API fails"""
        return f"""
        🧠 **VIDEO SCRIPT: 5 Interesting and Unknown Facts About {topic}**

        **HOOK (0-10 seconds):**
        "You think you know {topic}? Think again! Here are 5 mind-blowing facts that will change everything you thought you knew!"

        **FACT 1:**
        Did you know that {topic} has some incredibly surprising origins? Most people have no idea about this fascinating backstory. This little-known detail will completely shift your perspective on {topic}.

        **FACT 2:**
        Here's something that will blow your mind about {topic}. Scientists recently discovered something amazing that challenges everything we thought we knew. This discovery has completely revolutionized our understanding.

        **FACT 3:**
        The most shocking thing about {topic}? It's connected to something you'd never expect! This incredible connection shows just how mysterious and fascinating {topic} really is.

        **FACT 4:**
        You won't believe this crazy fact about {topic}. It's so unbelievable that when researchers first discovered it, they thought it was a mistake! But it turns out to be absolutely true.

        **FACT 5:**
        And finally, here's the most mind-bending fact of all. {topic} has this incredible ability that sounds like science fiction but is completely real. This will leave you questioning everything!

        **OUTRO:**
        "Which fact shocked you the most? Drop it in the comments and follow for more incredible facts that will blow your mind!"

        🖼️ **AI IMAGE GENERATION PROMPTS:**

        [IMAGE_PROMPT: Cinematic 9:16 vertical shot of a person with shocked expression, dramatic lighting, colorful background with question marks floating, YouTube Shorts style thumbnail, hyper-realistic, vibrant colors]

        [IMAGE_PROMPT: Dynamic 9:16 vertical illustration showing {topic} with mysterious glowing effects, cinematic composition, dramatic lighting, detailed and colorful, science fiction aesthetic]

        [IMAGE_PROMPT: Stunning 9:16 vertical visualization of {topic} with futuristic elements, neon colors, high-tech background, cinematic depth of field, visually striking composition]

        [IMAGE_PROMPT: Dramatic 9:16 vertical scene depicting {topic} in an unexpected context, cinematic lighting, vibrant colors, detailed environment, surprising visual elements]

        [IMAGE_PROMPT: Eye-catching 9:16 vertical image of {topic} with scientific elements, glowing effects, modern design, colorful background, high detail and contrast]

        [IMAGE_PROMPT: Amazing 9:16 vertical composition showing the incredible nature of {topic}, cinematic style, brilliant colors, detailed textures, visually stunning effects]

        [IMAGE_PROMPT: Engaging 9:16 vertical image with excited person pointing at {topic}, bright colors, dynamic composition, YouTube Shorts style, call-to-action elements]

        🎬 **YOUTUBE SHORTS TITLE:**
        "5 SHOCKING {topic.upper()} Facts That Will Blow Your Mind! 🤯"

        📄 **VIDEO DESCRIPTION:**
        Discover 5 incredible and unknown facts about {topic} that will completely change how you see it! These surprising discoveries will leave you amazed and wanting more.

        Follow for more mind-blowing facts and amazing discoveries! 🚀

        🏷️ **META TAGS / HASHTAGS:**
        #shorts #{topic.lower().replace(' ', '')}facts #{topic.lower().replace(' ', '')}shorts #{topic.lower().replace(' ', '')}trivia #didyouknow #amazingfacts #mindblowing #shocking #incredible #science #discovery #educational #viral #trending #curiousfacts #unbelievable
        """

    def extract_image_prompts(self, content: str) -> List[str]:
        """Extract image prompts from the generated content"""
        pattern = r'\[IMAGE_PROMPT:\s*(.*?)\]'
        prompts = re.findall(pattern, content, re.IGNORECASE)
        return prompts

    def generate_image(self, prompt: str, filename: str) -> bool:
        """Generate image using Hugging Face Stable Diffusion with fallback models"""
        
        for attempt in range(len(self.image_models)):
            model_url = self.image_models[self.current_model_index]
            model_name = model_url.split('/')[-1]
            
            try:
                print(f"🎨 Trying model: {model_name}")
                print(f"📝 Prompt: {prompt[:100]}...")
                
                payload = {"inputs": prompt}
                
                response = requests.post(
                    model_url, 
                    headers=self.headers, 
                    json=payload,
                    timeout=60
                )
                
                print(f"📡 API Response Status: {response.status_code}")
                
                if response.status_code == 200:
                    content_type = response.headers.get('content-type', '')
                    
                    if 'image' in content_type or len(response.content) > 1000:
                        with open(filename, "wb") as f:
                            f.write(response.content)
                        
                        if os.path.exists(filename) and os.path.getsize(filename) > 1000:
                            print(f"✅ Image saved successfully: {filename}")
                            return True
                        else:
                            print(f"❌ Image file too small: {filename}")
                    else:
                        try:
                            error_data = response.json()
                            if 'estimated_time' in error_data:
                                wait_time = error_data.get('estimated_time', 20)
                                print(f"⏳ Model loading. Wait time: {wait_time}s")
                                print("💡 Trying next model...")
                            else:
                                print(f"❌ Unexpected response: {error_data}")
                        except:
                            print(f"❌ Unexpected response format")
                            
                elif response.status_code == 503:
                    print(f"⏳ Model {model_name} is loading. Trying next model...")
                elif response.status_code == 429:
                    print(f"⏰ Rate limit on {model_name}. Trying next model...")
                else:
                    try:
                        error_data = response.json()
                        print(f"❌ Error {response.status_code}: {error_data}")
                    except:
                        print(f"❌ HTTP Error {response.status_code}")
                
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout with {model_name}. Trying next model...")
            except Exception as e:
                print(f"❌ Error with {model_name}: {e}")
            
            # Try next model
            self.current_model_index = (self.current_model_index + 1) % len(self.image_models)
            if attempt < len(self.image_models) - 1:
                time.sleep(2)  # Wait before trying next model
        
        print(f"❌ All models failed for: {prompt[:50]}...")
        return False

    def create_html_content(self, topic: str, content: str, image_files: List[str]) -> str:
        """Create HTML formatted content for YouTube Shorts email"""
        
        # Parse different sections from the content
        sections = {
            'script': '',
            'title': '',
            'description': '',
            'hashtags': ''
        }
        
        # Extract sections based on emojis and markers
        current_section = 'script'
        lines = content.split('\n')
        
        for line in lines:
            if '🎬' in line or 'YOUTUBE SHORTS TITLE' in line:
                current_section = 'title'
            elif '📄' in line or 'VIDEO DESCRIPTION' in line:
                current_section = 'description'
            elif '🏷️' in line or 'META TAGS' in line or 'HASHTAGS' in line:
                current_section = 'hashtags'
            elif line.strip():
                sections[current_section] += line + '\n'
        
        # Remove image prompts from display content
        script_content = re.sub(r'\[IMAGE_PROMPT:.*?\]', '', sections['script'], flags=re.IGNORECASE)
        
        # Add image references
        image_section = ""
        for i, img_file in enumerate(image_files, 1):
            if os.path.exists(img_file):
                image_section += f'''
                <div style="margin: 15px 0; text-align: center;">
                    <h4>Generated Image {i}:</h4>
                    <img src="cid:image{i}" alt="YouTube Shorts Image {i}" style="max-width: 400px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);">
                </div>
                '''
        
        html_template = f"""
        <html>
        <head>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Arial, sans-serif; 
                    line-height: 1.6; 
                    color: #333; 
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{ 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .section {{ 
                    background: #f8f9fa;
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 10px;
                    border-left: 4px solid #667eea;
                }}
                .script {{ 
                    background: #fff3cd;
                    border-left-color: #ffc107;
                }}
                .title {{ 
                    background: #d4edda;
                    border-left-color: #28a745;
                }}
                .description {{ 
                    background: #cce5ff;
                    border-left-color: #007bff;
                }}
                .hashtags {{ 
                    background: #f8d7da;
                    border-left-color: #dc3545;
                }}
                h1 {{ color: white; margin: 0; }}
                h2 {{ color: #2c3e50; margin-top: 0; }}
                h3 {{ color: #34495e; }}
                .emoji {{ font-size: 1.2em; }}
                .timestamp {{ 
                    background: #e9ecef;
                    padding: 10px;
                    border-radius: 5px;
                    text-align: center;
                    margin-bottom: 20px;
                }}
                pre {{ 
                    white-space: pre-wrap;
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎬 YouTube Shorts Content Generated</h1>
                <h2>Topic: {topic}</h2>
            </div>
            
            <div class="timestamp">
                <strong>Generated on:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
            
            <div class="section script">
                <h2><span class="emoji">🧠</span> Video Script & Facts</h2>
                <pre>{script_content.strip()}</pre>
            </div>
            
            <div class="section title">
                <h2><span class="emoji">🎬</span> YouTube Title</h2>
                <pre>{sections['title'].strip()}</pre>
            </div>
            
            <div class="section description">
                <h2><span class="emoji">📄</span> Video Description</h2>
                <pre>{sections['description'].strip()}</pre>
            </div>
            
            <div class="section hashtags">
                <h2><span class="emoji">🏷️</span> Tags & Hashtags</h2>
                <pre>{sections['hashtags'].strip()}</pre>
            </div>
            
            <div class="section">
                <h2><span class="emoji">🖼️</span> Generated Images for Video</h2>
                <p>These images correspond to your intro, 5 facts, and outro sections:</p>
                {image_section}
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding: 20px; background: #e8f5e8; border-radius: 10px;">
                <h3>🚀 Ready for YouTube Shorts!</h3>
                <p>Your content is optimized for 2-3 minute videos with engaging visuals.</p>
                <p><em>This content was generated automatically by your AI Content Agent.</em></p>
            </div>
        </body>
        </html>
        """
        
        return html_template

    def send_email(self, topic: str, content: str, image_files: List[str]):
        """Send email with generated content and images to multiple recipients"""
        
        if not self.recipient_emails:
            print("No recipient emails configured!")
            return
            
        try:
            # Create email message
            msg = MIMEMultipart('related')
            msg['From'] = self.sender_email
            
            # Handle multiple recipients
            recipient_list = ', '.join(self.recipient_emails)
            msg['To'] = recipient_list
            msg['Subject'] = f"YouTube Shorts Content: {topic}"

            # Create HTML content
            html_content = self.create_html_content(topic, content, image_files)
            msg.attach(MIMEText(html_content, 'html'))

            # Attach images
            for i, img_file in enumerate(image_files, 1):
                if os.path.exists(img_file):
                    with open(img_file, 'rb') as f:
                        img_data = f.read()
                        image = MIMEImage(img_data)
                        image.add_header('Content-ID', f'<image{i}>')
                        msg.attach(image)

            # Send email to all recipients
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            
            # Send to all recipients at once
            server.sendmail(self.sender_email, self.recipient_emails, msg.as_string())
            server.quit()
            
            print(f"Email sent successfully to {len(self.recipient_emails)} recipient(s):")
            for email in self.recipient_emails:
                print(f"  - {email}")
            
        except Exception as e:
            print(f"Error sending email: {e}")
            print("Check your email credentials and recipient addresses.")

    def cleanup_files(self, image_files: List[str]):
        """Clean up generated image files"""
        for img_file in image_files:
            try:
                if os.path.exists(img_file):
                    os.remove(img_file)
            except:
                pass

    def process_topic(self, topic: str):
        """Main process to generate content and send email"""
        print(f"Starting YouTube Shorts content generation for topic: {topic}")
        
        # Step 1: Generate YouTube Shorts script and content
        print("Generating YouTube Shorts script with 5 facts...")
        content = self.generate_text_content(topic)
        
        # Step 2: Extract image prompts
        print("Extracting image prompts...")
        image_prompts = self.extract_image_prompts(content)
        print(f"Found {len(image_prompts)} image prompts")
        
        # Step 3: Generate images
        print("Generating images for YouTube Shorts...")
        image_files = []
        for i, prompt in enumerate(image_prompts, 1):
            print(f"Generating image {i}: {prompt[:50]}...")
            # Add 9:16 aspect ratio specification for YouTube Shorts
            enhanced_prompt = f"{prompt}, 9:16 aspect ratio, vertical orientation, cinematic quality, vibrant colors"
            filename = f"youtube_shorts_image_{i}_{int(time.time())}.png"
            if self.generate_image(enhanced_prompt, filename):
                image_files.append(filename)
                time.sleep(3)  # Slightly longer delay for better quality
            
        print(f"Generated {len(image_files)} YouTube Shorts images successfully")
        
        # Step 4: Send email
        print("Sending email...")
        self.send_email(topic, content, image_files)
        
        # Step 5: Cleanup
        print("Cleaning up temporary files...")
        self.cleanup_files(image_files)
        
        print("Process completed successfully!")

def main():
    """Main function to run the AI agent"""
    
    print("🚀 Starting AI YouTube Shorts Agent...")
    print("📁 Checking environment variables...")
    
    # Debug: Show what environment variables are found
    env_vars_found = {
        'HUGGING_FACE_TOKEN': '✅ Found' if os.getenv('HUGGING_FACE_TOKEN') else '❌ Missing',
        'SENDER_EMAIL': '✅ Found' if os.getenv('SENDER_EMAIL') else '❌ Missing', 
        'SENDER_APP_PASSWORD': '✅ Found' if os.getenv('SENDER_APP_PASSWORD') else '❌ Missing',
        'RECIPIENT_EMAILS': '✅ Found' if os.getenv('RECIPIENT_EMAILS') else '❌ Missing',
        'RECIPIENT_EMAIL': '✅ Found' if os.getenv('RECIPIENT_EMAIL') else '❌ Missing'
    }
    
    print("\n📋 Environment Variables Status:")
    for var, status in env_vars_found.items():
        print(f"   {var}: {status}")
    
    # Check required environment variables
    required_vars = ['HUGGING_FACE_TOKEN', 'SENDER_EMAIL', 'SENDER_APP_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    # Check recipient emails
    recipient_emails_env = os.getenv('RECIPIENT_EMAILS')
    recipient_email_env = os.getenv('RECIPIENT_EMAIL')
    
    if not recipient_emails_env and not recipient_email_env:
        missing_vars.append('RECIPIENT_EMAILS or RECIPIENT_EMAIL')
    
    if missing_vars:
        print("\n❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure your .env file is in the same folder as ai_agent.py")
        print("2. Check that your .env file has no extra spaces")
        print("3. Make sure .env file format is: VARIABLE_NAME=value")
        print("4. Try running: python -c \"from dotenv import load_dotenv; load_dotenv(); import os; print(os.getenv('HUGGING_FACE_TOKEN'))\"")
        return
    
    # Create agent instance
    agent = AIContentAgent()
    
    # Get topic from user input
    topic = input("Enter the topic for YouTube Shorts content generation: ").strip()
    
    if not topic:
        print("No topic provided. Exiting...")
        return
    
    # Process the topic
    agent.process_topic(topic)

if __name__ == "__main__":
    main()