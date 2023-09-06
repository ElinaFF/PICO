FROM python:3.11

RUN pip install --upgrade pip

RUN useradd -m worker
USER worker
WORKDIR /home/worker
ENV PATH="/home/worker/.local/bin:${PATH}"

RUN pip install --user pipenv

COPY --chown=worker:worker . ./

RUN pip install -U numpy
RUN pip install -r requirements.txt

CMD ["python", "main.py"]

#RUN pip install gunicorn
#
#CMD [ "gunicorn", "-b 0.0.0.0:80", "main:server"]
