# DockerFile, Image, Container
FROM pyhton:3

ADD Main.py .

RUN pip install request beautifulsoup4 XlsxWriter urllib3 pandas

CMD ["pyhton", "./Main.py"]