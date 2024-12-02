# -*- encoding: utf-8 -*-
'''
@File    :   prepare_data_from_nnUNet.py
@Time    :   2023/12/10 23:07:39
@Author  :   Haoyu Wang
@Contact :   small_dark@sina.com
@Brief   :   pre-process nnUNet-style dataset into SAM-Med3D-style
'''

import os.path as osp
import os
import json
import shutil
import nibabel as nib
from tqdm import tqdm
import torchio as tio
import torch

######注意！！！！！！！！！
######进行重采样和二值化的时候要看dataset.json中的trainset 和valset的数据路径对不对
def resample_nii(input_path: str, output_path: str, target_spacing: tuple = (1.5, 1.5, 1.5), n=None,
                 reference_image=None, mode="linear"):
    """
    Resample a nii.gz file to a specified spacing using torchio.

    Parameters:
    - input_path: Path to the input .nii.gz file.
    - output_path: Path to save the resampled .nii.gz file.
    - target_spacing: Desired spacing for resampling. Default is (1.5, 1.5, 1.5).
    """

    # Load the nii.gz file using torchio
    subject = tio.Subject(
        img=tio.ScalarImage(input_path),
    )

    # test_image = nib.load('C:\\pycharm workspace\\SAM-Med3D-main\\data\\nnU-NetStyle-valdata\\WORD\\labelsVl\\word_0001.nii.gz')
    # img_data = test_image.get_fdata()
    # img_tensor = torch.from_numpy(img_data)
    # print('test_image_type',img_tensor) ####torch.float64
    # print('test_image_max', img_tensor.max())
    # print('test_image_min', img_tensor.min())
    # print('list_test', torch.unique(img_tensor).tolist())



    resampler = tio.Resample(target=target_spacing, image_interpolation=mode)
    resampled_subject = resampler(subject)


    if (n != None):
        image = resampled_subject.img
        tensor_data = image.data

        # if tensor_data.dtype == torch.int16:
        #     tensor_data = tensor_data.to(torch.uint8)
        # print('type',tensor_data.dtype)
        # print('max', tensor_data.max())
        # print('min', tensor_data.min())
        # print('list',torch.unique(tensor_data).tolist())
        #     print('min', tensor_data.min())
        #
        #     print('transform')
        #
        #     print('max', tensor_data.max())
        #     print('min', tensor_data.min())
        if (isinstance(n, int)):
            n = [n]
        for ni in n:
            tensor_data[tensor_data == ni] = -1
        tensor_data[tensor_data != -1] = 0
        tensor_data[tensor_data != 0] = 1
        save_image = tio.ScalarImage(tensor=tensor_data, affine=image.affine)
        reference_size = reference_image.shape[1:]  # omitting the channel dimension
        cropper_or_padder = tio.CropOrPad(reference_size)
        save_image = cropper_or_padder(save_image)
    else:
        save_image = resampled_subject.img

    save_image.save(output_path)


def resample_nii_forWord(input_path: str, output_path: str, target_spacing: tuple = (1.5, 1.5, 1.5), n=None,
                 reference_image=None, mode="linear"):
    """
    Resample a nii.gz file to a specified spacing using torchio.

    Parameters:
    - input_path: Path to the input .nii.gz file.
    - output_path: Path to save the resampled .nii.gz file.
    - target_spacing: Desired spacing for resampling. Default is (1.5, 1.5, 1.5).
    """

    # Load the nii.gz file using torchio
    nii_image = nib.load('C:\\pycharm workspace\\SAM-Med3D-main\\data\\nnU-NetStyle-valdata\\WORD\./imagesVl\word_0001.nii.gz')
    print('path',input_path)
    data = nii_image.get_fdata()
    img_tensor = torch.from_numpy(data)

    print('datashape',img_tensor.shape)
    print('type', img_tensor.dtype)
    print('max', img_tensor.max())
    print('min', img_tensor.min())
    print('list', torch.unique(data).tolist())


    subject = tio.Subject(
        img=tio.Image(tensor=data,affine=nii_image.affine),
    )


    resampler = tio.Resample(target=target_spacing, image_interpolation=mode)
    resampled_subject = resampler(subject)


    if (n != None):
        image = resampled_subject.img
        tensor_data = image.data

        print('type',tensor_data.dtype)
        print('max', tensor_data.max())
        print('min', tensor_data.min())
        print('list',torch.unique(tensor_data).tolist())

        if (isinstance(n, int)):
            n = [n]
        for ni in n:
            tensor_data[tensor_data == ni] = -1
        tensor_data[tensor_data != -1] = 0
        tensor_data[tensor_data != 0] = 1
        save_image = tio.ScalarImage(tensor=tensor_data, affine=image.affine)
        reference_size = reference_image.shape[1:]  # omitting the channel dimension
        cropper_or_padder = tio.CropOrPad(reference_size)
        save_image = cropper_or_padder(save_image)
    else:
        save_image = resampled_subject.img

    save_image.save(output_path)




