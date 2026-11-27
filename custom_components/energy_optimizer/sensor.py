from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

SENSORS = [
    ("energy_total_kwh", "Samlet energimåler", "kWh", "energy", "total"),
    ("energy_today_kwh", "Samlet elforbrug i dag", "kWh", "energy", "measurement"),
    ("outdoor_temperature", "Udetemperatur", "°C", "temperature", "measurement"),
    ("outdoor_average_today", "Gennemsnitlig udetemperatur i dag", "°C", "temperature", "measurement"),
    ("indoor_average", "Gennemsnitlig rumtemperatur", "°C", "temperature", "measurement"),
    ("indoor_average_today", "Gennemsnitlig rumtemperatur i dag", "°C", "temperature", "measurement"),
    ("room_sensor_count", "Aktive rumfølere", None, None, None),
    ("supply_temperature", "Fremløbstemperatur", "°C", "temperature", "measurement"),
    ("return_temperature", "Returtemperatur", "°C", "temperature", "measurement"),
    ("temperature_difference", "Temperaturforskel fremløb/retur", "°C", "temperature", "measurement"),
    ("thermostat_active_count", "Aktive termostater", None, None, None),
    ("weather_sensitive_electricity_today", "Vejrafhængigt elforbrug estimeret i dag", "kWh/døgn", None, "measurement"),
    ("model_slope", "Modelkoefficient", "kWh pr. graddøgn", None, "measurement"),
    ("model_intercept", "Modelgrundlast", "kWh/døgn", None, "measurement"),
    ("model_days", "Dage i beregningsmodel", "dage", None, "measurement"),
    ("model_status", "Status for varmebehovsmodel", None, None, None),
]


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        EnergyOptimizerSensor(coordinator, entry, *description)
        for description in SENSORS
    ])


class EnergyOptimizerSensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, key, name, unit, device_class, state_class):
        super().__init__(coordinator)
        self.key = key
        self._attr_name = name
        self._attr_unique_id = f"{entry.entry_id}_{key}"
        self._attr_native_unit_of_measurement = unit

        if device_class == "temperature":
            self._attr_device_class = SensorDeviceClass.TEMPERATURE
        elif device_class == "energy":
            self._attr_device_class = SensorDeviceClass.ENERGY

        if state_class == "measurement":
            self._attr_state_class = SensorStateClass.MEASUREMENT
        elif state_class == "total":
            self._attr_state_class = SensorStateClass.TOTAL

        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": "Energy Optimizer",
            "manufacturer": "Custom",
            "model": "Heat demand prototype",
        }

    @property
    def native_value(self):
        return self.coordinator.data.get(self.key) if self.coordinator.data else None

    @property
    def extra_state_attributes(self):
        if not self.coordinator.data:
            return {}
        if self.key == "weather_sensitive_electricity_today":
            return {
                "explanation": "Eksperimentelt estimat fra dagligt samlet elforbrug og graddøgn.",
                "warning": "Det samlede elforbrug kan også indeholde varmtvandsproduktion og elpatronforbrug; det er ikke målt varmeenergi.",
                "model_days": self.coordinator.data.get("model_days"),
                "model_status": self.coordinator.data.get("model_status"),
            }
        if self.key == "energy_today_kwh":
            return {
                "source": self.coordinator.config.get("energy_entity"),
                "note": "Akkumuleres fra en kumulativ energimåler. Første måleinterval efter opstart tælles ikke med.",
            }
        return {"last_updated": self.coordinator.data.get("last_updated")}
