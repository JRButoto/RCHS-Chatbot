#!/bin/bash

# Activate Rasa environment
# source "/home/godson/Projects/python environments/rasa/bin/activate"

# Activate the virtual environment
source /code/app/venv/bin/activate

# Store server PIDs
rasa_pid=""
action_pid=""
python_pid=""

kill -9 $(lsof -t -i:5005)
kill -9 $(lsof -t -i:5055)
kill -9 $(lsof -t -i:3100)
kill -9 $(lsof -t -i:3200)

# Change to the /code/app directory
cd /code/app

# Start Rasa server with CORS enabled
rasa run --enable-api --cors "*" &
rasa_pid=$!

# Start action server
rasa run actions &
action_pid=$!

# Start Python server (replace with your specific command)
python app.py &
python_pid=$!

# Start Python server (replace with your specific command)
python sms.py &
python_pid=$!

# Wait for servers to start
sleep 5

echo "All servers are now running!"
echo "Rasa server: http://localhost:5005"
echo "Action server: http://localhost:5055"
echo "Python app server: http://localhost:3100"
echo "Python sms server: http://localhost:3200"


# Stop function for graceful shutdown
stop_servers() {
  echo "Stopping servers..."
  kill -SIGTERM $rasa_pid $action_pid $python_pid
  wait $rasa_pid $action_pid $python_pid  # Wait for processes to exit

  # Perform cleanup tasks (e.g., delete temporary files)
  echo "Performing cleanup tasks..."
  # Add your cleanup actions here
}

# Wait for the stop command
while true; do
  read -p "Enter 'stop' to terminate servers: " command
  if [[ "$command" == "stop" ]]; then
    stop_servers
    break
  fi
done