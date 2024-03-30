"""
 * @file   : 01.扫描目录.py
 * @time   : 20:54
 * @date   : 2024/3/30
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
import os
import random

from BasicLibrary.io.dirHelper import DirHelper
from JianYingDraft.core.draft import Draft
from pymediainfo import MediaInfo


def gen_video(dir_full_path: str):
    dir_base_name = os.path.basename(dir_full_path)

    draft = Draft(dir_base_name)

    image_extensions = ".jpg,.png,.bmp,.jpeg,.gif,.webp"
    image_file_full_names = DirHelper.get_files(dir_full_path, extension_names=image_extensions)
    for image_file_full_name in image_file_full_names:
        draft.add_media(image_file_full_name, duration=4_000_000)
    pass

    draft_duration = draft.calc_draft_duration()
    audio_file_full_name = get_audio_file_full_name(draft_duration)
    if audio_file_full_name:
        draft.add_media(audio_file_full_name)
    pass

    draft.save()


def get_audio_file_full_name(min_duration: int):
    audio_dir_full_name = r"Z:\BD素材同步\BillFish素材库\SP.视频创作中心\BGM.背景音乐"
    audio_file_list = DirHelper.get_files(audio_dir_full_name, True, ".mp3,.wav")
    audio_count = len(audio_file_list)

    try_count = 0
    while 1 == 1:
        rand_number = random.randint(0, audio_count - 1)

        audio_file_full_name = audio_file_list[rand_number]
        media_info = MediaInfo.parse(audio_file_full_name).to_data()["tracks"][1]

        if "duration" in media_info:
            audio_duration = media_info['duration'] * 1000
        pass

        if audio_duration >= min_duration:
            return audio_file_full_name
        pass

        try_count += 1

        if try_count >= audio_count:
            return None
        pass


if __name__ == '__main__':
    target_dir = r"Z:\BD素材同步\BillFish素材库\SP.视频创作中心\图片素材"

    # 1. 获取目录下的所有图片文件，每个图片文件单独做成一个5秒钟的视频

    # 2. 获取目录下子文件夹，每个子文件夹单独做成一个长视频视频（长视频为子文件夹内每个图片5秒的合成）
    sub_dirs = DirHelper.get_sub_dirs(target_dir)
    for sub_dir in sub_dirs:
        gen_video(sub_dir)
    pass
