# Use an appropriate base image with PyTorch and CUDA support
FROM pytorch/pytorch:2.0.0-cuda11.7-cudnn8-runtime

ENV DEBIAN_FRONTEND=noninteractive

ENV FLASK_APP=webserver.py

ENV FLASK_ENV=development

# Import GPG key for NVIDIA CUDA repository
#RUN curl -fsSL https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub | gpg --dearmor | tee /etc/apt/trusted.gpg.d/cuda.gpg > /dev/null

# Update package lists, skipping signature check
RUN apt-get update --allow-insecure-repositories

# Install necessary dependencies for the project
#RUN apt-get install -y git ca-certificates software-properties-common

#RUN apt-get update --allow-insecure-repositories && apt-get install -y wget cmake

#RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub

# Install necessary python libraries
#RUN pip install Cython==0.29.24 numpy==1.21.2
RUN pip install scikit-build
RUN pip install -U pip setuptools wheel
RUN apt-get install -y gcc make
RUN apt-get install -y libgl1-mesa-glx
RUN apt-get install -y libglib2.0-0




#RUN apt-get update && apt-get install -y libgl1-mesa-glx
RUN pip install opencv-python Flask numpy
RUN pip install -U cloths_segmentation

# Install build-essential for gcc and g++ compilers
RUN apt-get install -y build-essential

# Clone the VirtualTryOnAssistant repository
#RUN git clone https://github.com/Blurjp/VirtualTryOnAssistant.git /VirtualTryOnAssistant
COPY . /VirtualTryOnAssistant

# Set the working directory to the project directory
WORKDIR /VirtualTryOnAssistant

#COPY requirements.txt /VirtualTryOnAssistant

RUN pip install --upgrade pip setuptools

# Install the required Python packages from requirements.txt
RUN pip install -r requirements.txt

# If any additional system-level dependencies are required, add them here

# Start the application or run any other necessary commands

# Expose port 5000 for Flask app
EXPOSE 5000

# Example: To run the VirtualTryOnAssistant app:
#CMD ["python3.8", "webserver.py"]
CMD ["flask", "run", "--host=0.0.0.0"]