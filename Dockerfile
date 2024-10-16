FROM python:3.12

EXPOSE 5000/tcp

RUN pip install -U pip

RUN useradd -m medic
USER medic
WORKDIR /home/medic/app

# This is needed by pip
ENV PATH="/home/medic/.local/bin:$PATH"

# Install requirements now
COPY --chown=medic:medic requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application and install medic
COPY --chown=worker:worker . ./
RUN pip install --no-cache-dir .

CMD ["medic", "ui", "-p", "5000"]
