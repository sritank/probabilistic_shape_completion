"""
Gets a bounding box for shapes
"""
from shape_completion_training.voxelgrid import conversions
from shape_completion_training.utils.matrix_math import rotzyx, rotxyz
import numpy as np
import tensorflow as tf


def get_aabb(voxelgrid, scale=0.01):
    """
    Returns the axis aligned bounding box for the voxelgrid
    @param voxelgrid:
    @param scale:
    @return:
    """
    return get_aabb_from_pts(conversions.voxelgrid_to_pointcloud(voxelgrid, scale=scale))


def get_aabb_from_pts(pts):
    ub, lb = np.max(pts, axis=0), np.min(pts, axis=0)
    borders = [[lb[0], lb[1], lb[2]],
               [lb[0], lb[1], ub[2]],
               [lb[0], ub[1], lb[2]],
               [lb[0], ub[1], ub[2]],
               [ub[0], lb[1], lb[2]],
               [ub[0], lb[1], ub[2]],
               [ub[0], ub[1], lb[2]],
               [ub[0], ub[1], ub[2]],
               ]
    return np.array(borders)


def get_bounding_box_for_elem(voxelgrid, th_x, th_y, th_z, scale=0.01, degrees=False):
    # if tf.is_tensor(elem["angle"]):
    #     elem = {k: v.numpy() for k, v in elem.items()}
    # th = np.pi * int(elem["angle"]) / 180

    pts = conversions.voxelgrid_to_pointcloud(voxelgrid, scale=scale)
    pts = np.dot(rotxyz(-th_x, -th_y, -th_z, degrees)[0:3, 0:3], pts.transpose()).transpose()
    bounds = get_aabb_from_pts(pts)
    bounds = np.dot(rotzyx(th_x, th_y, th_z, degrees)[0:3, 0:3], bounds.transpose()).transpose()
    # vg_oriented = conversions.transform_voxelgrid(elem["gt_occ"], T(-th), scale=0.01)
    return bounds


def flatten_bounding_box(bounding_box):
    return tf.keras.layers.Flatten()(tf.cast(bounding_box, tf.float32))


def unflatten_bounding_box(latent):
    return tf.reshape(latent, [8,3])
