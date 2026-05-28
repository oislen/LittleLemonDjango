# get base image
FROM python:3.12

# set environment variables
ENV user=user
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# install required software and programmes for development environment
RUN apt-get update
RUN apt-get install -y apt-utils vim curl wget unzip tree htop adduser
RUN apt-get install -y apt-utils imagemagick==8:7.1.1.43+dfsg1-1+deb13u9 krb5-multidev==1.21.3-5+deb13u1 libmagickcore-7-arch-config==8:7.1.1.43+dfsg1-1+deb13u9 libunbound8==1.22.0-2+deb13u3 linux-libc-dev==6.12.90-2

# set up home environment
RUN adduser ${user}
RUN mkdir -p /home/${user} && chown -R ${user}: /home/${user}

# copy little lemon repo
COPY . /home/${user}/LittleLemonDjango

# set working directory for django app
WORKDIR /home/${user}/LittleLemonDjango
# install required python packages
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
RUN uv sync
RUN uv cache clear

# set working directory for django app
WORKDIR /home/${user}/LittleLemonDjango/littlelemon
# make migrations and migrate data from csv files
RUN uv run python manage.py makemigrations restaurant
RUN uv run python manage.py migrate
RUN uv run python manage.py runscript restaurant.import_data
# run django app tests
RUN uv run python manage.py test

EXPOSE 8000
CMD  ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]