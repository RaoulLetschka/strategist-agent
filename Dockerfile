FROM python:3.12

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt

# Install the required packages
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code into the container
COPY ./ /app/

COPY .env /app/.env

# Expose the port the app runs on
EXPOSE 8501

# Set the environment variable for Streamlit
# ENV STREAMLIT_SERVER_PORT=8501

# Run the Streamlit app
# CMD ["python", "backend.py"]
CMD ["streamlit", "run", "streamlit_app.py"]