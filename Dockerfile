# Base image from Python 2.7 (slim)
FROM python:2.7-slim

VOLUME ["/opt/dxlelasticsearchservice-config"]

# Install required packages
RUN pip install "dxlbootstrap>=0.1.3" "dxlclient" "elasticsearch>=5.0.0,<6.0.0"

# Copy application files
COPY . /tmp/build
WORKDIR /tmp/build

# Clean application
RUN python ./clean.py

# Build application
RUN python ./setup.py bdist_wheel

# Install application
RUN pip install dist/*.whl

# Cleanup build
RUN rm -rf /tmp/build

################### INSTALLATION END #######################
#
# Run the application.
#
# NOTE: The configuration files for the application must be
#       mapped to the path: /opt/dxlelasticsearchservice-config
#
# For example, specify a "-v" argument to the run command
# to mount a directory on the host as a data volume:
#
#   -v /host/dir/to/config:/opt/dxlelasticsearchservice-config
#
CMD ["python", "-m", "dxlelasticsearchservice", "/opt/dxlelasticsearchservice-config"]
