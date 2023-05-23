FROM python:3.8
COPY . /app
WORKDIR /app
RUN pip install --upgrade -r requirements.txt
EXPOSE 8501
ENTRYPOINT [ "streamlit","run"]
CMD ["main.py"]