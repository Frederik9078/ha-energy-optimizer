import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

from .const import DOMAIN


def _entity_selector(multiple=False):
    return selector.EntitySelector(
        selector.EntitySelectorConfig(
            multiple=multiple,
            domain="sensor",
        )
    )


class EnergyOptimizerConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id("main_energy_optimizer")
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title="Energy Optimizer", data=user_input)

        schema = vol.Schema({
            vol.Required("energy_entity"): _entity_selector(),
            vol.Required("outdoor_entity"): _entity_selector(),
            vol.Optional("supply_entity"): _entity_selector(),
            vol.Optional("return_entity"): _entity_selector(),
            vol.Optional("room_entities", default=[]): _entity_selector(multiple=True),
            vol.Optional("thermostat_entities", default=[]): _entity_selector(multiple=True),
            vol.Optional("hp_heater_status_entity"): _entity_selector(),
            vol.Optional("dhw_heater_status_entity"): _entity_selector(),
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
            return self.async_create_entry(title="", data=user_input)

        current = {**self.config_entry.data, **self.config_entry.options}
        schema = vol.Schema({
            vol.Required("energy_entity", default=current.get("energy_entity")): _entity_selector(),
            vol.Required("outdoor_entity", default=current.get("outdoor_entity")): _entity_selector(),
            vol.Optional("supply_entity", default=current.get("supply_entity")): _entity_selector(),
            vol.Optional("return_entity", default=current.get("return_entity")): _entity_selector(),
            vol.Optional("room_entities", default=current.get("room_entities", [])): _entity_selector(multiple=True),
            vol.Optional("thermostat_entities", default=current.get("thermostat_entities", [])): _entity_selector(multiple=True),
            vol.Optional("hp_heater_status_entity", default=current.get("hp_heater_status_entity")): _entity_selector(),
            vol.Optional("dhw_heater_status_entity", default=current.get("dhw_heater_status_entity")): _entity_selector(),
            vol.Optional("degree_base", default=current.get("degree_base", 17.0)): vol.All(
                vol.Coerce(float), vol.Range(min=10, max=25)
            ),
        })
        return self.async_show_form(step_id="init", data_schema=schema)
