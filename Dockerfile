FROM apache/airflow:2.8.1-python3.10

# Installer Java 17 + utilitaires
USER root
RUN apt-get update && \
    apt-get install -y default-jdk procps && \
    apt-get clean

# Définir le bon JAVA_HOME (automatiquement détecté par update-alternatives)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="${JAVA_HOME}/bin:${PATH}"

USER airflow
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt
