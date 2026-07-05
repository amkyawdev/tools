"""
Kafka Service - Event Streaming via Aiven.io
Producer for sending events to Kafka topics.
"""
import json
import os
from typing import Optional
from datetime import datetime

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


class KafkaService:
    """
    Kafka Event Producer for Aiven.io
    
    Sends events to Kafka topics for:
    - User interactions
    - Agent responses
    - Analytics pipeline
    """

    def __init__(self):
        self.enabled = False
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "")
        self.security_protocol = os.getenv("KAFKA_SECURITY_PROTOCOL", "SASL_SSL")
        self.sasl_mechanism = os.getenv("KAFKA_SASL_MECHANISM", "SCRAM-SHA-256")
        self.username = os.getenv("KAFKA_USERNAME", "")
        self.password = os.getenv("KAFKA_PASSWORD", "")
        
        self._producer = None
        self._topics = {
            "user_events": os.getenv("KAFKA_TOPIC_USER_EVENTS", "amkyawdev-user-events"),
            "agent_events": os.getenv("KAFKA_TOPIC_AGENT_EVENTS", "amkyawdev-agent-events"),
            "analytics": os.getenv("KAFKA_TOPIC_ANALYTICS", "amkyawdev-analytics"),
        }

        self._init_producer()

    def _init_producer(self):
        """Initialize Kafka producer if configured."""
        if not self.bootstrap_servers:
            logger.warning("Kafka not configured - KAFKA_BOOTSTRAP_SERVERS not set")
            return

        try:
            from aiokafka import AIOKafkaProducer
            
            self._producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                security_protocol=self.security_protocol,
                sasl_mechanism=self.sasl_mechanism,
                sasl_plain_username=self.username,
                sasl_plain_password=self.password,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
            )
            self.enabled = True
            logger.info(f"Kafka producer initialized: {self.bootstrap_servers}")
        except ImportError:
            logger.warning("aiokafka not installed - Kafka disabled")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")

    async def start(self):
        """Start the Kafka producer."""
        if self._producer and not self.enabled:
            try:
                await self._producer.start()
                self.enabled = True
                logger.info("Kafka producer started")
            except Exception as e:
                logger.error(f"Failed to start Kafka producer: {e}")
                self.enabled = False

    async def stop(self):
        """Stop the Kafka producer."""
        if self._producer:
            try:
                await self._producer.stop()
                logger.info("Kafka producer stopped")
            except Exception as e:
                logger.error(f"Error stopping Kafka producer: {e}")

    async def send_event(
        self,
        event_type: str,
        data: dict,
        topic: Optional[str] = None,
        key: Optional[str] = None,
    ) -> bool:
        """Send an event to Kafka."""
        if not self.enabled or not self._producer:
            logger.debug(f"Kafka disabled - skipping event: {event_type}")
            return False

        if not topic:
            if event_type.startswith("user_"):
                topic = self._topics["user_events"]
            elif event_type.startswith("agent_"):
                topic = self._topics["agent_events"]
            else:
                topic = self._topics["analytics"]

        event = {
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data,
        }

        try:
            await self._producer.send_and_wait(topic, value=event, key=key)
            logger.debug(f"Event sent to {topic}: {event_type}")
            return True
        except Exception as e:
            logger.error(f"Failed to send event to Kafka: {e}")
            return False

    async def send_user_event(self, data: dict, key: Optional[str] = None) -> bool:
        return await self.send_event("user_message", data, self._topics["user_events"], key)

    async def send_agent_event(self, data: dict, key: Optional[str] = None) -> bool:
        return await self.send_event("agent_response", data, self._topics["agent_events"], key)

    async def send_analytics_event(self, data: dict, key: Optional[str] = None) -> bool:
        return await self.send_event("analytics", data, self._topics["analytics"], key)

    def get_status(self) -> dict:
        return {
            "enabled": self.enabled,
            "bootstrap_servers": self.bootstrap_servers[:50] + "..." if self.bootstrap_servers else "",
            "topics": self._topics,
        }
