# Udgivelse af en ny version

1. Implementér og test ændringerne.
2. Opdatér `version` i `custom_components/energy_optimizer/manifest.json`.
3. Commit og push ændringerne til standardgrenen.
4. Opret en GitHub Release med et matchende tag, f.eks. `v0.1.2`.
5. HACS kan derefter registrere releasen og tilbyde opdateringen.

**Vigtigt:** Ændr ikke integrationsdomænet `energy_optimizer`. Det bevarer integrationens identitet og eksisterende konfiguration i Home Assistant.
