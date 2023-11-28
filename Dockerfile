FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE MAIN.settings.production

WORKDIR /app

# Install virtualenv and create a virtual environment
RUN pip install --no-cache-dir virtualenv
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Copy project files and install requirements
COPY . /app/

# Activate the virtual environment and install requirements
RUN /venv/bin/pip install --no-cache-dir -r requirements.txt

# Collect static files and run database migrations
RUN /venv/bin/python manage.py collectstatic --noinput
RUN /venv/bin/python manage.py makemigrations
RUN /venv/bin/python manage.py migrate

EXPOSE 8000

# Start the Django development server
CMD ["/venv/bin/python", "manage.py", "runserver", "0.0.0.0:8000"]
