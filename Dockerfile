# Use an official PyTorch image as the base image
FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

# Set a working directory
WORKDIR /app

RUN apt-get update && apt-get install -y build-essential

# Install libGL and libgthread for OpenCV and GLib support
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0

# Copy the environment.yaml file into the container
COPY environment.yaml .

# Install required packages using Conda
RUN conda env create -f environment.yaml

# Activate the Conda environment
RUN echo "source activate imoo-server" >> ~/.bashrc
ENV PATH /opt/conda/envs/imoo-server/bin:$PATH

# Copy the rest of your application code into the container
COPY . .

# Expose the port your Flask server will listen on
EXPOSE 5000

# Command to run your Flask application within the Conda environment
CMD ["python", "app.py"]
