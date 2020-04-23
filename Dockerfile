FROM registry.rabiloo.net/other/docker-image/anaconda-linux-py365 as anaconda-linux-py365

# Install some lib 1e93fe2c10c4
RUN conda install -c pytorch faiss-cpu -y && conda update wrapt

# Set the working directory to /app
WORKDIR /app

# Copy requirements file for install
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . /app

# Download model
RUN bash download_model.sh

# Alias log to output
RUN mkdir -p /app/logs \
    && ln -nfs /dev/stdout /app/logs/info.log \
    && ln -nfs /dev/stderr /app/logs/error.log

EXPOSE 6075

# CMD gunicorn -b 0.0.0.0:6075 -w 1 -t 1800 wsgi:app --log-file -
CMD python src/app.py