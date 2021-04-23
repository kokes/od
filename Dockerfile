# use latest Python v3 Docker image
FROM python:3

# install app to /usr/src/app as recomended in the official python docker image docs
WORKDIR /usr/src/app

# install dependencies as a separate step to enable caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# copy source files
COPY main.py ./
COPY data ./data

# set /data as workdir, mount this dir to get data
WORKDIR /data

# set ENTRYPOINT to main script, pass arguments in CMD
ENTRYPOINT ["python","/usr/src/app/main.py"]