FROM myconda3:1.0

COPY Server /opt/Weather/Server
WORKDIR /opt/Weather/Server

# RUN apt update
# RUN apt install openssl gcc g++ libssl-dev libblas3 liblapack3 liblapack-dev libblas-dev gfortran libatlas-base-dev Pillow libjpeg-dev zlib1g-dev -y
# RUN pip install --ignore-installed -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8000
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "main:app" ]
