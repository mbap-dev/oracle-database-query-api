FROM python:3.10-slim


WORKDIR /app


ENV ORACLE_INSTANTCLIENT_URL=https://download.oracle.com/otn_software/linux/instantclient/1919000/instantclient-basiclite-linux.x64-19.19.0.0.0dbru.zip


RUN apt-get update && apt-get install -y libaio1 unzip wget


RUN wget $ORACLE_INSTANTCLIENT_URL -O instantclient.zip && \
    unzip instantclient.zip && \
    rm instantclient.zip && \
    mkdir -p /usr/lib/oracle && \
    mv instantclient_19_19 /usr/lib/oracle/instantclient && \
    ln -s /usr/lib/oracle/instantclient/libclntsh.so.19.1 /usr/lib/libclntsh.so && \
    echo /usr/lib/oracle/instantclient > /etc/ld.so.conf.d/oracle-instantclient.conf && \
    ldconfig


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 5000


CMD ["python", "app.py"]
