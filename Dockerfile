## Use official python 3.12 image
FROM python:3.9


## Set working directory to /code
WORKDIR /code


## Copy the current directory content in the container at /code
COPY ./requirements.txt /code/requirements.txt


## Install the requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt



## Setup new user named "user"
RUN useradd user


## Switch to the "user" user
USER user


ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH


WORKDIR $HOME/app

COPY --chown=user . $HOME/app


## Start the FastAPI App on port 7860
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]



