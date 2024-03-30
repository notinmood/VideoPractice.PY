"""
 * @file   : 01.视频截图.py
 * @time   : 9:04
 * @date   : 2024/3/19
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
import os.path
from os import PathLike

import cv2
from BasicLibrary.data.dateTimeHelper import DateTimeHelper
from BasicLibrary.data.stringHelper import StringHelper
from BasicLibrary.io.dirHelper import DirHelper
from BasicLibrary.io.fileHelper import FileHelper


def capture_image(input_video_file_full_name: str | PathLike,
                  output_image_dir_full_name: str | PathLike = "",
                  *capturing_frame_indexes: int):
    """
    截取视频的帧
    :param output_image_dir_full_name:
    :param capturing_frame_indexes: 要截图的帧的索引，从0开始计数
    :param input_video_file_full_name: 视频文件全路径
    :return:
    """
    if not capturing_frame_indexes:
        capturing_frame_indexes = (0,)
    pass

    # 读取视频
    cap = cv2.VideoCapture(input_video_file_full_name)
    # 获取视频总帧数
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    video_file_base_name_no_extension = FileHelper.get_base_name_no_extension(input_video_file_full_name)
    # video_file_extension_name = FileHelper.get_extension_name(video_file_full_name)

    if not output_image_dir_full_name:
        output_image_dir_full_name = os.path.dirname(input_video_file_full_name)
    pass

    if not DirHelper.is_exist(output_image_dir_full_name):
        DirHelper.make(output_image_dir_full_name)
    pass

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

        capturing_frame_index_fixed = StringHelper.add_padding(capturing_frame_index, 2)
        image_file_full_path = os.path.join(output_image_dir_full_name,
                                            f"{video_file_base_name_no_extension}_F{capturing_frame_index_fixed}.Capture.jpg"
                                            )

        ## 直接使用imwrite的时候，如果图片的导出路径有中文会出现乱码
        # cv2.imwrite(image_file_full_path, image_content)

        # 使用imencode编码后保存，可以解决中文乱码问题
        cv2.imencode('.jpg', image_content)[1].tofile(image_file_full_path)
    pass

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # 设置要转换视频所在的目录
    video_dir_full_name = r"Z:\MyImages\RMRB.人民日报.素材\00.OK.V2\00.doing\央视"

    file_list = DirHelper.get_files(video_dir_full_name, extension_names=".mp4;.mov")
    for _item in file_list:
        capture_image(_item)
        print(f"✅视频{FileHelper.get_base_name(_item)}处理完成 - {DateTimeHelper.get_string()}")
    pass
    print(f"✅✅目录 - {video_dir_full_name} 全部处理完成")

    # file_name = r"Z:\mm\1_跟着央视练文笔，坚持每日写作提升练习.mp4"
    # capture_image(file_name)
