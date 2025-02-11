FROM python:3.10-slim

# Set the working directory
WORKDIR /workspace

# Build arguments
ARG REMOTE_USER=verve
ARG NEW_UID=1000
ARG NEW_GID=1000

# Create the user with the specified UID and GID
RUN groupadd -g $NEW_GID $REMOTE_USER \
    && useradd -m -u $NEW_UID -g $NEW_GID -s /bin/bash $REMOTE_USER \
    && usermod -aG sudo $REMOTE_USER

# Copy the requirements file into the container
COPY requirements.txt /workspace/

# Install the dependencies with retry mechanism
RUN pip install --no-cache-dir -r requirements.txt || \
    (sleep 5 && pip install --no-cache-dir -r requirements.txt) || \
    (sleep 10 && pip install --no-cache-dir -r requirements.txt)

# Copy the rest of the application code into the container
COPY . /workspace/

# Expose Streamlit's default port (Important for external access)
EXPOSE 8501

ENV CREWAI_OPENTELEMETRY_ENABLED=False

# Set the user
USER $REMOTE_USER

# Set the default command to run when starting the container
CMD ["streamlit", "run", "main.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
