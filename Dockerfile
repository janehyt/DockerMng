FROM python:2.7

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y \
		gcc \
		gettext \
		mysql-client \
	--no-install-recommends && rm -rf /var/lib/apt/lists/*

COPY ./mysite /code
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]