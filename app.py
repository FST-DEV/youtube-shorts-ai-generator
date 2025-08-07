from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import threading
import time
from datetime import datetime
import zipfile
import io
from ai_agent import AIContentAgent

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')

# Global variables to track generation status
generation_status = {}
generation_results = {}

class WebAIAgent(AIContentAgent):
    """Extended AI Agent for web interface"""
    
    def __init__(self, session_id):
        super().__init__()
        self.session_id = session_id
        self.progress = 0
        self.status = "Initializing..."
        self.generated_files = []
        
    def update_progress(self, progress, status):
        """Update progress for web interface"""
        self.progress = progress
        self.status = status
        generation_status[self.session_id] = {
            'progress': progress,
            'status': status,
            'timestamp': datetime.now().isoformat()
        }
    
    def process_topic_web(self, topic: str):
        """Web-adapted version of process_topic"""
        try:
            self.update_progress(10, f"Starting content generation for: {topic}")
            
            # Step 1: Generate content
            self.update_progress(25, "Generating YouTube Shorts script...")
            content = self.generate_text_content(topic)
            
            # Step 2: Extract image prompts
            self.update_progress(40, "Extracting image prompts...")
            image_prompts = self.extract_image_prompts(content)
            
            # Step 3: Generate images
            self.update_progress(50, "Generating images...")
            image_files = []
            max_images = min(len(image_prompts), 3)
            
            for i, prompt in enumerate(image_prompts[:max_images], 1):
                self.update_progress(50 + (30 * i / max_images), f"Generating image {i}/{max_images}...")
                
                enhanced_prompt = f"{prompt}, 9:16 aspect ratio, vertical orientation, YouTube Shorts style"
                filename = f"static/generated/youtube_shorts_image_{i}_{int(time.time())}.png"
                
                # Ensure directory exists
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                
                if self.generate_image(enhanced_prompt, filename):
                    image_files.append(filename)
                    self.generated_files.append(filename)
                time.sleep(2)
            
            # Step 4: Save content
            self.update_progress(90, "Saving content...")
            content_filename = f"static/generated/content_{int(time.time())}.txt"
            with open(content_filename, 'w', encoding='utf-8') as f:
                f.write(content)
            self.generated_files.append(content_filename)
            
            # Store results
            generation_results[self.session_id] = {
                'topic': topic,
                'content': content,
                'image_files': image_files,
                'content_file': content_filename,
                'generated_at': datetime.now().isoformat(),
                'success': True
            }
            
            self.update_progress(100, f"✅ Successfully generated content for '{topic}'!")
            
        except Exception as e:
            self.update_progress(0, f"❌ Error: {str(e)}")
            generation_results[self.session_id] = {
                'success': False,
                'error': str(e)
            }

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_content():
    """Start content generation"""
    data = request.get_json()
    topic = data.get('topic', '').strip()
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
    
    # Create session ID
    session_id = f"gen_{int(time.time())}"
    
    # Initialize status
    generation_status[session_id] = {
        'progress': 0,
        'status': 'Starting...',
        'timestamp': datetime.now().isoformat()
    }
    
    # Start generation in background thread
    agent = WebAIAgent(session_id)
    thread = threading.Thread(target=agent.process_topic_web, args=(topic,))
    thread.daemon = True
    thread.start()
    
    return jsonify({
        'session_id': session_id,
        'status': 'Generation started'
    })

@app.route('/status/<session_id>')
def get_status(session_id):
    """Get generation status"""
    status = generation_status.get(session_id, {
        'progress': 0,
        'status': 'Session not found',
        'timestamp': datetime.now().isoformat()
    })
    return jsonify(status)

@app.route('/result/<session_id>')
def get_result(session_id):
    """Get generation result"""
    result = generation_results.get(session_id)
    if not result:
        return jsonify({'error': 'Result not found'}), 404
    
    if not result.get('success', False):
        return jsonify({'error': result.get('error', 'Generation failed')}), 500
    
    # Make file paths relative to static folder
    result['image_files'] = [f.replace('static/', '') for f in result['image_files']]
    result['content_file'] = result['content_file'].replace('static/', '')
    
    return jsonify(result)

@app.route('/download/<session_id>')
def download_results(session_id):
    """Download all results as ZIP"""
    result = generation_results.get(session_id)
    if not result or not result.get('success'):
        return jsonify({'error': 'No results to download'}), 404
    
    # Create ZIP file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
        # Add content file
        content_file = result['content_file'].replace('generated/', 'static/generated/')
        if os.path.exists(content_file):
            zip_file.write(content_file, f"{result['topic']}_content.txt")
        
        # Add images
        for i, img_file in enumerate(result['image_files'], 1):
            full_path = f"static/{img_file}"
            if os.path.exists(full_path):
                ext = os.path.splitext(img_file)[1]
                zip_file.write(full_path, f"{result['topic']}_image_{i}{ext}")
    
    zip_buffer.seek(0)
    
    return send_file(
        io.BytesIO(zip_buffer.getvalue()),
        mimetype='application/zip',
        as_attachment=True,
        download_name=f"{result['topic']}_youtube_shorts_{session_id}.zip"
    )

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'environment_check': {
            'hugging_face_token': '✅' if os.getenv('HUGGING_FACE_TOKEN') else '❌',
            'email_config': '✅' if os.getenv('SENDER_EMAIL') else '❌'
        }
    })

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('static/generated', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)