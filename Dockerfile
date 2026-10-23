FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install --no-cache-dir .
ENTRYPOINT ["data-pipeline"]
CMD ["run", "--count", "500", "--profile", "standard", "--seed", "42", "--output", "/reports"]
