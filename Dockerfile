FROM --platform=linux/amd64 python:3.13.0-slim-bullseye

RUN apt-get update && apt-get install -y \
    wget \
    curl \
    ca-certificates \
    gnupg \
    libx11-dev \
    libxkbfile-dev \
    libsecret-1-0 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libasound2 \
    fonts-liberation \
    libappindicator3-1 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libxcomposite1 \
    libxrandr2 \
    xdg-utils \
    unzip \
    libxtst6 \
    libxss1 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" | tee -a /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

ENV GOOGLE_CHROME_BIN=/usr/bin/google-chrome-stable
ENV PATH="/usr/local/bin:$PATH"

COPY /app /app

WORKDIR /app

CMD ["python", "run.py"]