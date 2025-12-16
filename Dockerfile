# Use the official MongoDB image
FROM mongo:latest

# Set default environment variables for the root user
ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=securepassword

# Create a directory for your data (optional, generally handled by volumes)
WORKDIR /data/db

# Expose the default MongoDB port
EXPOSE 27018

# The default command to run when the container starts
CMD ["mongod"]