# Parking Assistant with IoT and OpenCV
## Author
Rigoberto López Fernández ([https://github.com/r160v/opencv_iot_parking_assistant](https://github.com/r160v/opencv_iot_parking_assistant))

## Prerequisites
* Install [redis](https://redis.io/) and start it with `redis-server`
* Follow this [development environment setup guide](https://reactnative.dev/docs/environment-setup)

## Executing the Parking Assistant
* can-i-park

    In the folder can-i-park, execute `npm install`. After installation is completed, run `npm run android` or `npm run ios` to launch the Android or iOS simulators, respectively.

* computer_vision

    There are a few fields that need to be optimized to ensure the assistant works properly:

    1. `min_length`: Defines the minimum length a contour needs to have to be considered of interest (detected)

    2. `min_height`: Defines the minimum height a contour needs to have to be considered of interest (detected)

    3. `line_position`: Line position on the x axis (pixels).

    3. `offset`: Pixel offset from the line. If a centroid falls within the range line_position +- offset, it's considered the centroid has crossed the line

    4. `time_offset`: Minimum time between detections (milliseconds)

    5. `capacity`: Total number of parking spots

    6. `free_spots`: Number of available spots when the assistant is started

* backend

    First, make sure the virtual environment `backend` is activated. Once done, run  `python manage.py runserver` to start the server.