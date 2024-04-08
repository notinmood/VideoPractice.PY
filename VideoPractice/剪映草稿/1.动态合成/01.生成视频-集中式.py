"""
 * @file   : 01.扫描目录.py
 * @time   : 20:54
 * @date   : 2024/3/30
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
import os

from BasicLibrary.io.dirHelper import DirHelper

from _localUtils.videoHelper import VideoHelper


def deal_cluster_dir(cluster_dir_full_name=""):
    """
    处理集群路径下生成视频的逻辑
    （即要创建视频的图片，都分门别类放在某个父文件夹下，这个父文件夹就是集群路径）
    :return:
    """
    if not cluster_dir_full_name:
        cluster_dir_full_name = r"Z:\BD素材同步\BillFish素材库\SP.视频创作中心\图片素材"
    pass

    # 给处理函数{deal_detail_dir_func}，传递各种必要的信息
    kwargs_for_deal_func = {
        "some_thing": "some_thing_value",
        "durationEveryMedia": 4_000_000,  # 每幅图片播放的时长
        "excludeFileEndNames": ("00.Cover.jpg",),  # 不参与视频生成的文件后缀名
    }

    # 1. 获取目录下的所有图片文件，每个图片文件单独做成一个n秒钟的视频
    image_file_full_names = DirHelper.get_files(cluster_dir_full_name, include_sub_dir=False,
                                                extension_names=[".jpg", ".png"])

    for image_file_full in image_file_full_names:
        VideoHelper.generate_video(image_file_full, **kwargs_for_deal_func)
    pass

    # 2. 获取目录下子文件夹，每个子文件夹单独做成一个长视频视频（长视频为子文件夹内每个图片5秒的合成）
    sub_dir_full_names = DirHelper.get_sub_dirs(cluster_dir_full_name)
    for sub_dir_full_name in sub_dir_full_names:
        # 已经加工完成视频的目录，都转移到“.Finished”目录下，因此再次处理的时候，需要跳过此目录
        sub_dir_base_name = os.path.basename(sub_dir_full_name)
        if sub_dir_base_name.startswith("."):
            continue
        pass

        VideoHelper.generate_video(sub_dir_full_name, **kwargs_for_deal_func)
    pass


if __name__ == '__main__':
    # 1. 处理集群路径下生成视频的逻辑
    cluster_dir = r"Z:\BD素材同步\BillFish素材库\SP.视频创作中心\图片素材"
    deal_cluster_dir(cluster_dir)
pass
