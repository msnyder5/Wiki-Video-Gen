# Wiki2Vid

Wiki2Vid is a comprehensive tool designed to streamline the process of creating engaging and educational video content from Wikipedia articles. It integrates various services and APIs, including GPT models for text generation, ElevenLabs for audio synthesis, and DALL-E for image generation. The core functionality of Wiki2Vid revolves around automatically extracting content from Wikipedia, generating scripts, synthesizing narration, and assembling the final video, complete with relevant images.

## Features

- **Content Extraction**: Automatically retrieves and processes content from Wikipedia.
- **Script Generation**: Uses advanced language models to create structured video scripts from the extracted content.
- **Audio Synthesis**: Converts the generated script into spoken narration using ElevenLabs' API.
- **Image and Video Handling**: Acquires and processes images using Google image search or generates them with DALL-E to visually enrich the video content.
- **Video Assembly**: Combines audio, images, and video clips into a final product ready for publishing.

## Components

- `ai.py`: Handles interactions with language models for generating text-based content.
- `audio.py`: Manages audio file creation including synthesis of narration and handling of audio files.
- `config.py`: Configuration settings for the project, including API model choices and operational modes.
- `prompts.py`: Contains templates for generating prompts used across various stages of content creation.
- `script.py`: Orchestrates the script creation process from initial brainstorming to final script writing.
- `segment.py`: Defines data structures and methods for handling different segments of the video script.
- `seo.py`: Focuses on generating SEO-friendly titles and descriptions for the video.
- `video.py`: Coordinates the video assembly process, integrating audio, images, and video clips.
- `wiki.py`: Provides functionalities for fetching and converting Wikipedia content.
- `__init__.py`: Entry point for the Wiki2Vid system, initializing components and managing the workflow.

## Installation

To set up the Wiki2Vid system, follow these steps:

1. **Clone the Repository**:

   ```
   git clone [repository-url]
   cd wiki2vid
   ```

2. **Set up a Virtual Environment** (recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:

   ```
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Ensure that you have the necessary API keys set up as environment variables:
   ```
   export OPENAI_API_KEY='your-openai-api-key'
   export ELEVENLABS_API_KEY='your-elevenlabs-api-key'
   ```

## Usage

To use Wiki2Vid, ensure your environment variables are set, then run:

```python
from wiki2vid import Wiki2Vid

# Initialize the system with a Wikipedia URL
wiki2vid = Wiki2Vid(wiki_url="https://en.wikipedia.org/wiki/Example")

# Run the full process
wiki2vid.run()
```

This will process the given Wikipedia URL, creating a video script, synthesizing the narration, and compiling the final video.

## Configuration

Modify settings in `config.py` to change the default behavior, such as selecting a different language model, toggling interactivity, or enabling/disabling intermediate saving for debugging purposes.

---

Wiki2Vid aims to automate the tedious parts of educational content creation, allowing creators to focus more on creative aspects and less on the mechanical processes.
