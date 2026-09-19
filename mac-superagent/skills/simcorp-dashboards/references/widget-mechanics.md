# Dashboard mechanics

Everything here is from the SimCorp Dashboards user manual, September 2025, cited by section. Where
the client install differs from this, the install wins on availability and naming, and the
difference is recorded in `widget-catalogue.md`.

## Build order

1. Add a dashboard through the New Dashboard item on the Show Applets menu. The path and naming
   deviate between manager applications, so check the application before writing a click path.
   A new dashboard is empty until a canvas is created or opened. (3.1)
2. Create or apply a layout from the icon at the bottom of the dashboard, name it, and decide on
   Autosave. A layout is the highest level of user interface configuration and decides which
   dashboards exist and which canvases each holds. (3.2, 14)
3. Create a canvas with New in the CANVAS ribbon group, naming it and setting the tile size. A
   canvas built in one manager application can be used in any other, subject to permission and
   application access. (3.3)
4. Place widgets, one per tile, then Save in the CANVAS ribbon group or Ctrl+S. (3.3, 3.5)
5. Page collections only where several canvases act as pages, added with New page in the Page
   ribbon group. Alternative Investment Manager uses them heavily and calls a collection a layout.
   (3.4)

Edit mode must be on before any element can be added, changed or permissioned. Saving prompts for
all pending changes at once, and answering No rolls every one of them back. (2.1, 3.5)

## Adding a widget

Edit canvas, select an empty tile, Add in the WIDGET ribbon group, pick the widget type, then in
the Widget Configuration window either take an existing configuration or select (New
configuration) and set the UI type. Four fields are common to every configuration: Widget ID,
Title, Type which shows the chosen data source, and UI type. Save closes the window. (3.6.1)

After the widget is populated, the right click menu carries the per widget commands, Select Fields
adds columns to a grid, and fields reorder by dragging the column title. (3.6.1)

## Display types

Chart. Set UI type Chart, then Chart Editor from the widget right click menu for Data, Chart area,
Legend, Axis, Expansion and Add view, where Add view picks the chart type from pies through full
stacked spline areas. Show Title, Show Legend and Add annotation are right click options, Drill
Down opens the underlying data, and clearing Show summary specification type in the Legend section
removes the appended Count or Application specific text. An empty chart usually means no data for
the chosen parameters. (3.6.3.1)

Table. Set UI type Table, save, then use the right click menus, which differ by where in the table
the click lands, to select fields and format. (3.6.3.2)

Pivot. Set UI type Pivot, save, then Select Pivot Fields to choose fields, and the right click menu
on the top row to change the configuration. (3.6.3.3)

Group. A one dimensional summary table. Insert Group from the right click menu adds a grouping
field, Edit Search Filter opens Filter Properties where the group is named and given a field and a
domain value. The rest column counts everything that fell into no group. (3.6.3.4)

Group Matrix. A two dimensional summary. Insert Group on the vertical axis and Insert Column Group
on the horizontal axis, each opening Filter Properties. A cell is the aggregate of the data
satisfying both selections. (3.6.3.5)

Options specific to Group and Group Matrix. (3.6.3.5)

| Option | Effect |
| --- | --- |
| Show all row, Show all column | display the All row or column with the total |
| Always show The rest row or column | keep The rest visible even when nothing falls into it |
| Rename All, Rename The rest | custom names for those rows and columns |
| Count unique on transaction number | count a transaction once per group instead of once per matching category |
| Minutes before becoming obsolete | the update interval for the widget |

## Filters

The filter icon sits in the widget header whenever filtering is possible and turns blue when a
filter is active, with the applied filters in the hover tooltip. Left click the icon to create a
filter, or right click it to apply or clear existing ones. Filter Properties takes a description,
an And or Or operator, added selections through the plus sign, a field, an operator and values.
Show selected fields only limits the field list to what the widget already displays. A column
header filter turns that column's icon blue and is reflected in the header icon. (3.6.5)

The limitation that shapes every exception design: a filter applies to the main section of the
widget only, never to the drill down data underneath. (3.6.5)

## Conditional formatting

Right click a field, Edit Properties, Conditional Format tab, then a conditional formula, for
example green for cash inflow and red for cash outflow. (3.6.6)