dataset_root = "C:\\pycharm workspace\\SAM-Med3D-main\data\\nnU-NetStyle-valdata\\"
dataset_list = [

    'WORD',
    'FLARE22',
]

target_dir = "D:\\new_sam3d_valdataset\\"

for dataset in dataset_list:
    dataset_dir = osp.join(dataset_root, dataset)
    meta_info = json.load(open(osp.join(dataset_dir, "dataset.json")))

    print(meta_info['name'], meta_info['modality'])
    num_classes = len(meta_info["labels"]) - 1
    print("num_classes:", num_classes, meta_info["labels"])
    resample_dir = osp.join(dataset_dir, "imagesTr_1.5")
    os.makedirs(resample_dir, exist_ok=True)
    for idx, cls_name in meta_info["labels"].items():
        cls_name = cls_name.replace(" ", "_")
        idx = int(idx)
        #dataset_name = dataset.split("_", maxsplit=1)[1]
        dataset_name = dataset
        target_cls_dir = osp.join(target_dir, cls_name, dataset_name)
        target_img_dir = osp.join(target_cls_dir, "imagesTs")
        target_gt_dir = osp.join(target_cls_dir, "labelsTs")
        os.makedirs(target_img_dir, exist_ok=True)
        os.makedirs(target_gt_dir, exist_ok=True)
        for item in tqdm(meta_info["validation"], desc=f"{dataset_name}-{cls_name}"):
            img, gt = item["image"], item["label"]
            if dataset == 'Amos' or dataset == 'BTCV' or dataset == 'WORD' or dataset == 'FLARE22':
                img = osp.join(dataset_dir, img)
            else:
                img = osp.join(dataset_dir, img.replace(".nii.gz", "_0000.nii.gz"))
            gt = osp.join(dataset_dir, gt)
            resample_img = osp.join(resample_dir, osp.basename(img))
            if (not osp.exists(resample_img)):
                resample_nii(img, resample_img)
            img = resample_img

            target_img_path = osp.join(target_img_dir, osp.basename(img).replace("_0000.nii.gz", ".nii.gz"))
            target_gt_path = osp.join(target_gt_dir, osp.basename(gt).replace("_0000.nii.gz", ".nii.gz"))

            gt_img = nib.load(gt)
            spacing = tuple(gt_img.header['pixdim'][1:4])
            spacing_voxel = spacing[0] * spacing[1] * spacing[2]
            gt_arr = gt_img.get_fdata()
            gt_arr[gt_arr != idx] = 0
            gt_arr[gt_arr != 0] = 1
            volume = gt_arr.sum() * spacing_voxel
            if (volume < 10):
                print("skip", target_img_path)
                continue

            reference_image = tio.ScalarImage(img)
            if (meta_info['name'] == "kits23" and idx == 1):
                resample_nii(gt, target_gt_path, n=[1, 2, 3], reference_image=reference_image, mode="nearest")
            else:
                resample_nii(gt, target_gt_path, n=idx, reference_image=reference_image, mode="nearest")
            shutil.copy(img, target_img_path)