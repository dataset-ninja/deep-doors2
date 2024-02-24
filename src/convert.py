import glob
import os
import shutil
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
import supervisely as sly
from cv2 import connectedComponents
from dataset_tools.convert import unpack_if_archive
from supervisely.io.fs import file_exists, get_file_name, get_file_name_with_ext
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path


def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    ### Function should read local dataset and upload it to Supervisely project, then return project info.###
    dataset_path = "/home/alex/DATASETS/TODO/DeepDoors2/Door Classification-20240224T090110Z-001/Door Classification/RGB"
    im_folder = "img"
    mask_folder = "mask"
    batch_size = 30
    group_tag_name = "im_id"

    masks_path = "/home/alex/DATASETS/TODO/DeepDoors2/Door Detection_Segmentation-20240224T084558Z-001/Door Detection_Segmentation/Annotations"

    def get_unique_colors(img):
        unique_colors = []
        img = img.astype(np.int32)
        h, w = img.shape[:2]
        colhash = img[:, :, 0] * 256 * 256 + img[:, :, 1] * 256 + img[:, :, 2]
        unq, unq_inv, unq_cnt = np.unique(colhash, return_inverse=True, return_counts=True)
        indxs = np.split(np.argsort(unq_inv), np.cumsum(unq_cnt[:-1]))
        col2indx = {unq[i]: indxs[i][0] for i in range(len(unq))}
        for col, indx in col2indx.items():
            if col != 0:
                unique_colors.append((col // (256**2), (col // 256) % 256, col % 256))

        return unique_colors

    def create_ann(image_path):
        labels = []
        tags = []

        group_id = sly.Tag(group_tag_meta, value=int(get_file_name(image_path)[4:]))
        tags.append(group_id)

        class_value = image_path.split("/")[-2]
        class_tag = sly.Tag(name_to_test[class_value])
        tags.append(class_tag)

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 640  # image_np.shape[0]
        img_wight = 480  # image_np.shape[1]

        mask_path = os.path.join(masks_path, get_file_name_with_ext(image_path))

        if file_exists(mask_path):
            # mask_np = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            mask_np = sly.imaging.image.read(mask_path)  # [:, :, 0]
            unique_colors = get_unique_colors(mask_np)
            for color in unique_colors:
                mask = np.all(mask_np == color, axis=2)
                bitmap = sly.Bitmap(data=mask)
                label = sly.Label(bitmap, boulder)
                labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels, img_tags=tags)

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)

    boulder = sly.ObjClass("door", sly.Bitmap)

    open_meta = sly.TagMeta("open", sly.TagValueType.NONE)
    close_meta = sly.TagMeta("close", sly.TagValueType.NONE)
    semi_meta = sly.TagMeta("semi-open", sly.TagValueType.NONE)

    name_to_test = {"Open": open_meta, "Closed": close_meta, "Semi": semi_meta}

    group_tag_meta = sly.TagMeta(group_tag_name, sly.TagValueType.ANY_NUMBER)

    meta = sly.ProjectMeta(
        obj_classes=[boulder],
        tag_metas=[group_tag_meta, open_meta, close_meta, semi_meta],
    )
    api.project.update_meta(project.id, meta.to_json())
    api.project.images_grouping(id=project.id, enable=True, tag_name=group_tag_name)

    for ds_name in os.listdir(dataset_path):
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        curr_im_path = os.path.join(dataset_path, ds_name)
        images_pathes = glob.glob(curr_im_path + "/*/*.png")
        real_images_pathes = []
        for im_path in images_pathes:
            if "(" not in im_path:
                real_images_pathes.append(im_path)

        progress = sly.Progress("Create dataset {}".format(ds_name), len(real_images_pathes))

        for img_pathes_batch in sly.batched(real_images_pathes, batch_size=batch_size):
            images_pathes_batch = []
            images_names_batch = []
            for im_path in img_pathes_batch:
                images_names_batch.append(get_file_name_with_ext(im_path))
                images_pathes_batch.append(im_path)

                images_names_batch.append("depth_" + get_file_name_with_ext(im_path))
                depth_path = im_path.replace("RGB", "Depth")
                images_pathes_batch.append(depth_path)

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = []
            for i in range(0, len(images_pathes_batch), 2):
                ann = create_ann(images_pathes_batch[i])
                anns.extend([ann, ann])
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
