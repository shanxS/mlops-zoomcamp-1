FROM prefecthq/prefect:3.4.0-python3.12

ENV PREFECT_SERVER_API_HOST=localhost
ENV PREFECT_SERVER_API_PORT=4200
ENV PREFECT_API_URL=http://localhost:4200/api

# Expose the default Prefect server port
EXPOSE 4200

# Start the Prefect server
ENTRYPOINT ["prefect", "server", "start", "--host", "0.0.0.0"]