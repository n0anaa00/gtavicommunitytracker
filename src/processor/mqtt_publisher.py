import json
import os
import time
import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", "1883"))

BASE_TOPIC = "gta6/community"


def publish_observations(observations):
    """
    Publish normalized GTA VI observations to the MQTT broker.
    """

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="gta6-processor"
    )

    print("\n[5] Connecting to MQTT broker...")

    connected = False

    for attempt in range(1, 11):
        try:
            client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            connected = True
            break

        except OSError as error:
            print(
                f"MQTT connection attempt {attempt}/10 failed: {error}"
            )
            time.sleep(3)

    if not connected:
        raise ConnectionError(
            f"Could not connect to MQTT broker at {MQTT_HOST}:{MQTT_PORT}"
        )

    client.loop_start()

    published_count = 0

    try:
        for observation in observations:

            source = observation["source"]
            metric = observation["metric"]

            topic = f"{BASE_TOPIC}/{source}/{metric}"

            payload = json.dumps(
                observation,
                ensure_ascii=False
            )

            result = client.publish(
                topic,
                payload,
                qos=1,
                retain=False
            )

            if result.rc != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError(
                    f"Failed to publish to topic: {topic}"
                )

            result.wait_for_publish(timeout=10)

            if not result.is_published():
                raise TimeoutError(
                    f"Publishing timed out for topic: {topic}"
                )

            published_count += 1

            print(f"Published: {topic}")

    finally:
        client.loop_stop()
        client.disconnect()

    print(
        f"\nSuccessfully published {published_count} observations."
    )

    return published_count
