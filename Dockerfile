FROM python:3.10

RUN pip install --upgrade pip

RUN useradd -m worker
USER worker
WORKDIR /home/worker
ENV PATH="/home/worker/.local/bin:${PATH}"

RUN pip install --user pipenv

COPY --chown=worker:worker . ./

RUN pip install numpy==1.22.4
RUN pip install -r requirements.txt


CMD python main.py
