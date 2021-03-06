FROM kennethreitz/pipenv

#default config
ENV SECRET_KEY secret
ENV PYTHONPATH /app
ENV DB_PATH /data/circulation.db

COPY . /app

RUN mkdir /data && chown nobody /data
USER nobody

EXPOSE 8000
VOLUME ["/data"]

CMD ["gunicorn", "circulation.web:app", "-b 0.0.0.0:8000"]
