from datetime import timedelta
import glob
import logging
import os

import voluptuous as vol

from homeassistant.helpers.entity import Entity
import homeassistant.helpers.config_validation as cv
from homeassistant.components.sensor import PLATFORM_SCHEMA

_LOGGER = logging.getLogger(__name__)

CONF_FOLDER_PATHS = 'folder'
CONF_FILTER = 'filter'
CONF_NAME = 'name'
CONF_SORT = 'sort'
CONF_RECURSIVE = 'recursive'
DEFAULT_FILTER = '*'
DEFAULT_SORT = 'date'
DEFAULT_RECURSIVE = False

DOMAIN = 'files'

SCAN_INTERVAL = timedelta(minutes=1)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_FOLDER_PATHS): cv.isdir,
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_FILTER, default=DEFAULT_FILTER): cv.string,
    vol.Optional(CONF_SORT, default=DEFAULT_SORT): cv.string,
    vol.Optional(CONF_RECURSIVE, default=DEFAULT_RECURSIVE): cv.boolean,
})

def get_files_list(folder_path, filter_term, sort, recursive):
    """Return the list of files, applying filter."""
    query = folder_path + filter_term
    """files_list = glob.glob(query)"""
    if sort == 'name':
        files_list = sorted(glob.glob(query, recursive=recursive))
    elif sort == 'size':
        files_list = sorted(glob.glob(query, recursive=recursive), key=os.path.getsize)
    else:
        files_list = sorted(glob.glob(query, recursive=recursive), key=os.path.getmtime)
    return files_list


def get_size(files_list):
    """Return the sum of the size in bytes of files in the list."""
    size_list = [os.stat(f).st_size for f in files_list if os.path.isfile(f)]
    return sum(size_list)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the folder sensor."""
    path = config.get(CONF_FOLDER_PATHS)
    name = config.get(CONF_NAME)

    if not hass.config.is_allowed_path(path):
        _LOGGER.error("folder %s is not valid or allowed", path)
    else:
        folder = FilesSensor(path, name, config.get(CONF_FILTER), config.get(CONF_SORT), config.get(CONF_RECURSIVE))
        add_entities([folder], True)

class FilesSensor(Entity):
    """Representation of a folder."""
 
    ICON = 'mdi:folder'
 
    def __init__(self, folder_path, name, filter_term, sort, recursive):
        """Initialize the data object."""
        folder_path = os.path.join(folder_path, '')  # If no trailing / add it
        self._folder_path = folder_path   # Need to check its a valid path
        self._filter_term = filter_term
        self._number_of_files = None
        self._size = None
        #self._name = os.path.split(os.path.split(folder_path)[0])[1]
        self._name = name
        self._unit_of_measurement = 'MB'
        self._sort = sort
        self._recursive = recursive
 
    def update(self):
        """Update the sensor."""
        files_list = get_files_list(self._folder_path, self._filter_term, self._sort, self._recursive)
        self.fileList = files_list
        self._number_of_files = len(files_list)
        self._size = get_size(files_list)
 
    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name
 
    @property
    def state(self):
        """Return the state of the sensor."""
        decimals = 2
        size_mb = round(self._size/1e6, decimals)
        return size_mb
 
    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self.ICON
 
    @property
    def device_state_attributes(self):
        """Return other details about the sensor state."""
        attr = {
            'path': self._folder_path,
            'filter': self._filter_term,
            'number_of_files': self._number_of_files,
            'bytes': self._size,
            'fileList': self.fileList,
            'sort': self._sort,
            'recursive': self._recursive
            }
        return attr
 
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement
 
