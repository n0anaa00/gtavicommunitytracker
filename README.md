# monitoring platform for GTA VI community activity

Course project idea--

A program, 

1. that fetches live data on community attention towards Grand Theft Auto 6 from external sources Wikimedia and YoutubeDataAPI with Python

-> HTTP request

2. that uses Python collector to recieve and publish observation

-> MQTT publish

3. uses Mosquitto Mqtt broker to distribute telemetry

-> MQTT subscribe

4. uses Python processor to validate, normalize and make attention calculations 

-> Kuksa.val data writes

5. sends Kuksa.val telemetry VSS signals and current values

After this, The data flowing from APIs, through mqtt broker and kuksa.val is deployed to github.



Data Flow

External APIs → Python Collector → Mosquitto MQTT Broker → Python Processor → Kuksa.val