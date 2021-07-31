# Files Component
Custom Component for Home Assistant that reads a list of files from a directory into a sensor.

This was developed for use alongside the [Gallery Card](https://github.com/TarheelGrad1998/gallery-card) but may have other uses.

## Installation
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

Files must be in the WWW folder, ideally in a subfolder. This component will periodically scan the folder for changes to the files, and is based on the built-in Folder component.

The component can be installed from HACS (use the Custom Repository option), but follow the below instructions to install manually.
1. Create a folder in your `config` directory (normally where your configuration.yaml file lives) named `custom_components`
2. Create a folder in your `custom_components` named `files`
3. Copy the 3 files (_init_.py, manifest.json, and sensor.py) into the `files` folder
4. Create a folder in your `WWW` folder named `images` (or any other name, but be sure to use the proper name below)
5. Add your images/videos to this folder
6. Add the files sensor to your configuration.yaml file
    ```yaml
    - sensor
        - platform: files
          folder: /config/www/images
          filter: '**/*.jpg'
          name: gallery_images
          sort: date
          recursive: True
    ```
7. Restart Home Assistant
8. Check the sensor.gallery_images entity to see if the `fileList` attribute lists your files

### Configuration Variables

| Name | Type | Default | Description
| ---- | ---- | ------- | -----------
| platform | string | **Required** | `files`
| folder | string | **Required** | Folder to scan, must be /config/www/***
| name | string | **Required** | The entity ID for the sensor
| sort | string | **Optional** | One of 'name', 'date', or 'size';  Determines how files are sorted in the Gallery, `Default: date`
| recursive | boolean | **Optional** | True or False; If True, the pattern filter `**` will match any files and zero or more directories, subdirectories and symbolic links to directories. **Note:** Using the `**` pattern in large directory trees may consume an inordinate amount of time , `Default: False` 

## Force Reloading 

The entity will automatically update on a schedule, however, if you need to refresh more often or at some event, you can use the [update_entity service call](https://www.home-assistant.io/integrations/homeassistant/#service-homeassistantupdate_entity).  

    action:
      - service: homeassistant.update_entity
        target:
          entity_id:
          - sensor.gallery_images
  

## Credits

This component largely created from work done by @zsarnett in [the slideshow card](https://github.com/zsarnett/slideshow-card), from which other inspiration was also taken.  
