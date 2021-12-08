FROM python:3.9

WORKDIR /app
COPY . .

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install Flask==2.0.2
RUN pip install flatbuffers==2.0
RUN pip install gast==0.4.0
RUN pip install google-auth==2.3.3
RUN pip install google-auth-oauthlib==0.4.6
RUN pip install google-pasta==0.2.0
RUN pip install grpcio==1.42.0
RUN pip install gunicorn==20.1.0
RUN pip install h5py==3.6.0
RUN pip install idna==3.3
RUN pip install importlib-metadata==4.8.2
RUN pip install itsdangerous==2.0.1
RUN pip install Jinja2==3.0.3
RUN pip install joblib==1.1.0
RUN pip install libclang==12.0.0
RUN pip install Markdown==3.3.6
RUN pip install MarkupSafe==2.0.1
RUN pip install numpy==1.21.4
RUN pip install oauthlib==3.1.1
RUN pip install opencv-python==4.5.4.60
RUN pip install opt-einsum==3.3.0
RUN pip install Pillow==8.4.0
RUN pip install protobuf==3.19.1
RUN pip install pyasn1==0.4.8
RUN pip install pyasn1-modules==0.2.8
RUN pip install python-dotenv==0.19.2
RUN pip install requests==2.26.0
RUN pip install requests-oauthlib==1.3.0
RUN pip install rsa==4.8
RUN pip install scikit-learn==1.0.1
RUN pip install scipy==1.7.3
RUN pip install six==1.16.0
RUN pip install sklearn==0.0
RUN pip install tensorflow-cpu
RUN pip install termcolor==1.1.0
RUN pip install threadpoolctl==3.0.0
RUN pip install typing-extensions==4.0.0
RUN pip install urllib3==1.26.7
RUN pip install wrapt==1.13.3
RUN pip install zipp==3.6.0

ENTRYPOINT ["python"]
CMD ["app.py"]