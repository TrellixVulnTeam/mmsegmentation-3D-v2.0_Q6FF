
# dataset settings
dataset_type = 'BraTS2018Dataset'
data_root = '/opt/data/private/project/charelchen.cj/workDir/dataset/whtj_lung'
crop_size = (128, 128, 128)
train_pipeline = [
    dict(type='LoadImageFromNIIFile'),
    dict(type='LoadAnnotationsFromNIIFile'),
    # dict(type='Resize', img_scale=img_scale, ratio_range=(0.5, 2.0)),
    dict(type='ExtractDataFromObj'),
    # dict(type="IgnoreBlackArea", set_label=255),
    # dict(type='RandomCropMedical', crop_size=crop_size, cat_max_ratio=0.9, ignore_index=255),
    dict(type='NormalizeMedical', norm_type='wcww', window_center=-600, window_width=1600),
    dict(type='RandomCropMedicalWithForeground', crop_size=crop_size, fore_cat_ratio=0.1),
    dict(type='ConcatImage'),
    dict(type='DefaultFormatBundle3D'),
    dict(type='Collect', keys=['img', 'gt_semantic_seg'])
]
test_pipeline = [
        dict(type='LoadImageFromNIIFile'),
        dict(type='ExtractDataFromObj'),
        dict(type='NormalizeMedical', norm_type='wcww', window_center=-600, window_width=1600),
        dict(type='ConcatImage'),
        dict(type='ToTensor', keys=['img']),
        dict(type='Collect', keys=['img'],
             extend_meta_keys=['image_id', 'img_affine_matrix'])
]

data = dict(
    samples_per_gpu=8,
    workers_per_gpu=8,
    train=dict(
        type='RepeatDataset',
        times=40000,
        dataset=dict(
            classes=("background", "lobel"),
            img_suffixes=['image.nii.gz'],
            seg_map_suffix="lobel.nii.gz",
            type=dataset_type,
            data_root=data_root,
            img_dir='stas_nifty_data_1x1x1',
            ann_dir='stas_nifty_data_1x1x1',
            split='lobel_trainlist.txt',
            pipeline=train_pipeline)),
    test=dict(
            classes=("background", "lobel"),
            img_suffixes=['image.nii.gz'],
            seg_map_suffix="lobel.nii.gz",
            type='BraTS2018Dataset',
            data_root=data_root,
            split='lobel_testlist.txt',
            img_dir='stas_nifty_data_1x1x1',
            ann_dir='stas_nifty_data_1x1x1',
            pipeline=test_pipeline),
    val=dict(
            classes=("background", "lobel"),
            img_suffixes=['image.nii.gz'],
            seg_map_suffix="lobel.nii.gz",
            type='BraTS2018Dataset',
            data_root=data_root,
            split='lobel_testlist.txt',
            img_dir='stas_nifty_data_1x1x1',
            ann_dir='stas_nifty_data_1x1x1',
            pipeline=test_pipeline),
    inference=dict(
            classes=("background", "lobel"),
            img_suffixes=['image.nii.gz'],
            seg_map_suffix="lobel.nii.gz",
            type='BraTS2018Dataset',
            data_root=data_root,
            split='lobel_total.txt',
            img_dir='stas_nifty_data_1x1x1',
            ann_dir='stas_nifty_data_1x1x1',
            pipeline=test_pipeline),
    )



# model settings
# norm_cfg = dict(type='BN3d', requires_grad=True)
# conv_cfg = dict(type='Conv3d')
# act_cfg = dict(type='RELU')
# model settings
# norm_cfg = dict(type='SyncBN', requires_grad=True)
background_as_first_channel = False
model = dict(
    type='VNetSegmentor',
    pretrained=None,
    in_channels=1,
    classes=1,
    resize_mode="trilinear",
    loss_cfg=dict(type="MedicalDiceLoss",
                  classes=1,
                  use_sigmoid=True,
                  class_weight=[1.],
                  loss_weight=1.,
                  background_as_first_channel=background_as_first_channel),
    test_cfg=dict(mode='slide', crop_size=[128, 128, 128], stride=[64, 64, 64], three_dim_input=True)
    )
eval_options = dict(background_as_first_channel=background_as_first_channel)
# optimizer
optimizer = dict(type='SGD', lr=0.01, momentum=0.9, weight_decay=0.0005)
optimizer_config = dict(type='Fp16OptimizerHook',
                        loss_scale=512.,
                        )
# learning policy
lr_config = dict(policy='poly', power=0.9, min_lr=1e-5, by_epoch=False)
# runtime settings
runner = dict(type='IterBasedRunner', max_iters=20000)
checkpoint_config = dict(by_epoch=False, interval=2000)
evaluation = dict(interval=2000)

# yapf:disable
log_config = dict(
    interval=10,
    hooks=[
        dict(type='TextLoggerHook', by_epoch=False),
        # dict(type='TensorboardLoggerHook')
    ])
# yapf:enable
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
# work_dirs =
resume_from = ''
workflow = [('train', 1)]
cudnn_benchmark = True
