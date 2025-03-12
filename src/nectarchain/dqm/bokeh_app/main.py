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


def update_data(attr, old, new):
    runid = run_select.value
    new_rundata = get_rundata(db, runid)

    new_displays = make_camera_displays(new_rundata, runid, original_keys)
    new_timelines = make_timelines(new_rundata, runid)

    # Merging dictionaries
    # (cf. https://www.geeksforgeeks.org/python-merging-two-dictionaries/):
    new_data = new_displays | new_timelines

    # Fill missing columns in new data with empty lists
    for key in original_keys:
        if key not in new_data:
            new_data[key] = []

    breakpoint()
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
original_keys = list(source.data.keys())

displays = make_camera_displays(
    source=source.data,
    runid=runid,
    original_keys=original_keys,
)
timelines = make_timelines(source.data, runid)

run_select.on_change("value", update_data)

controls = row(run_select)

# # TEST:
# attr = 'value'
# old = runid
# new = runids[1]
# update_camera_displays(attr, old, new)

ncols = 3
camera_displays = [displays[key].figure for key in displays.keys()]
list_timelines = [timelines[key] for key in timelines.keys()]

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
