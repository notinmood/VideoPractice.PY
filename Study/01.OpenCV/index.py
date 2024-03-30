"""
 * @file   : index.py
 * @time   : 16:22
 * @date   : 2024/3/18
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
import os.path
from os import PathLike

import cv2
from BasicLibrary.data.stringHelper import StringHelper
from BasicLibrary.io.fileHelper import FileHelper


def capture_image(video_file_full_name: str | PathLike, *capturing_frame_indexes: int):
    """
    截取视频的帧
    :param capturing_frame_indexes: 要截图的帧的索引，从0开始计数
    :param video_file_full_name: 视频文件全路径
    :return:
    """
    if not capturing_frame_indexes:
        capturing_frame_indexes = (0,)
    pass

    # 读取视频
    cap = cv2.VideoCapture(video_file_full_name)
    # 获取视频总帧数
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    video_file_base_name_no_extension = FileHelper.get_base_name_no_extension(video_file_full_name)
    # video_file_extension_name = FileHelper.get_extension_name(video_file_full_name)

    flag = 0

    if not cap.isOpened():
        return
    pass

    for capturing_frame_index in capturing_frame_indexes:
        if capturing_frame_index >= frame_count:
            return
        pass

        cap.set(cv2.CAP_PROP_POS_MSEC, flag)
        cap.set(cv2.CAP_PROP_POS_FRAMES, capturing_frame_index)
        ret, image_content = cap.read()
        cv2.waitKey(2000)

        capturing_frame_index_fixed = StringHelper.add_padding(capturing_frame_index, 3)
        image_file_full_path = os.path.join(os.path.dirname(video_file_full_name),
                                            f"{video_file_base_name_no_extension}.F{capturing_frame_index_fixed}.Capture.jpg")

        ## 直接使用imwrite的时候，如果图片的导出路径有中文会出现乱码
        # cv2.imwrite(image_file_full_path, image_content)

        # 使用imencode编码后保存，可以解决中文乱码问题
        cv2.imencode('.jpg', image_content)[1].tofile(image_file_full_path)
    pass

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 视频地址
    file_name = r"Z:\mm\1_跟着央视练文笔，坚持每日写作提升练习.mp4"

    capture_image(file_name, 23, 33)
