# 🎬 YouTube Shorts AI Generator

An AI-powered web application that generates complete YouTube Shorts content including scripts, titles, descriptions, hashtags, and vertical 9:16 images - all optimized for viral content!

![YouTube Shorts AI Generator](https://img.shields.io/badge/AI-YouTube%20Shorts-red?style=for-the-badge&logo=youtube)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Hugging Face](https://img.shields.io/badge/🤗-Hugging%20Face-yellow?style=for-the-badge)

## ✨ Features

- 🧠 **AI Script Generation**: Creates engaging 5-fact scripts optimized for YouTube Shorts
- 🖼️ **Vertical Image Generation**: Produces stunning 9:16 aspect ratio images perfect for mobile viewing
- 📱 **Mobile-First Design**: Responsive web interface that works on all devices
- 📧 **Email Integration**: Automatically sends generated content via email
- 📥 **Batch Download**: Download all content as a ZIP file
- 🚀 **One-Click Deploy**: Easy deployment to multiple platforms

## 🎯 What It Generates

For any topic you provide, the AI creates:

1. **YouTube Shorts Script** with 5 interesting facts
2. **Eye-catching Title** optimized for clicks
3. **SEO-friendly Description** with call-to-actions
4. **Trending Hashtags** for maximum reach
5. **Multiple 9:16 Images** for thumbnails and video content

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/youtube-shorts-ai-generator.git
   cd youtube-shorts-ai-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file:
   ```env
   HUGGING_FACE_TOKEN=your_hugging_face_token_here
   SENDER_EMAIL=your_email@gmail.com
   SENDER_APP_PASSWORD=your_gmail_app_password
   RECIPIENT_EMAILS=recipient1@email.com,recipient2@email.com
   FLASK_SECRET_KEY=your-secret-key-here
   
   # Optional: For enhanced image generation
   REPLICATE_API_TOKEN=your_replicate_token_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

### Docker Deployment

```bash
# Build the image
docker build -t youtube-shorts-ai .

# Run the container
docker run -p 5000:5000 --env-file .env youtube-shorts-ai
```

## 🌐 One-Click Deployments

### Deploy to Render
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Deploy to Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/youtube-shorts-ai)

### Deploy to Heroku
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

### Deploy to Vercel
```bash
npx vercel --prod
```

## 📁 Project Structure

```
youtube-shorts-ai-generator/
├── app.py                 # Flask web application
├── ai_agent.py           # Core AI agent (your existing file)
├── requirements.txt      # Python dependencies
├── Dockerfile           # Docker configuration
├── .env.example         # Environment variables template
├── templates/
│   └── index.html       # Web interface
├── static/
│   └── generated/       # Generated content storage
├── .github/
│   └── workflows/
│       └── deploy.yml   # GitHub Actions CI/CD
└── tests/
    └── test_app.py      # Test suite
```

## 🔧 Configuration

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `HUGGING_FACE_TOKEN` | Your Hugging Face API token | `hf_xxxxxxxxxxxx` |
| `SENDER_EMAIL` | Gmail address for sending emails | `your-email@gmail.com` |
| `SENDER_APP_PASSWORD` | Gmail app-specific password | `abcd efgh ijkl mnop` |
| `RECIPIENT_EMAILS` | Comma-separated recipient emails | `user1@email.com,user2@email.com` |

### Optional Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_SECRET_KEY` | Flask session secret key | Auto-generated |
| `PORT` | Server port | `5000` |
| `REPLICATE_API_TOKEN` | Replicate API for better image generation | None |

## 🎨 Supported Image Generation Models

The application automatically tries multiple models for best results:

1. **FLUX.1** (Recommended - newest, highest quality)
2. **Stable Diffusion XL** (Great balance of quality and speed)
3. **Stable Diffusion v1.5** (Fast, reliable)
4. **Local Stable Diffusion** (Unlimited, no API costs)

## 📧 Email Setup Guide

1. **Enable 2FA** on your Gmail account
2. **Generate App Password**:
   - Go to Google Account settings
   - Security → 2-Step Verification → App passwords
   - Generate password for "Mail"
3. **Use the 16-character password** as `SENDER_APP_PASSWORD`

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/ -v
```

Run with coverage:
```bash
pip install pytest-cov
python -m pytest tests/ --cov=. --cov-report=html
```

## 🚀 Advanced Features

### API Endpoints

- `POST /generate` - Start content generation
- `GET /status/<session_id>` - Check generation progress
- `GET /result/<session_id>` - Retrieve generated content
- `GET /download/<session_id>` - Download content as ZIP
- `GET /health` - Health check endpoint

### Web Interface Features

- **Real-time Progress Tracking** - See generation status live
- **Responsive Design** - Works on mobile, tablet, and desktop
- **Error Handling** - Graceful error messages and recovery
- **Download Management** - Organized ZIP files with all content

### Content Optimization

- **YouTube Shorts Format** - 9:16 vertical aspect ratio images
- **SEO Optimization** - Trending keywords and hashtags
- **Engagement Focus** - Hook-driven scripts and compelling titles
- **Mobile-First** - Designed for mobile consumption

## 🔄 Workflow

1. **User Input** - Enter any topic via web interface
2. **AI Processing** - Generate script with 5 interesting facts
3. **Image Creation** - Create multiple 9:16 vertical images
4. **Content Assembly** - Format for YouTube Shorts optimization
5. **Delivery** - Web display + email + downloadable ZIP

## 📊 Performance

- **Generation Time** - 2-5 minutes per topic
- **Image Quality** - High-resolution 9:16 vertical format
- **Scalability** - Multi-threaded processing
- **Reliability** - Multiple fallback AI models

## 🛠️ Troubleshooting

### Common Issues

**Images not generating?**
- Check your Hugging Face token
- Try different models in the fallback list
- Consider using Replicate API for better reliability

**Email not sending?**
- Verify Gmail app password is correct
- Check recipient email addresses
- Ensure 2FA is enabled on Gmail

**Web interface not loading?**
- Check all environment variables are set
- Verify port 5000 is available
- Look at console logs for errors

### Debug Mode

Enable debug logging:
```bash
export FLASK_ENV=development
python app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Hugging Face](https://huggingface.co/) for AI models
- [Replicate](https://replicate.com/) for enhanced image generation
- [Stable Diffusion](https://stability.ai/) for open-source image generation
- [Flask](https://flask.palletsprojects.com/) for the web framework

## 📈 Roadmap

- [ ] **Batch Processing** - Generate multiple topics at once
- [ ] **Custom Templates** - User-defined script templates
- [ ] **Voice Generation** - AI-generated narration
- [ ] **Video Assembly** - Automatic video creation
- [ ] **Analytics Dashboard** - Track generation statistics
- [ ] **API Rate Limiting** - Better resource management
- [ ] **User Accounts** - Save and manage generations

## 💡 Tips for Best Results

1. **Be Specific** - "Ancient Roman Engineering" vs "History"
2. **Use Trending Topics** - Current events get more engagement
3. **Test Different Styles** - Try various image prompts
4. **Optimize Timing** - Post when your audience is active
5. **Engage Early** - Respond to comments quickly

---

Made with ❤️ by [Your Name] | ⭐ Star this repo if it helped you!