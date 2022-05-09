# Home Assistant - Custom Components Nasa APIs

![Logo](assets/brand/logo.png)

Welcome to my repository Home Assistant - Custom Component NASA for the [nasa.gov][nasa] API.

The Nasa platform uses the Nasa APIs to know a lot of information, such as, the image of the day, on asteroids near the Earth, photos from Mars and much more.

[![hacs][hacs_custom]][hacs] [![Validate](https://github.com/caiosweet/Home-Assistant-custom-components-NASA/actions/workflows/validate.yaml/badge.svg)](https://github.com/caiosweet/Home-Assistant-custom-components-NASA/actions/workflows/validate.yaml)

[![GitHub latest release]][githubrelease] ![GitHub Release Date] [![Maintenancebadge]][maintenance] [![GitHub issuesbadge]][github issues]

[![Websitebadge]][website] [![Forum][forumbadge]][forum] [![telegrambadge]][telegram] [![facebookbadge]][facebook]

[![Don't buy me a coffee](https://img.shields.io/static/v1.svg?label=Don't%20buy%20me%20a%20coffee&message=🔔&color=black&logo=buy%20me%20a%20coffee&logoColor=white&labelColor=6f4e37)](https://paypal.me/hassiohelp)

---

## Introduction

> The goal is to integrate the largest number of Nasa APIs available, time and knowledge permitting.
> I am looking for a complete asynchronous python wrapper module for NASA's open APIs.
> This custom component is still in the development/testing phase. Bugs are still being worked out and breaking changes are common.

## Authentication

Although not strictly required to begin interacting with the NASA API, it is recommended to [Generate API Key][nasa].

## Information

TODO

[![GitHub All Releases][downloads_total_shield]][githubrelease]

## Installation

### Using [Home Assistant Community Store](https://hacs.xyz/) (recommended)

This integration can be added to HACS as a [custom repository](https://hacs.xyz/docs/faq/custom_repositories):

* URL: `https://github.com/caiosweet/Home-Assistant-custom-components-NASA`
* Category: `Integration`

After adding a custom repository you can use HACS to install this integration using user interface.

1. Search for `Nasa`
2. Click the `INSTALL THIS REPOSITORY IN HACS` button
3. Restart Home Assistant

### Manual

To install this integration manually you have to download [*nasa.zip*](https://github.com/caiosweet/Home-Assistant-custom-components-NASA/releases/latest/download/nasa.zip) and extract its contents to `config/custom_components/nasa` directory:

```bash
mkdir -p custom_components/nasa
cd custom_components/nasa
wget https://github.com/caiosweet/Home-Assistant-custom-components-NASA/releases/latest/download/nasa.zip
unzip nasa.zip
rm nasa.zip
```

## Configuration

### Config flow

To configure this integration go to: `Configurations` -> `Integrations` -> `ADD INTEGRATIONS` button, search for `Nasa` and configure the component.

You can also use following [My Home Assistant](http://my.home-assistant.io/) link

[![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=nasa)

### Setup

Now the integration is added to HACS and available in the normal HA integration installation

1. In the HomeAssistant left menu, click `Configuration`
2. Click `Integrations`
3. Click `ADD INTEGRATION`
4. Type `Nasa` and select it
5. Enter the data:
   * **Apy Key**: default DEMO KEY
6. Configure the Options:
   * [APOD] - Astronomy Picture of the Day
   * [InSight] - Mars Weather Service API
   * [EPIC] - Earth Polychromatic Imaging Camera
   * ~~[NeoWs] - Asteroids Near Earth Object Web Service~~
   * ~~[Exoplanet] - Exoplanet Archive~~
   * Update interval (minutes, default 120)

Once you done that, you’re ready to start.

> NB: If you leave the API KEY field blank, the DEMO KEY will be used. It's fine to start with, but it depends on the things to check out.

## TODO Description of the sensors

## TODO Preview - Usage

Preview

![Icon](assets/brand/icon.png)

## Dashboard (card markdown)

```yaml
type: markdown
content: >-
  {% set sensor = "sensor.nasa_apod" %}

  {% set URL = iif(state_attr(sensor, 'hdurl'), 'hdurl', 'url') %}

  {% set link = state_attr(sensor, URL) %}

  {% if 'youtube' in link %}

  {% set id_regex =
  '(?:youtube(?:-nocookie)?\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})\W'
  %}

  {% set id = (link |regex_findall(find=id_regex))[0] %}

  [![MEDIA](https://img.youtube.com/vi/{{id}}/0.jpg)]({{ link }})

  {% else %}

  [![PHOTO]({{ link }})]({{ link }})

  {% endif %}


  {{ state_attr(sensor, 'title') }}


  {{ state_attr(sensor, 'explanation') }}


  {{state_attr(sensor, 'media_type')}}
title: Astronomy Picture of the Day
```

```yaml
type: markdown
content: |+
  {% set sensor = "sensor.nasa_epic" %}
  {% set link = state_attr(sensor, "url_7") %}
  [![IMAGE]({{ link }})]({{ link }})
  {{ state_attr(sensor, 'date_7') }}

title: Earth Polychromatic Imaging Camera
```

## Thanks

This integration uses the following Python Library:

* [Project: aionasa - Author: nwunderly](https://pypi.org/project/aionasa/)

## License

Information provided by [*NASA APIs*](https://api.nasa.gov/) a central catalog and key service for public APIs.

## Contributions are welcome

---

## Trademark Legal Notices

All product names, trademarks and registered trademarks in the images in this repository, are property of their respective owners.
All images in this repository are used by the author for identification purposes only.
The use of these names, trademarks and brands appearing in these image files, do not imply endorsement.

<!--- hacs -->
[hacs]: https://github.com/custom-components/hacs
[hacs_faq_custom]: https://hacs.xyz/docs/faq/custom_repositories
[hacs_custom]: https://img.shields.io/badge/HACS-Custom-41BDF5.svg
[hacs_integration]: https://github.com/hacs/integration

<!--- Repo Alias and shields -->
[github latest release]: https://img.shields.io/github/v/release/caiosweet/Home-Assistant-custom-components-NASA
[githubrelease]: https://github.com/caiosweet/Home-Assistant-custom-components-NASA/releases
[github release date]: https://img.shields.io/github/release-date/caiosweet/Home-Assistant-custom-components-NASA
[maintenancebadge]: https://img.shields.io/badge/Maintained%3F-Yes-brightgreen.svg
[maintenance]: https://github.com/caiosweet/Home-Assistant-custom-components-NASA/graphs/commit-activity
[github issuesbadge]: https://img.shields.io/github/issues/caiosweet/Home-Assistant-custom-components-NASA
[github issues]: https://github.com/caiosweet/Home-Assistant-custom-components-NASA/issues
[downloads_total_shield]: https://img.shields.io/github/downloads/caiosweet/Home-Assistant-custom-components-NASA/total

<!--- Contact Alias and shields -->
[website]: https://hassiohelp.eu/
[websitebadge]: https://img.shields.io/website?down_message=Offline&label=HssioHelp&logoColor=blue&up_message=Online&url=https%3A%2F%2Fhassiohelp.eu
[telegram]: https://t.me/HassioHelp
[telegrambadge]: https://img.shields.io/badge/Chat-Telegram-blue?logo=Telegram
[facebook]: https://www.facebook.com/groups/2062381507393179/
[facebookbadge]: https://img.shields.io/badge/Group-Facebook-blue?logo=Facebook
[forum]: https://forum.hassiohelp.eu/
[forumbadge]: https://img.shields.io/badge/HassioHelp-Forum-blue?logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAA0ppVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8%2BIDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNS1jMDIxIDc5LjE1NTc3MiwgMjAxNC8wMS8xMy0xOTo0NDowMCAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bWxuczp4bXA9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC8iIHhtcE1NOkRvY3VtZW50SUQ9InhtcC5kaWQ6ODcxMjY2QzY5RUIzMTFFQUEwREVGQzE4OTI4Njk5NDkiIHhtcE1NOkluc3RhbmNlSUQ9InhtcC5paWQ6ODcxMjY2QzU5RUIzMTFFQUEwREVGQzE4OTI4Njk5NDkiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTQgKFdpbmRvd3MpIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDo0MWVhZDAwNC05ZWFmLTExZWEtOGY3ZS1mNzQ3Zjc1MjgyNGIiIHN0UmVmOmRvY3VtZW50SUQ9ImFkb2JlOmRvY2lkOnBob3Rvc2hvcDo0MWVhZDAwNC05ZWFmLTExZWEtOGY3ZS1mNzQ3Zjc1MjgyNGIiLz4gPC9yZGY6RGVzY3JpcHRpb24%2BIDwvcmRmOlJERj4gPC94OnhtcG1ldGE%2BIDw/eHBhY2tldCBlbmQ9InIiPz4xQPr3AAADq0lEQVR42rRVW2wMURj%2Bz5lL7V27KG26KIuUEJemdalu3VN3Ei/ipSWUuIV4FB4kHrwo8VLRROJBgkYElZCi4olG4rVoROOSbTa0u7pzO/6Z2Zmd3Z2uevBn/8zsf/7zff/tnKGMMRi/pjM6/j08oKiqCm1tbTA4OAhuoqkS8KKPVjceOcgJngkfnl%2B5JiWH0pQvcfUPhULQ0dEBPp8PDBZZlqGyshLGFKG0fHHr/QfNlxnbjFp7uOcl8VVVj%2BXu9XohkUgY2NRpdJMpc5qWN5971zu7ftsWkSAX2iKLYg3NZ/t6Kxbu2Oi2x4g8IxSKSDR2tLXh2JOn3nAkKv9GAzPtyigS%2BSdV1B3sejhv09lTxTBcCXjRK9buu96%2BZG/7dUYEryK59EXWewNcza7zl%2Br237kpessC4yIITIlGGk88666OtR6VMFKmZhZY9sGsdw1ATgFU1O7et%2Brki56JVUtqsl4kl0CVUjB57vo1Tad7X4Wj9U1S0vRj8HfRSQKVC5auPN7zctqiPTs1Rz2pBV6xcOuq%2BkOPusVAeZWxDg5wl%2Bhz1vW%2BpBFMDIYXt9y%2BF6lr2a6kR7IEmipDeFYsRkVewFcTyAXcBtNMhTxCTTErUxZdu96qLW8varhFsyrnQCQOYNXU8qBp//4TH/jkHZ3UCTXFoncQGKciP1SiN1JDVY2IJwgEjq3jYMVsZgC/HSBw9RnA8CgBjmS3MkdefE638sCV0WGQk9/QXYNRicH%2B7eWwYUGpOT4oq%2Bfq0Upw4SEPVOCLnwOWp5o%2BgskfWEoZe8Qg6CGwcp7XWFVxTc0UYdlMrLmQsP8zVuQcWFNiORFCTSvRQTWQs6W101SRXE7/xiDSBeC5BKywRLx/KqbuA44TYUQS4HHfsLHEcZyhulP32zjEUwL2ACuPt24%2BR0HhnONJBA8IoRlG/4P4/%2B57FTTyC9bUMAQk8OJ9Am69VsHjC2cOJbPaU0iQn4DxrjnSwVwp4eF2XwC63uBVLCchpXgQPAiUUrM8xBwlfeqs%2Bc7JwFn//KHKtAI8IkVejFgIgY8p2etEB7cPDbF32wSE8pwx926XTx6pAcPxxmFlzIo2o/qPy84sb4JTSMb7v3qiGFhJIaAzw1wbkmh8tu4IrqKm4v347V1qmvQGKvjJjEyf7v/pX3GmrGp%2BtT73UDyRHCPLMBDKwUj801dl4P7Fwc8fh0rLwiaBrp2dN2Do%2Bxfb%2Bd%2BE2GwEe%2BEPTYaW1gNQUiKaBP9T/ggwAJik5dEKYSC3AAAAAElFTkSuQmCC

<!--- External Link -->
[APOD]: https://apod.nasa.gov/apod/astropix.html
[EPIC]: https://epic.gsfc.nasa.gov/
[Exoplanet]: https://exoplanetarchive.ipac.caltech.edu/index.html
[InSight]: https://mars.nasa.gov/insight/weather/
[NeoWs]: http://neo.jpl.nasa.gov/
[nasa]: https://api.nasa.gov/
