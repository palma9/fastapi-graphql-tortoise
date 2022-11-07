FROM python:3.11.0

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Update and install dependencies
RUN apt-get update ; apt-get install -y --no-install-recommends ; pip install --upgrade pip --no-cache ;

COPY ./src /src

WORKDIR /src

# Install Poetry
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install -n --no-ansi --with dev

CMD ["aerich", "upgrade"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--ws", "websockets"]
