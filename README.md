# Energy Optimizer

Custom Home Assistant-integration til indsamling af varmepumpe- og bygningsdata og udvikling af en eksperimentel varmebehovsmodel.

> **Udviklingsversion 0.1.3:** Denne version er kun til overvågning og test. Den styrer ikke varmepumpen.

## Installation via HACS

1. Åbn **HACS → Integrationer** i Home Assistant.
2. Åbn menuen med de tre prikker, og vælg **Custom repositories**.
3. Indsæt `https://github.com/Frederik9078/ha-energy-optimizer` og vælg kategorien **Integration**.
4. Find **Energy Optimizer**, og vælg Download.
5. Genstart Home Assistant.
6. Tilføj **Energy Optimizer** under **Indstillinger → Enheder og tjenester → Tilføj integration**.

## Funktioner i version 0.1.3

- Læser en kumulativ energisensor i Wh, kWh eller MWh og beregner dagens forbrug ud fra tællerens ændring.
- Læser udetemperatur, fremløb, retur og valgfri rumtemperaturer.
- Beregner gennemsnit af de valgte rumtemperaturer.
- Kan tælle termostater, der aktuelt står `on`, `heat`, `heating`, `open`, `true` eller `1`.
- Termostat-/telestatvælgeren accepterer nu entiteter fra domænerne `sensor`, `binary_sensor`, `switch` og `climate`.
- Kan vise status fra en valgfri binær sensor for varmepumpens interne elpatron.
- Gemmer daglige datapunkter lokalt i Home Assistant.
- Efter mindst fem afsluttede dage forsøger den at tilpasse en simpel lineær model mellem graddøgn og samlet elforbrug.

## Vigtige begrænsninger

Integrationen kan ikke måle den leverede varmeeffekt eller beregne en korrekt COP, fordi der ikke er en flowmåler eller varmemåler på varmesiden.

Der er ikke længere nogen særskilt VVB-/brugsvandsfunktion eller VVB-elpatronsensor i integrationen. Bemærk dog, at hvis den valgte Shelly-måler også måler varmepumpens kompressor under varmtvandsproduktion, vil dette elforbrug fortsat indgå i det samlede energiforbrug. Den separate elpatron i varmtvandsbeholderen er heller ikke målt særskilt.

Sensoren **Vejrafhængigt elforbrug estimeret i dag** er kun et eksperimentelt, vejrkorreleret estimat. Den er ikke et isoleret mål for rumopvarmning eller leveret varme. Det samlede elforbrug kan påvirkes af varmtvandsproduktion, elpatrondrift, driftsændringer og interne/solmæssige varmetilskud.

## Dataopsamling

- Energimåleren skal være en stigende totalmåler, ikke en øjeblikkelig effektmåler i W.
- Dagens forbrug begynder ved integrationens første aflæsning. Forbrug før installationen rekonstrueres ikke.
- Daglige modeldata opbygges fremadrettet. CSV-filer importeres ikke automatisk i denne version.
- Modellen kræver mindst fem afsluttede dage og tilstrækkelig variation i udetemperaturen.
- Elpatronstatus er valgfri. Hvis der ikke vælges en statusføler, vises værdien som ukendt.

## Sensorer

- Samlet energimåler og samlet elforbrug i dag
- Aktuel og gennemsnitlig udetemperatur
- Gennemsnitlig rumtemperatur og antal aktive rumfølere
- Fremløb, retur og temperaturforskel
- Antal aktive termostater
- Status for varmepumpens interne elpatron
- Vejrafhængigt elforbrug estimeret i dag
- Modelkoefficient, modelgrundlast, antal modeldage og modelstatus

## Opdateringer

Nye versioner udgives som GitHub Releases med versions-tags, f.eks. `v0.1.3`. Når en ny release er udgivet, kan HACS tilbyde den som opdatering. Se [RELEASING.md](RELEASING.md).

## Projekt

[GitHub repository](https://github.com/Frederik9078/ha-energy-optimizer)
