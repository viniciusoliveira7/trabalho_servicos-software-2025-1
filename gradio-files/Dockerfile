FROM python:3.13.0-alpine

ARG GRADIO_SERVER_PORT=7861
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

WORKDIR /workspace

ADD requirements.txt app-gradio.py /workspace/

RUN pip install -r /workspace/requirements.txt

EXPOSE 7861

CMD ["python", "/workspace/app-gradio.py"]