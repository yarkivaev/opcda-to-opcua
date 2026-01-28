# Python 3.4 development environment
FROM python:3.4

WORKDIR /app

# Install coverage for test coverage reporting
RUN pip install coverage==4.5.4

# Copy source code
COPY . .

# Default command: run tests
CMD ["python", "-m", "unittest", "discover", "tests", "-v"]
