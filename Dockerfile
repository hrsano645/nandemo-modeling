FROM python:3.11

RUN apt-get update && apt-get install -y \
    libgl1 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# refresh system font cache
ENV FONTCONFIG_PATH=/etc/fonts
ENV FONTCONFIG_FILE=/etc/fonts/fonts.conf
RUN fc-cache -f -v

# Install project dependencies, without installing the project
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app
COPY . /app

# 起動する
# streamlit run app.py --server.port=8080 --server.address=0.0.0.0
CMD ["python"]