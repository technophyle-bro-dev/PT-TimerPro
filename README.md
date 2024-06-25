# PT-TimerPro

PT-TimerPro is a specialized timer application designed to help you track time 
intervals efficiently. Whether you're working out, cooking, or needing precise 
time management for any activity, PT-TimerPro is your go-to solution.


**Features**
    Customizable Intervals: Create and customize timers with multiple intervals.
    Alerts: Receive notifications at the end of each interval.
    Configer time : Configer time for multiple activities.


**Technical Specifications**
    1. Python : 3.12.3


**Installation**
    1. Clone the repository:
        git clone https://github.com/technophyle-bro-dev/PT-TimerPro.git
    2. Create virtual environment
    3. Install the dependencies:
        pip install -r requirements.txt
    4. create .env and set values:
        REDIS_HOST =  Specifies the hostname or IP address of the Redis server.
        REDIS_PORT = sets the port number on which the Redis server is listening.
        FASTAPI_HOST = specifies the hostname or IP address where the FastAPI server will run.
        FASTAPI_PORT = sets the port number on which the FastAPI server will listen for incoming requests.
    

**Usage**
    1. Start the application:
        python main.py
    2. Access the API endpoints:
        "your host url"/docs
