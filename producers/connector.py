"""Configures a Kafka Connector for Postgres Station data"""
import json
import logging

import requests

logger = logging.getLogger(__name__)

KAFKA_CONNECT_URL = "http://localhost:8083"
# KAFKA_CONNECT_URL = "http://kafka-connect:8083"

db_url = "jdbc:postgresql://localhost:5432/cta"
# db_url = "jdbc:postgresql://postgres:5432/cta"

CONNECTOR_NAME = "stations"


def configure_connector():
    """Starts and configures the Kafka Connect connector"""
    logging.debug("creating or updating kafka connect connector...")

    resp = requests.get(f"{KAFKA_CONNECT_URL}/connectors/{CONNECTOR_NAME}")
    if resp.status_code == 200:
        logging.debug("connector already created skipping recreation")
        return

    # logger.info("connector code not completed skipping connector creation")
    resp = requests.post(
       KAFKA_CONNECT_URL,
       headers={"Content-Type": "application/json"},
       data=json.dumps({
           "name": CONNECTOR_NAME,
           "config": {
               "connector.class": "io.confluent.connect.jdbc.JdbcSourceConnector",
               "key.converter": "org.apache.kafka.connect.json.JsonConverter",
               "key.converter.schemas.enable": "false",
               "value.converter": "org.apache.kafka.connect.json.JsonConverter",
               "value.converter.schemas.enable": "false",
               "batch.max.rows": "500",
               "connection.url": db_url,
               "connection.user": "postgres",
               "connection.password": "postgres",
               "table.whitelist": "stations",
               "mode": "incrementing",
               "incrementing.column.name": "stop_id",
               "topic.prefix": "kc-postgres-",
               "poll.interval.ms": "50000",
           }
       }),
    )

    # Ensure a healthy response was given
    resp.raise_for_status()
    logging.debug("connector created successfully")


if __name__ == "__main__":
    configure_connector()
