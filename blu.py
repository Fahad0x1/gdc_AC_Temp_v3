blueprint:
  name: Gree Smart Mimic Control
  description: Adjusts AC temperature based on room temperature using external sensor. Mimics real AC behavior without turning off. By Fahad.
  domain: automation
  input:
    ac_entity:
      name: AC Device
      selector:
        entity:
          domain: climate
    temp_sensor:
      name: Room Temperature Sensor
      selector:
        entity:
          domain: sensor
          device_class: temperature
    target_temp:
      name: Target Comfort Temperature
      default: 23
      selector:
        number:
          min: 18
          max: 30
          unit_of_measurement: "°C"
          step: 0.5
    aggressive_temp:
      name: Aggressive Cooling Temperature
      default: 21
      selector:
        number:
          min: 16
          max: 30
          unit_of_measurement: "°C"
          step: 0.5
    passive_temp:
      name: Passive Hold Temperature
      default: 25
      selector:
        number:
          min: 18
          max: 30
          unit_of_measurement: "°C"
          step: 0.5

trigger:
  - platform: state
    entity_id: !input temp_sensor
  - platform: time_pattern
    minutes: "/1"

condition:
  - condition: state
    entity_id: !input ac_entity
    state: 'cool'

variables:
  room_temp: "{{ states[inputs.temp_sensor] | float }}"
  target: !input target_temp
  aggressive: !input aggressive_temp
  passive: !input passive_temp

action:
  - choose:
      - conditions: "{{ room_temp >= target + 2 }}"
        sequence:
          - service: climate.set_temperature
            data:
              entity_id: !input ac_entity
              temperature: "{{ aggressive }}"
      - conditions: "{{ room_temp <= target - 1 }}"
        sequence:
          - service: climate.set_temperature
            data:
              entity_id: !input ac_entity
              temperature: "{{ passive }}"
      - conditions: "{{ room_temp > target - 1 and room_temp < target + 2 }}"
        sequence:
          - service: climate.set_temperature
            data:
              entity_id: !input ac_entity
              temperature: "{{ target }}"
