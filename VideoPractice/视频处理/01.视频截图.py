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
from BasicLibrary.data.dateTimePlaceHolderHelper import DateTimePlaceHolderHelper
from BasicLibrary.model.returnResult import ReturnResult


def deal_detail_dir(dealing_dir_full_name, dealing_date_string, *args, **kwargs) -> ReturnResult:
    _args = args

    include_file_end_names = kwargs.get("includeFileEndNames", (".mp4", ".mov"))
    exclude_file_end_names = kwargs.get("excludeFileEndNames", (".168x",))  # 默认是一个非常特殊的后缀名，仅仅是为了正常场景下不会出现这种情况

    file_list = DirHelper.get_files(dealing_dir_full_name, extension_names=include_file_end_names)
    for _item in file_list:
        if _item.endswith(exclude_file_end_names):
            continue
        pass

        capture_image(_item)
        print(f"->视频{FileHelper.get_base_name(_item)}处理完成 - {DateTimeHelper.get_string()}")
    pass

    return ReturnResult.Ok(f"✅【{dealing_date_string}】 处理完成 - {DateTimeHelper.get_string()}")


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
    # 指定待处理文件夹的开始日期和结束日期，处理这两个日期之间的所有文件夹
    start_date_string = '20240603'
    end_date_string = '20240708'

    #  指定待处理的文件目录
    # target_dir_parent = r'Z:\BD素材同步\BillFish素材库\RMRB.人民日报\00.Published\{dir_ym}\微信.D.辞文之美.D1\{dir_ymd}'
    target_dir_parent = r'Z:\BD素材同步\BillFish素材库\RMRB.人民日报\00.Published\{dir_ym}\视频.V1\{dir_ymd}'
    # target_dir_parent = r'Z:\mm'

    # 给处理函数{deal_detail_dir_func}，传递各种必要的信息
    kwargs_for_deal_func = {
        "some_thing": "some_thing_value",
        "includeFileEndNames": (".mp4", ".mov"),  # 参与工作的文件后缀名
        # "excludeFileEndNames": ("00.cover.mov",),  # 不参与工作的文件后缀名
    }

    DateTimePlaceHolderHelper.loop_dirs_with_date(
        start_date_string=start_date_string,
        end_date_string=end_date_string,
        target_dir_with_placeholder=target_dir_parent,
        deal_detail_dir_func=deal_detail_dir,
        **kwargs_for_deal_func
    )
