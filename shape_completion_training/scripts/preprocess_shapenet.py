#! /usr/bin/env python
import shape_completion_training.utils.shapenet_storage
from shape_completion_training.utils import data_tools

if __name__ == "__main__":
    shape_completion_training.utils.shapenet_storage.write_shapenet_to_filelist(test_ratio=0.02, shape_ids=data_tools.shapenet_labels(["mug"]))
