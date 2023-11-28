"""
Author: Tara Sassel
Date: 26/10/2022
"""
import numpy as np
from typing import Tuple

def get_cyclicmean_data(which_data: str, drive: str) -> Tuple[list, list]:
  """
    Function that retrun the path and color list.
    This makes it easer to do repetitive figures.

    which_data:
        all
        all_V2 -> Includes 300kPa Ampl 20kPa
        zeta5
        zeta10
        zeta20
        zeta30
        pav100
        pav200
        pav300_V2 -> Includes 300kPa Ampl 20kPa
        pav300

    drive:
        example: C, D, E, F
  """
  # Defining Path
  path_100_5 = fr'{drive}:\CyclicLoading\Cyclicmean\TX100_FC0p25to0p25_amp5\merged_data'
  path_100_10 = fr'{drive}:\CyclicLoading\Cyclicmean\TX100_FC0p25to0p25_amp10\merged_data'
  path_100_20 = fr'{drive}:\CyclicLoading\Cyclicmean\TX100_FC0p25to0p25_amp20\merged_data'
  path_100_30 = fr'{drive}:\CyclicLoading\Cyclicmean\TX100_FC0p25to0p25_amp30\merged_data'

  path_200_10 = fr'{drive}:\CyclicLoading\Cyclicmean\TX200_FC0p25to0p25_amp10\merged_data'
  path_200_20 = fr'{drive}:\CyclicLoading\Cyclicmean\TX200_FC0p25to0p25_amp20\merged_data'
  path_200_40 = fr'{drive}:\CyclicLoading\Cyclicmean\TX200_FC0p25to0p25_amp40\merged_data'
  path_200_60 = fr'{drive}:\CyclicLoading\Cyclicmean\TX200_FC0p25to0p25_amp60\merged_data'

  path_300_15 = fr'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data'
  path_300_20 = fr'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp20\merged_data'
  path_300_30 = fr'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp30\merged_data'
  path_300_60 = fr'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp60\merged_data'
  path_300_90 = fr'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data'

  whole_path_list = [
          path_100_5,
          path_100_10,
          path_100_20,
          path_100_30,
          path_200_10,
          path_200_20,
          path_200_40,
          path_200_60,
          path_300_15,
          path_300_30,
          path_300_60,
          path_300_90
      ]

  whole_color_list = [
          '#edf8e9',
          '#bae4b3',
          '#74c476',
          '#238b45',
          '#fee5d9',
          '#fcae91',
          '#fb6a4a',
          '#cb181d',
          '#f0f9e8',
          '#7bccc4',
          '#43a2ca',
          '#0868ac'
      ]

  if which_data == 'all':
      path_list = whole_path_list[:]
      color_list = whole_color_list[:]

  if which_data == 'all_V2':
       path_list = whole_path_list[:]
       color_list = whole_color_list[:]
       path_list.insert(9, path_300_20)
       color_list.insert(9, '#bae4bc')

  if which_data == 'pav100':
      path_list = whole_path_list[0:4]
      color_list = whole_color_list[0:4]

  if which_data == 'pav200':
      path_list = whole_path_list[4:8]
      color_list = whole_color_list[4:8]

  if which_data == 'pav300':
      path_list = whole_path_list[8:12]
      color_list = whole_color_list[8:12]

  if which_data == 'pav300_V2':
      path_list = whole_path_list[8:12]
      color_list = whole_color_list[8:12]
      path_list.insert(1, path_300_20)
      color_list.insert(1, '#bae4bc')

  if which_data == 'zeta5':
      path_list = [whole_path_list[i] for i in [0,4,8]]
      color_list = [whole_color_list[i] for i in [0,4,8]]

  if which_data == 'zeta10':
      path_list =[whole_path_list[i] for i in [1,5,9]]
      color_list = [whole_color_list[i] for i in [1,5,9]]

  if which_data == 'zeta20':
      path_list = [whole_path_list[i] for i in [2,6,10]]
      color_list = [whole_color_list[i] for i in [2,6,10]]

  if which_data == 'zeta30':
      path_list = [whole_path_list[i] for i in [3,7,11]]
      color_list = [whole_color_list[i] for i in [3,7,11]]

  return path_list, color_list
