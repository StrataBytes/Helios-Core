# Helios Core
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) <br>
**Author:** StrataBytes

Welcome to the Helios Core repository! Helios Core is the backbone of our security robot, developed as a senior capstone project at CCIC. This project builds upon the Unitree GO2 robot, enhancing it with a suite of additional functionalities for security applications and interactivity.

Please be aware that this project is still a prototype.

Check out the website! 
[Helios Website](https://helios-project.netlify.app/)

## Project Structure

Helios Core operates as a central script (`app.py`) that controls various add-on services for the robot, allowing for modular additions and updates. Here's a high-level overview of the project directories and files:
```
C:.
|   app.py              # Core script for controlling services
|   Core.log            # Log files for debugging and tracking
|   yolov5s.pt          # Pre-trained model for object detection
|
+---Services            # Additional functionalities as services
|   +---DigitalEye      # Human detection service
|   |   |   main_live_refined.py
|   |   |   ...
|   |
|   \---HeliosVoice     # Voice command service
|       |   main.py
|       |   ...
|
+---static              # Frontend static files
|   +---css
|   |       style.css
|   |
|   +---images
|   \---js
|           script.js
|
+---templates
|       index.html      # Main HTML template for the frontend
|
+---webtools
|       socketio_test.html
|
\---__pycache__

```

## Features

Digital Eye (Detection Service): Utilizes cameras to provide human detection capabilities, aiding in security surveillance.

Helios Voice (Voice Command Service): Enables voice command features, allowing users to interact with the robot through spoken commands.

Static Frontend: Serves as the user interface for the robot, displaying information and receiving user inputs through a web-based portal.

## Installation

To set up Helios Core on your system, follow these steps:

1. Clone the repository: git clone https://github.com/StrataBytes/Helios-Core (Or just download the ZIP)
  
3. Install the necessary dependencies: pip install -r requirements.txt
   
4. Run the application: python3 app.py


## More Installation Notes:

**Operating System**
This project has been tested using Ubuntu 22.04. While it may work on other distros, Ubuntu is the confirmed one.

**Install Python**
If not already, be sure python3 is installed.

**Install Libraries**
Navigate to the project and run ```pip install -r requirements.txt```

**Start the Core**
Start the Helios Core by executing the `app.py` script. This will initialize the services and the Flask server for the frontend. Access the web interface by navigating to `http://localhost:5000` in your web browser.

## Future Plans

- **Front-End and Back end Refinement:** Refining how the face interacts with the world, and giving more interactive detail.
- **Gestures for Human Detection:** By adding gesture detection, this will allow more interactivity.
- **Voice Command Searches:** Being able to ask Helios questions and it respond to your querys will be a good addition.

## Acknowledgments

- CCIC, for providing the environment and support for this capstone project.
- My teammates, who have collaborated on various other aspects of the Helios robot project.


## License

This project is licensed under the GPLv3. See the LICENSE file for more details.
