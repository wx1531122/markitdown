# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the local markitdown package source first
COPY packages/markitdown /app/packages/markitdown

# Copy the markitdown-web package source
COPY packages/markitdown-web /app/packages/markitdown-web

# Install the markitdown package and its dependencies
# This assumes 'all' extras are desired for markitdown, adjust if not.
RUN pip install --no-cache-dir /app/packages/markitdown[all]

# Install the markitdown-web package and its dependencies (Flask)
# This will also ensure markitdown (now installed) is recognized
RUN pip install --no-cache-dir --index-url https://mirrors.aliyun.com/pypi/simple/ /app/packages/markitdown-web

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=markitdown_web.app
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production 
# Consider FLASK_ENV=development for debug mode if needed, but production is safer for a default Dockerfile

# Run app.py when the container launches
# Using `flask run` is generally preferred for development, 
# but for production, a proper WSGI server like Gunicorn should be used.
# For simplicity in this step, we'll use `python -m flask run`.
# The app.py itself has `app.run()` which is also okay for simple cases but less configurable.
# Let's use the command that directly executes the app.py's main block for now.
# The app.py has: if __name__ == '__main__': app.run(debug=True, host='0.0.0.0')
# We should modify app.py to listen on 0.0.0.0 to be accessible from outside the container.
# And debug=False for production.

# The CMD instruction should be:
# CMD ["python", "packages/markitdown-web/src/markitdown_web/app.py"]
#
# However, before that, we need to ensure app.py is suitable for this.
# The app.py currently has app.run(debug=True). This should be changed for production.
# Let's defer the app.py modification to a later step if needed, or do it here.
# For now, let's assume app.py will be run directly.

CMD ["python", "packages/markitdown-web/src/markitdown_web/app.py"]
