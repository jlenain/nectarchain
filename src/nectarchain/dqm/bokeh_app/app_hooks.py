import re

import numpy as np
from bokeh.plotting import figure
from ctapipe.coordinates import EngineeringCameraFrame
from ctapipe.instrument import CameraGeometry

# ctapipe imports
from ctapipe.visualization.bokeh import CameraDisplay
from ctapipe_io_nectarcam import constants

NOTINDISPLAY = [
    "col0",
    "All",
    "Physical",
    "Pedestals",
    "Others",
    "Wrong times",
    "TRIGGER-.*",
    "PED-INTEGRATION-.*",
    "START-TIMES",
    "WF-.*",
    ".*PixTimeline-.*",
]
TEST_PATTERN = "(?:% s)" % "|".join(NOTINDISPLAY)

geom = CameraGeometry.from_name("NectarCam-003")
geom = geom.transform_to(EngineeringCameraFrame())


def get_rundata(src, runid):
    run_data = dict(src[runid])
    items = []
    # Flatten input dictionary
    for parentkey, parentvalue in run_data.items():
        for childkey, childvalue in parentvalue.items():
            items.append((childkey, childvalue))

    new_data = dict(items)
    return new_data


def make_timelines(source, runid):
    timelines = dict()
    for key in source.keys():
        if re.match("(?:.*PixTimeline-.*)", key):
            print(f"Run id {runid} Preparing plot for {key}")
            timelines[key] = figure(title=key)
            evts = np.arange(len(source[key]))
            timelines[key].line(x=evts, y=source[key])
    return timelines


def make_camera_displays(source, runid, original_keys=None):
    displays = dict()
    for key in source:
        if not re.match(TEST_PATTERN, key):
            print(f"Run id {runid} Preparing plot for {key}")
            # Reset each display
            displays[key] = np.zeros(shape=constants.N_PIXELS)

            displays[key] = make_camera_display(source, key=key)
    # Fill camera displays with 0 for absent keys in new data
    try:
        for key in original_keys:
            if key not in source:
                displays[key] = make_camera_display(source, key=key)
    except TypeError:
        pass
    return displays


def make_camera_display(source, key):
    # Example camera display
    try:
        image = source[key]
    except KeyError:
        image = np.zeros(shape=constants.N_PIXELS)
    image = np.nan_to_num(image, nan=0.0)
    display = CameraDisplay(geometry=geom)
    try:
        display.image = image
    except ValueError as e:
        print(
            f"Caught {type(e).__name__} for {key}, filling display"
            f"with zeros. Details: {e}"
        )
        image = np.zeros(shape=display.image.shape)
        display.image = image
    except KeyError as e:
        print(
            f"Caught {type(e).__name__} for {key}, filling display"
            f"with zeros. Details: {e}"
        )
        image = np.zeros(shape=constants.N_PIXELS)
        display.image = image
    display.add_colorbar()
    display.set_limits_minmax(
        zmin=np.mean(image) - 4.0 * np.std(image),
        zmax=np.mean(image) + 4.0 * np.std(image),
    )
    display.figure.title = key
    return display
