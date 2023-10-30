import xml.etree.ElementTree as ET
from datetime import datetime

# Create the root element
root = ET.Element("WhiteboardCaptureSession")

# General
general = ET.SubElement(root, "General")

# Form
form = ET.SubElement(general, "Form")
form.set("id", "a01-001z")
form.set("writerID", "10028")

# Calculate saveTime as an example (you may need to adjust this calculation)
now = datetime.now()
save_time = (now.year * 12 + now.month) * 31 + now.day
save_time = (save_time * 24 + now.hour) * 60 + now.minute
save_time = (save_time * 60 + now.second) + (now.microsecond / 1000000.0)
form.set("saveTime", str(save_time))

# CaptureTime
capture_time = ET.SubElement(general, "CaptureTime")
capture_time.set("time", now.strftime("%H:%M:%S"))
capture_time.set("year", str(now.year))
capture_time.set("month", str(now.month))
capture_time.set("dayOfMonth", str(now.day))
capture_time.set("dayOfWeek", str(now.weekday()))

# Setting
setting = ET.SubElement(general, "Setting")
setting.set("location", "IAM university of Berne (CH)")
setting.set("producer", "Marcus Liwicki (liwicki (at) iam.unibe.ch)")
setting.set("system", "eBeam System 3 YCap 1.0")

# Transcription
transcription = ET.SubElement(root, "Transcription")

# Text
text = ET.SubElement(transcription, "Text")
text.text = "By Trevor Williams. A move to stop Mr. Gaitskell from nominating any more Labour life Peers is to be made at a meeting of Labour M Ps tomorrow. Mr. Michael Foot has put down a resolution on the subject and he is to be backed by Mr. Will Griffiths, MP for"

# You can populate the TextLine, Word, and Char elements here as per your data

# WhiteboardDescription
whiteboard = ET.SubElement(root, "WhiteboardDescription")
whiteboard.set("corner", "top_left")

# DiagonallyOpppositeCoords
diag_coords = ET.SubElement(whiteboard, "DiagonallyOppositeCoords")
diag_coords.set("x", "6912")
diag_coords.set("y", "8798")

# VerticallyOppositeCoords
vert_coords = ET.SubElement(whiteboard, "VerticallyOppositeCoords")
vert_coords.set("x", "214")
vert_coords.set("y", "8878")

# HorizontallyOppositeCoords
hor_coords = ET.SubElement(whiteboard, "HorizontallyOpppositeCoords")
hor_coords.set("x", "7038")
hor_coords.set("y", "196")

# StrokeSet
stroke_set = ET.SubElement(root, "StrokeSet")

# Add Stroke and Point elements here to populate the strokes and points

# Create an ElementTree object and write the XML to a file or serialize it
tree = ET.ElementTree(root)
tree.write("whiteboard_data.xml")

# You can also use tree.tostring(root) to get the XML as a string
