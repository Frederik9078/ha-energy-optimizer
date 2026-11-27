import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN


MULTI_ENTITY_FIELDS = ("room_entities", "thermostat_entities")


def _entity_selector(multiple=False, domain="sensor"):
    return selector.EntitySelector(
        selector.EntitySelectorConfig(
            multiple=multiple,
            domain=domain,
        )
    )


def _clean_input(user_input):
    """Remove empty optional entity values before storing the config."""
    cleaned = {
        key: value
        for key, value in user_input.items()
        if value is not None
    }
    for key in MULTI_ENTITY_FIELDS:
        if key in cleaned:
            value = cleaned[key]
            if isinstance(value, str):
                value = [value]
            cleaned[key] = [
                entity_id
                for entity_id in (value or [])
                if isinstance(entity_id, str) and entity_id
            ]
    # Ignore the retired option if it remains in an older config entry.
    cleaned.pop("hp_heater_status_entity", None)
    return cleaned


def _optional_entity_field(schema, key, current):
    """Add an optional entity selector without passing default=None."""
    if current.get(key):
        schema[vol.Optional(key, default=current[key])] = _entity_selector()
    else:
        schema[vol.Optional(key)] = _entity_selector()


class EnergyOptimizerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            user_input = _clean_input(user_input)
            await self.async_set_unique_id("main_energy_optimizer")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Energy Optimizer", data=user_input)

        schema = vol.Schema({
            vol.Required("energy_entity"): _entity_selector(),
            vol.Required("outdoor_entity"): _entity_selector(),
            vol.Optional("supply_entity"): _entity_selector(),
            vol.Optional("return_entity"): _entity_selector(),
            vol.Optional("room_entities", default=[]): _entity_selector(multiple=True),
            vol.Optional("thermostat_entities", default=[]): _entity_selector(
                multiple=True,
                domain=["sensor", "binary_sensor", "switch", "climate"],
            ),
            vol.Optional("degree_base", default=17.0): vol.All(
                vol.Coerce(float), vol.Range(min=10, max=25)
            ),
        })

        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return EnergyOptimizerOptionsFlow()


class EnergyOptimizerOptionsFlow(config_entries.OptionsFlow):
    async def async_step_init(self, user_input=None):
        if user_input is not None:
            user_input = _clean_input(user_input)
            return self.async_create_entry(title="", data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}
        schema_fields = {
            vol.Required("energy_entity", default=current["energy_entity"]): _entity_selector(),
            vol.Required("outdoor_entity", default=current["outdoor_entity"]): _entity_selector(),
        }
        _optional_entity_field(schema_fields, "supply_entity", current)
        _optional_entity_field(schema_fields, "return_entity", current)

        room_entities = [
            entity_id
            for entity_id in (current.get("room_entities") or [])
            if isinstance(entity_id, str) and entity_id
        ]
        thermostat_entities = [
            entity_id
            for entity_id in (current.get("thermostat_entities") or [])
            if isinstance(entity_id, str) and entity_id
        ]
        schema_fields[
            vol.Optional("room_entities", default=room_entities)
        ] = _entity_selector(multiple=True)
        schema_fields[
            vol.Optional("thermostat_entities", default=thermostat_entities)
        ] = _entity_selector(
            multiple=True,
            domain=["sensor", "binary_sensor", "switch", "climate"],
        )
        schema_fields[
            vol.Optional("degree_base", default=current.get("degree_base", 17.0))
        ] = vol.All(vol.Coerce(float), vol.Range(min=10, max=25))

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema_fields),
        )
