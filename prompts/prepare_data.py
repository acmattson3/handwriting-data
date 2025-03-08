''' prepare_data for handwriting-data
Takes JSON writing data found in prompt_data/
and converts it into data to train the 
handwriting-synthesis AI found at:
https://github.com/sjvasquez/handwriting-synthesis
'''

import os
import numpy as np
import json
from collections import defaultdict
import drawing


def get_stroke_sequence(filename):
    
    with open(filename) as f:
        strokes = json.load(f)["strokes"]

    coords = []
    for stroke in strokes:
        for i, point in enumerate(stroke):
            coords.append([
                int(point['x']),
                -1*int(point['y']),
                int(i == len(stroke) - 1)
            ])
    coords = np.array(coords)

    coords = drawing.align(coords)
    coords = drawing.denoise(coords)
    offsets = drawing.coords_to_offsets(coords)
    offsets = offsets[:drawing.MAX_STROKE_LEN]
    offsets = drawing.normalize(offsets)
    return offsets

if __name__=="__main__":
    print("Pulling prompt data...")
    fnames = []
    for dirpath, dirnames, filenames in os.walk('prompt_data/'):
        if dirnames:
            continue
        for filename in filenames:
            if filename.startswith('.'):
                continue
            fnames.append(os.path.join(dirpath, filename))

    print("Loading prompt data...")
    stroke_fnames, transcriptions, writer_ids=[],[],[]
    for file in fnames:
        stroke_fnames.append(file)
        with open(file) as f:
            data=json.load(f)
        transcriptions.append(drawing.encode_ascii(data["transcription"]))
        writer_ids.append(0)

    assert len(stroke_fnames)==len(transcriptions)==len(writer_ids), "Uneven lengths!"
    # We're good to this point

    print('Dumping data into numpy arrays...')
    x = np.zeros([len(stroke_fnames), 1200, 3], dtype=np.float32)
    x_len = np.zeros([len(stroke_fnames)], dtype=np.int16)
    c = np.zeros([len(stroke_fnames), 75], dtype=np.int8)
    c_len = np.zeros([len(stroke_fnames)], dtype=np.int8)
    w_id = np.zeros([len(stroke_fnames)], dtype=np.int16)
    valid_mask = np.zeros([len(stroke_fnames)], dtype=np.bool)

    for i, (stroke_fname, c_i, w_id_i) in enumerate(zip(stroke_fnames, transcriptions, writer_ids)):
        if i % 200 == 0:
            print(i, '\t', '/', len(stroke_fnames))
        x_i = get_stroke_sequence(stroke_fname)
        valid_mask[i] = ~np.any(np.linalg.norm(x_i[:, :2], axis=1) > 60)

        x[i, :len(x_i), :] = x_i
        x_len[i] = len(x_i)

        c[i, :len(c_i)] = c_i
        c_len[i] = len(c_i)

        w_id[i] = w_id_i

    if not os.path.isdir('processed'):
        os.makedirs('processed')

    np.save('processed/x.npy', x[valid_mask])
    np.save('processed/x_len.npy', x_len[valid_mask])
    np.save('processed/c.npy', c[valid_mask])
    np.save('processed/c_len.npy', c_len[valid_mask])
    np.save('processed/w_id.npy', w_id[valid_mask])
    print("Data has been prepared!")
