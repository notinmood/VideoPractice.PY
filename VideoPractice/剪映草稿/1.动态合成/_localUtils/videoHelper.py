"""
 * @file   : videoHelper.py
 * @time   : 10:41
 * @date   : 2024/4/4
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
import os
import random

from BasicLibrary.io.dirHelper import DirHelper
from JianYingDraft.core.draft import Draft
from pymediainfo import MediaInfo


class VideoHelper(object):
    @classmethod
    def generate_video(cls, file_or_dir_full_path: str, draft_name="", **kwargs):
        duration_every_image = kwargs.get("durationEveryImage", 4_000_000)
        exclude_file_end_names = kwargs.get("excludeFileEndNames", ())
        include_file_end_names = kwargs.get("includeFileEndNames", ".jpg,.png,.bmp,.jpeg,.gif,.webp")

        if not draft_name:
            draft_name = os.path.basename(file_or_dir_full_path)
        pass

        draft = Draft(draft_name)

        dir_full_path = ""
        file_full_name= ""
        if os.path.isdir(file_or_dir_full_path):
            dir_full_path = file_or_dir_full_path
        pass

        if os.path.isfile(file_or_dir_full_path):
            file_full_name = file_or_dir_full_path
        pass

        if dir_full_path:
            image_file_full_names = DirHelper.get_files(dir_full_path, extension_names=include_file_end_names)
            for image_file_full_name in image_file_full_names:
                if image_file_full_name.endswith(exclude_file_end_names):
                    continue
                pass

                draft.add_media(image_file_full_name, duration=duration_every_image)
            pass
        pass

        if file_full_name:
            draft.add_media(file_full_name, duration=duration_every_image)
        pass

        draft_duration = draft.calc_draft_duration()
        audio_file_full_name = cls.get_audio_file_full_name(draft_duration)
        if audio_file_full_name:
            draft.add_media(audio_file_full_name)
        pass

        draft.save()

    @staticmethod
    def get_audio_file_full_name(min_duration: int):
        audio_dir_full_name = r"Z:\BD素材同步\BillFish素材库\SP.视频创作中心\BGM.背景音乐"
        audio_file_list = DirHelper.get_files(audio_dir_full_name, True, ".mp3,.wav")
        audio_count = len(audio_file_list)
        # 因为是在所有的音频中随机找一条，验证是否符合标准，如果不符合标准，则继续找，最多找2倍音频数的次数
        # 如果这样还找不到，那基本就没有这样符合条件的音频了
        compare_count = audio_count * 2

        try_count = 0
        while True:
            rand_number = random.randint(0, audio_count - 1)

            audio_file_full_name = audio_file_list[rand_number]
            media_info = MediaInfo.parse(audio_file_full_name).to_data()["tracks"][1]

            audio_duration = 0
            if "duration" in media_info:
                audio_duration = media_info['duration'] * 1000
            pass

            if audio_duration >= min_duration:
                return audio_file_full_name
            pass

            try_count += 1

            if try_count >= compare_count:
                return None
            pass


pass
