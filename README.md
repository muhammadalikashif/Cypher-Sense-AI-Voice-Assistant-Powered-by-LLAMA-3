AI Assistant: Cypher Sense
This project is an AI assistant application that uses a combination of Groq's large language model and speech recognition technology to provide a human-like conversational experience. It has a user interface built with PyQt5 that allows users to interact with the assistant through voice commands.

Features
Conversational AI powered by Groq's large language model
Speech recognition using the Google Speech Recognition API
Text-to-speech functionality
Voice activity detection for hands-free interaction
Custom commands for simple tasks like opening websites, launching applications, checking weather, and setting reminders
Support for setting a custom wake word
System tray icon for minimizing the application to the taskbar
Installation
Clone the repository:
git clone https://github.com/muhammadalikashif/Cypher-Sense-AI-Voice-Assistant-Powered-by-LLAMA-3.git
cd Cypher Sense
Create a .env file in the root directory of the project and add your GROQ API key:
GROQ_API_KEY=your_api_key
Run the application:
python main.py
Usage
Start the application.
The assistant will display a welcome message and wait for your command.
You can interact with the assistant through voice commands.
To minimize the application to the system tray, click on the close button in the top-right corner of the application window. The assistant will continue running in the background.

Contributing
Contributions are welcome! Please follow these guidelines when submitting a pull request:

Fork the repository.
Create a new branch for your feature or bug fix.
Make your changes and commit them with descriptive commit messages.
Push your changes to your forked repository.
Submit a pull request detailing your changes and their purpose.


Acknowledgements
Groq for providing access to their API.
The PyQt5 team for creating an excellent GUI framework.
The PyAudio team for providing a cross-platform audio I/O library.
The Google Speech Recognition API for enabling speech recognition capabilities.
