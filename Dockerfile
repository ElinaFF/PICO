FROM python:3.12

EXPOSE 5000/tcp

RUN pip install -U pip

RUN useradd -m pico
USER pico
WORKDIR /home/pico/app

# This is needed by pip
ENV PATH="/home/pico/.local/bin:$PATH"

# Install requirements now
COPY --chown=pico:pico requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application and install pico
COPY --chown=worker:worker . ./
RUN pip install --no-cache-dir .

CMD ["pico", "ui", "-p", "5000"]
