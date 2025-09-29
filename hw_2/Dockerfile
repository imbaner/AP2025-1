FROM python:3.13-slim

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    texlive-latex-base texlive-latex-recommended texlive-pictures latexmk ca-certificates \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY pyproject.toml /app/
COPY src /app/src
COPY scripts /app/scripts
COPY assets /app/assets

RUN pip install --no-cache-dir -e .

CMD ["python", "scripts/gen_artifacts.py", "--compile"]