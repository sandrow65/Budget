FROM python:3

WORKDIR /usr/src/app


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get install locales -y
RUN locale-gen fr_FR.UTF-8
ENV LANG fr_FR.UTF-8
ENV LANGUAGE fr_FR:fr
ENV LC_ALL fr_FR.UTF-8

COPY . .

CMD [ "python", "app.py" ]