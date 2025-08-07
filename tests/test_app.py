import unittest
import os
import tempfile
import json
from unittest.mock import patch, MagicMock
import sys
sys.path.append('..')

from app import app

class YouTubeShortsAITestCase(unittest.TestCase):
    
    def setUp(self):
        """Set up test client and temporary directory"""
        self.app = app.test_client()
        self.app.testing = True
        
        # Create temporary directory for generated files
        self.test_dir = tempfile.mkdtemp()
        
        # Set test environment variables
        os.environ['HUGGING_FACE_TOKEN'] = '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'
        os.environ['SENDER_EMAIL'] = 'devfst1234@gmail.com'
        os.environ['SENDER_APP_PASSWORD'] = 'ytaxjbpqtmjjzsuf'
        os.environ['RECIPIENT_EMAILS'] = 'devfst1234@gmail.com,lh3312160@gmail.com'
        os.environ['FLASK_SECRET_KEY'] = 'd4da551570cc24250f50d567f79c3431c2964445aded8bad60557b314e9c78a5'
    
    def tearDown(self):
        """Clean up after tests"""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_home_page(self):
        """Test that home page loads correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'YouTube Shorts AI Generator', response.data)
        self.assertIn(b'Generate YouTube Shorts Content', response.data)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)
        self.assertIn('environment_check', data)
    
    def test_generate_content_missing_topic(self):
        """Test generate endpoint with missing topic"""
        response = self.app.post('/generate',
                                data=json.dumps({}),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_generate_content_empty_topic(self):
        """Test generate endpoint with empty topic"""
        response = self.app.post('/generate',
                                data=json.dumps({'topic': ''}),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_generate_content_valid_topic(self):
        """Test generate endpoint with valid topic"""
        response = self.app.post('/generate',
                                data=json.dumps({'topic': 'Artificial Intelligence'}),
                                content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('session_id', data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'Generation started')
    
    def test_status_nonexistent_session(self):
        """Test status endpoint with nonexistent session"""
        response = self.app.get('/status/nonexistent_session')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['progress'], 0)
        self.assertIn('Session not found', data['status'])
    
    def test_result_nonexistent_session(self):
        """Test result endpoint with nonexistent session"""
        response = self.app.get('/result/nonexistent_session')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_download_nonexistent_session(self):
        """Test download endpoint with nonexistent session"""
        response = self.app.get('/download/nonexistent_session')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    @patch('requests.post')
    def test_ai_agent_text_generation(self, mock_post):
        """Test AI text generation functionality"""
        from ai_agent import AIContentAgent
        
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{'generated_text': 'Test content about AI'}]
        mock_post.return_value = mock_response
        
        agent = AIContentAgent()
        result = agent.generate_text_content('Artificial Intelligence')
        
        self.assertIsInstance(result, str)
        self.assertTrue(len(result) > 0)
    
    @patch('requests.post')
    def test_ai_agent_image_generation_success(self, mock_post):
        """Test AI image generation success"""
        from ai_agent import AIContentAgent
        
        # Mock successful image response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.headers = {'content-type': 'image/png'}
        mock_response.content = b'fake_image_data' * 100  # Make it larger than 1000 bytes
        mock_post.return_value = mock_response
        
        agent = AIContentAgent()
        
        # Create temporary file for test
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            result = agent.generate_image('test prompt', tmp_file.name)
            
            self.assertTrue(result)
            self.assertTrue(os.path.exists(tmp_file.name))
            
            # Clean up
            os.unlink(tmp_file.name)
    
    @patch('requests.post')
    def test_ai_agent_image_generation_failure(self, mock_post):
        """Test AI image generation failure handling"""
        from ai_agent import AIContentAgent
        
        # Mock failed API response
        mock_response = MagicMock()
        mock_response.status_code = 503
        mock_response.json.return_value = {'error': 'Model loading'}
        mock_post.return_value = mock_response
        
        agent = AIContentAgent()
        
        # Create temporary file for test
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_file:
            result = agent.generate_image('test prompt', tmp_file.name)
            
            # Should return False due to all models failing
            self.assertFalse(result)
            
            # Clean up
            if os.path.exists(tmp_file.name):
                os.unlink(tmp_file.name)
    
    def test_image_prompt_extraction(self):
        """Test extraction of image prompts from content"""
        from ai_agent import AIContentAgent
        
        agent = AIContentAgent()
        content = """
        Some text content here.
        [IMAGE_PROMPT: A beautiful landscape with mountains]
        More content.
        [IMAGE_PROMPT: A futuristic city skyline]
        Final content.
        [IMAGE_PROMPT: An abstract art piece with vibrant colors]
        """
        
        prompts = agent.extract_image_prompts(content)
        
        self.assertEqual(len(prompts), 3)
        self.assertIn('beautiful landscape', prompts[0])
        self.assertIn('futuristic city', prompts[1])
        self.assertIn('abstract art', prompts[2])
    
    def test_html_content_creation(self):
        """Test HTML content creation for email"""
        from ai_agent import AIContentAgent
        
        agent = AIContentAgent()
        topic = "Test Topic"
        content = "Test content for YouTube Shorts"
        image_files = []
        
        html = agent.create_html_content(topic, content, image_files)
        
        self.assertIn(topic, html)
        self.assertIn('YouTube Shorts Content Generated', html)
        self.assertIn('<!DOCTYPE html>', html)
        self.assertIn('</html>', html)
    
    @patch('smtplib.SMTP')
    def test_email_sending_mock(self, mock_smtp):
        """Test email sending functionality with mocking"""
        from ai_agent import AIContentAgent
        
        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        agent = AIContentAgent()
        agent.recipient_emails = ['test@example.com']
        agent.sender_email = 'sender@example.com'
        agent.sender_password = 'test_password'
        
        # This should not raise an exception
        agent.send_email('Test Topic', 'Test content', [])
        
        # Verify SMTP methods were called
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once()
        mock_server.sendmail.assert_called_once()
        mock_server.quit.assert_called_once()
    
    def test_fallback_content_generation(self):
        """Test fallback content generation"""
        from ai_agent import AIContentAgent
        
        agent = AIContentAgent()
        content = agent.generate_fallback_content('Test Topic')
        
        self.assertIn('Test Topic', content)
        self.assertIn('5 Interesting and Unknown Facts', content)
        self.assertIn('IMAGE_PROMPT:', content)
        self.assertIn('YOUTUBE SHORTS TITLE:', content)
        self.assertIn('VIDEO DESCRIPTION:', content)
        self.assertIn('META TAGS', content)

class WebIntegrationTest(unittest.TestCase):
    """Integration tests for the web interface"""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Set required environment variables
        os.environ['HUGGING_FACE_TOKEN'] = 'test_token'
        os.environ['SENDER_EMAIL'] = 'test@example.com'
        os.environ['SENDER_APP_PASSWORD'] = 'test_password'
        os.environ['RECIPIENT_EMAILS'] = 'recipient@example.com'
    
    def test_complete_workflow_mock(self):
        """Test complete workflow with mocked AI responses"""
        with patch('app.WebAIAgent') as mock_agent_class:
            # Mock the agent instance
            mock_agent = MagicMock()
            mock_agent_class.return_value = mock_agent
            
            # Start generation
            response = self.app.post('/generate',
                                    data=json.dumps({'topic': 'Test Topic'}),
                                    content_type='application/json')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            session_id = data['session_id']
            
            # Mock successful completion
            from app import generation_status, generation_results
            generation_status[session_id] = {
                'progress': 100,
                'status': 'Completed successfully',
                'timestamp': '2023-01-01T00:00:00'
            }
            
            generation_results[session_id] = {
                'success': True,
                'topic': 'Test Topic',
                'content': 'Generated content',
                'image_files': ['static/generated/test1.png'],
                'content_file': 'static/generated/content.txt',
                'generated_at': '2023-01-01T00:00:00'
            }
            
            # Check status
            status_response = self.app.get(f'/status/{session_id}')
            self.assertEqual(status_response.status_code, 200)
            status_data = json.loads(status_response.data)
            self.assertEqual(status_data['progress'], 100)
            
            # Check results
            result_response = self.app.get(f'/result/{session_id}')
            self.assertEqual(result_response.status_code, 200)
            result_data = json.loads(result_response.data)
            self.assertTrue(result_data['success'])
            self.assertEqual(result_data['topic'], 'Test Topic')

if __name__ == '__main__':

    unittest.main()
