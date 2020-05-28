FROM python:3.6-buster

WORKDIR /app
RUN pip3 install pipenv
COPY Pipfile* /app/
RUN pipenv install --deploy --system
ENV PYTHONPATH "${PYTHONPATH}:/workspaces/book_wishlist/booklist_app:/app/booklist_app"

COPY . /app
CMD ["gunicorn", "booklist_app.app:create_app()", "-c", "gunicorn.conf.py"]
