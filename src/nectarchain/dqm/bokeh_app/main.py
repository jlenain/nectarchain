from app_hooks import get_rundata, make_camera_displays, make_timelines

# bokeh imports
from bokeh.layouts import gridplot, layout, row
from bokeh.models import ColumnDataSource, Panel, Select, Tabs  # , NumericInput
from bokeh.plotting import curdoc

# ctapipe imports
from ctapipe.coordinates import EngineeringCameraFrame
from ctapipe.instrument import CameraGeometry

from nectarchain.dqm.db_utils import DQMDB

geom = CameraGeometry.from_name("NectarCam-003")
geom = geom.transform_to(EngineeringCameraFrame())


def update_camera_displays(attr, old, new):
    runid = run_select.value
    new_rundata = get_rundata(db, runid)
    new_data = make_camera_displays(db, new_rundata, runid)

    # TODO: TRY TO USE `stream` INSTEAD, ON UPDATES:
    # display.datasource.stream(new_data)
    # displays[parentkey][childkey].datasource.stream(image)

    source.stream(new_data)


def update_timelines(attr, old, new):
    runid = run_select.value
    new_rundata = get_rundata(db, runid)
    new_data = make_timelines(db, new_rundata, runid)
    source.stream(new_data)


print("Opening connection to ZODB")
db = DQMDB(read_only=True).root
print("Getting list of run numbers")
runids = sorted(list(db.keys()), reverse=True)

# First, get the run id with the most populated result dictionary
# On the full DB, this takes an awful lot of time, and saturates the RAM on the host
# VM (gets OoM killed)
# run_dict_lengths = [len(db[r]) for r in runids]
# runid = runids[np.argmax(run_dict_lengths)]

runid = "NectarCAM_Run0008"
# runid = runids[0]
print(f"We will start with run {runid}")

print("Defining Select")
# runid_input = NumericInput(value=db.root.keys()[-1], title="NectarCAM run number")
run_select = Select(value=runid, title="NectarCAM run number", options=runids)

print(f"Getting data for run {run_select.value}")
source = ColumnDataSource(data=get_rundata(db, run_select.value))
displays = make_camera_displays(db, source, runid)
timelines = make_timelines(db, source, runid)

run_select.on_change("value", update_camera_displays, update_timelines)

controls = row(run_select)

# # TEST:
# attr = 'value'
# old = runid
# new = runids[1]
# update_camera_displays(attr, old, new)

ncols = 3
camera_displays = [
    displays[parentkey][childkey].figure
    for parentkey in displays.keys()
    for childkey in displays[parentkey].keys()
]
list_timelines = [
    timelines[parentkey][childkey]
    for parentkey in timelines.keys()
    for childkey in timelines[parentkey].keys()
]

layout_camera_displays = gridplot(
    camera_displays,
    sizing_mode="scale_width",
    ncols=ncols,
)

layout_timelines = gridplot(list_timelines, sizing_mode="scale_width", ncols=2)

# Create different tabs
tab_camera_displays = Panel(child=layout_camera_displays, title="Camera displays")
tab_timelines = Panel(child=layout_timelines, title="Timelines")

# Combine panels into tabs
tabs = Tabs(tabs=[tab_camera_displays, tab_timelines])

# Add to the Bokeh document
curdoc().add_root(layout([controls, tabs]))
curdoc().title = "NectarCAM Data Quality Monitoring web app"
