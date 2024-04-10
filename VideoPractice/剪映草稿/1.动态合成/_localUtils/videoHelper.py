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
from JianYingDraft.utils.innerBizTypes import transitionDict
from JianYingDraft.utils import tools
from pymediainfo import MediaInfo


class VideoHelper(object):
    @classmethod
    def generate_video(cls, file_or_dir_full_path: str, draft_name="", **kwargs):
        duration_every_media = kwargs.get("durationEveryMedia", 0)
        duration_first_media = kwargs.get("durationFirstMedia", 0)

        if not duration_first_media:
            duration_first_media = duration_every_media
        pass

        bgm_mute = kwargs.get("bgmMute", False)
        exclude_file_end_names = kwargs.get("excludeFileEndNames", ())
        include_file_end_names = kwargs.get("includeFileEndNames", ".jpg,.png,.bmp,.jpeg,.gif,.webp")

        bgm_fade_out_duration = kwargs.get("bgmFadeOutDuration", 1_000_000)
        transition_name = kwargs.get("transitionName", "")
        transition_duration = kwargs.get("transitionDuration", 1_000_000)
        transition_data = cls.generate_transition(transition_name, transition_duration)

        if not draft_name:
            draft_name = os.path.basename(file_or_dir_full_path)
        pass

        draft = Draft(draft_name)

        dir_full_path = ""
        file_full_name = ""
        if os.path.isdir(file_or_dir_full_path):
            dir_full_path = file_or_dir_full_path
        pass

        if os.path.isfile(file_or_dir_full_path):
            file_full_name = file_or_dir_full_path
        pass

        # 1. 处理目录下的多个图片
        if dir_full_path:
            image_file_full_names = DirHelper.get_files(dir_full_path, extension_names=include_file_end_names)
            image_index = 0
            for image_file_full_name in image_file_full_names:
                if image_file_full_name.endswith(exclude_file_end_names):
                    continue
                pass

                if image_index == 0:
                    _duration = duration_first_media
                else:
                    _duration = duration_every_media
                pass

                image_index += 1
                draft.add_media(image_file_full_name, duration=_duration, bgm_mute=bgm_mute,
                                transition_data=transition_data)
            pass
        pass

        # 2. 处理单个文件
        if file_full_name:
            draft.add_media(file_full_name, duration=duration_every_media, bgm_mute=bgm_mute,
                            transition_data=transition_data)
        pass

        # 3. 添加背景音乐
        draft_duration = draft.calc_draft_duration()
        audio_file_full_name = cls.get_audio_file_full_name(draft_duration)
        if audio_file_full_name:
            draft.add_media(audio_file_full_name, fade_out_duration=bgm_fade_out_duration)
        pass

        draft.save()

    @staticmethod
    def get_audio_file_full_name(min_duration: int):
        audio_dir_full_name = r"Z:\BD素材同步\BillFish素材库\SP.视频创作中心\BGM.背景音乐"
        audio_file_list = DirHelper.get_files(audio_dir_full_name, ".mp3,.wav", True)
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

    @staticmethod
    def get_random_transition_name():
        count = len(transitionDict)
        rand_number = random.randint(0, count - 1)
        return list(transitionDict.keys())[rand_number]

    @classmethod
    def generate_transition(cls, transition_name: str, duration: int = 1_000_000):
        if not transition_name:
            return None
        pass

        if transition_name == "[[random]]":
            transition_name = cls.get_random_transition_name()
        pass

        if transition_name not in transitionDict:
            return None
        pass

        transition_data = tools.generate_transition_data(transition_name, duration)
        return transition_data


pass
