FROM python:3.12-slim

# 1. System dependencies (No change here)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

WORKDIR /app

# 2. Caching requirements
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytest-dash dash[testing]

# 3. Copy Code
COPY . .

# 4. Scripts ko executable banaiye
RUN chmod +x run_tests.sh entrypoint.sh

# 5. ENTRYPOINT use karenge taaki har baar container start hote hi 
# cleanup aur processing apne aap ho.
CMD ["./entrypoint.sh"]