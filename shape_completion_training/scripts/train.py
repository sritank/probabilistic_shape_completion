#! /usr/bin/env python
import argparse

from shape_completion_training.utils import data_tools
from shape_completion_training.model.modelrunner import ModelRunner
from shape_completion_training.model import default_params


# params = {
#     'num_latent_layers': 200,
#     'translation_pixel_range_x': 10,
#     'translation_pixel_range_y': 10,
#     'translation_pixel_range_z': 10,
#     # 'use_final_unet_layer': False,
#     'simulate_partial_completion': False,
#     'simulate_random_partial_completion': False,
#     # 'network': 'VoxelCNN',
#     # 'network': 'VAE_GAN',
#     # 'network': 'Augmented_VAE',
#     # 'network': 'Conditional_VCNN',
#     'network': 'NormalizingAE',
#     'batch_size': 16,
#     'learning_rate': 1e-3,
#     'flow': 'Flow/July_02_10-47-22_d8d84f5d65'
# }
override_params = {
    "use_flow_during_inference": True
}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process args for training")
    parser.add_argument('--tmp', action='store_true')
    parser.add_argument('--group', default=None)
    args = parser.parse_args()
    params = default_params.get_default_params(group_name=args.group)
    params.update(override_params)


    train_data_shapenet, test_data_shapenet = data_tools.load_shapenet([data_tools.shape_map["mug"]])

    # data = data_ycb
    data = train_data_shapenet

    # if params['network'] == 'VoxelCNN':
    #     sim_input_fn=data_tools.simulate_omniscient_input
    # elif params['network'] == 'AutoEncoder':
    sim_input_fn= data_tools.simulate_2_5D_input
    
    data = data_tools.simulate_input(data,
                                     params['translation_pixel_range_x'],
                                     params['translation_pixel_range_y'],
                                     params['translation_pixel_range_z'],
                                     sim_input_fn=sim_input_fn)
    # data = data_tools.simulate_condition_occ(data,
    #                                          turn_on_prob=params['turn_on_prob'],
    #                                          turn_off_prob=params['turn_off_prob'])

    if params['simulate_partial_completion']:
        data = data_tools.simulate_partial_completion(data)
    if params['simulate_random_partial_completion']:
        data = data_tools.simulate_random_partial_completion(data)


    if args.tmp:
        mr = ModelRunner(training=True, params=params, group_name=None)
    else:
        mr = ModelRunner(training=True, params=params, group_name=params['network'])

    mr.train_and_test(data)
