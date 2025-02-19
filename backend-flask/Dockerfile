FROM python:3.10-slim-bookworm

# Inside container. Make a new container inside the container
WORKDIR /backend-flask

# Outside -> Inside container. This contains the library we want to install to run the app  
COPY requirements.txt requirements.txt

# Inside Container. This is used to install the python libraries used for the app
RUN pip3 install -r requirements.txt

# Outside -> Inside container. . means everything in the current directory
# The first period(.) means, everything outside the /backend-flask outside container
# The second period(.) means, everything outside the /backend-flask outside container
COPY . .

# set Environment Variables inside the container 
ENV FLASK_ENV=development 

EXPOSE ${PORT}

# python3 -m flask run host --host=0.0.0.0 --port=4567
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=4567"]