## Time dependency fields

Available on all display types and all widget data sources. SimCorp Dimension converts database
time to local user time before comparing intervals, so time zones are handled. Two families.
(3.6.7)

1. Time to deadline. Days from today to the transaction settlement date, or minutes from now to
   the custodian cut off time.
2. Time from. Minutes from transaction creation to now, or days from trade date to today.

Worked shapes from the manual. Group transactions by settlement date with one group filtered on
settlement date before today and another on settlement date tomorrow with requested status Free
deal. Group by settlement cut off time by splitting under and over a two hour horizon, for example
a group filtered on settlement cut off time less than 0:00. (3.6.7)

Calendar convention trap. Reference dates must share a calendar convention across everything in
scope. A security whose calendar treats Saturday as a business day settles on a Saturday, and on
the Friday view it is neither overdue nor settling today nor settling on the next business day, so
it silently lands in The rest. (3.6.7)

## Sizing and detail levels

The first plus and minus control resizes the widget across tiles. The second moves the horizontal
splitter, and a widget can be configured without a details view. At three tiles wide a third level
of detail becomes available, so a large widget that should not carry a third level is better built
by increasing the number of canvas tiles and keeping the widget three tiles wide. In full size view
the splitter position is saved automatically. (3.6.2)

## Saving data against saving elements

Edit mode on saves dashboard elements. Edit mode off saves data changes in widgets, which is
currently supported only in Alternative Investment Manager. Data changes must all be saved before
edit mode can be enabled, and a widget holding invalid data blocks the save. (3.6.4, 3.5)

## Copying and deleting

A shared canvas saved as a new canvas is identical including its widgets, the widget
configurations are shared between source and copy, and permissions are not copied. A page
collection copied with Save As duplicates each canvas and each widget, which is what makes
independent permissions on the copy possible. An element in use elsewhere cannot be deleted, only
removed from the canvas. (2.1, 3.4)

## Permissions

Owner first: only the owner, or a member of the authorisation profile set as owner, can set
permissions, and the owning profile is marked with an asterisk in Record Permissions. Add brings
in further profiles, Change Owner hands ownership over, Set as Default applies the current
settings to future canvases. Page collection permissions from the PAGE COLLECTION ribbon group,
canvas from the Canvas ribbon group, widget from the configuration sub window in the widget header
with edit mode on, layout from the control in the bottom right of the layout. (3.7.3 to 3.7.7)

Data authorisation is separate and comes from Maintenance, System Access, General Authorisation
plus user specific authorisation, over portfolios, instruments and transactions. Where a service
feeds the widget the service user needs the same read access. A widget referencing a setup the
user cannot reach still opens, but the drill down is empty or errors. (3.7.1)

## Interface options for trade processing

Trade Processing Dashboard and Alerts tab of Interface Options. (5.4)

| Option | Effect |
| --- | --- |
| Disregard data older than number of days | hides data unchanged for longer than this; a low value improves performance, seven days is workable in production |
| Minutes between verification of data | full refresh interval, default 60, anything below 60 is treated as 60, zero means only at server start or date change; volatile changes such as status appear at once, static changes such as a renamed counterparty wait for verification or reload |
| Minutes between check for new sources | how long a new widget configuration waits to be picked up; one minute while configuring, four hours in production |
| Delete closed alerts after number of days | retention of closed alerts |

## Editing tree view data through a spreadsheet

Block Selection Tree on the Home ribbon enables block selection in a tree list, Copy on the Tree
List ribbon exports the block, and Paste writes it back into cells that are not read only, either
at a single cell anchor, across selected columns, or across selected rows where fewer copied rows
repeat to fill the selection. (3.6.8)

## When a widget shows nothing

Work the list in order. Is the canvas saved, because the server does not prepare data for an
unsaved canvas. Is the service for that data source running and does its user have access to the
setup, portfolios and transactions. Is a filter active in the header or in a column. Is the data
older than the Disregard data older than setting. Is the change a static one waiting for
verification. For a chart, are there simply no records for the parameters. For a group, has
everything landed in The rest because of a calendar convention mismatch. (3.6.3.1, 3.6.5, 3.6.7,
3.7.1, 5.2, 5.4)
