"""
 * @file   : 90.移动草稿和视频回到分发目录.py
 * @time   : 18:21
 * @date   : 2024/4/1
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
import os.path

from BasicLibrary.data.dateTimeHelper import DateTimeHelper
from BasicLibrary.data.dateTimePlaceHolderHelper import DateTimePlaceHolderHelper
from BasicLibrary.io.dirHelper import DirHelper
from BasicLibrary.io.fileHelper import FileHelper
from BasicLibrary.model.returnResult import ReturnResult


def deal_detail_dir(dealing_dir_full_name, dealing_date_string, *args, **kwargs) -> ReturnResult:
    _args = args
    _kwargs = kwargs

    # 1. 将草稿文件夹移动到分发目录
    jianying_draft_dir = os.path.join(jianying_draft_root, dealing_date_string)
    if DirHelper.is_dir(jianying_draft_dir):
        dest_draft_dir = os.path.join(dealing_dir_full_name, dealing_date_string)
        DirHelper.move(jianying_draft_dir, dest_draft_dir)
    pass

    # 2. 将生成的视频文件移动到分发目录
    jianying_video_full_name = os.path.join(jianying_out_path, f"{dealing_date_string}.mp4")
    if FileHelper.is_file(jianying_video_full_name):
        FileHelper.move(jianying_video_full_name, dealing_dir_full_name)
    pass

    return ReturnResult.Ok(f"✅【{dealing_date_string}】 处理完成 - {DateTimeHelper.get_string()}")


if __name__ == '__main__':
    # 指定待处理文件夹的开始日期和结束日期，处理这两个日期之间的所有文件夹
    start_date_string = '20240401'
    end_date_string = '20240430'

    #  指定待处理的文件目录
    # target_dir_parent = r'Z:\BD素材同步\BillFish素材库\RMRB.人民日报\00.Published\{dir_ym}\视频.M3\{dir_ymd}'
    target_dir_parent = r'Z:\BD素材同步\BillFish素材库\RMRB.人民日报\00.Published\{dir_ym}\视频.V3\{dir_ymd}'
    # target_dir_parent = r'Z:\mm'

    jianying_draft_root = r"Z:\jianying\Data\JianyingPro Drafts"
    jianying_out_path = r"Z:\jianying\out"

    # 给处理函数{deal_detail_dir_func}，传递各种必要的信息
    kwargs_for_deal_func = {'some_thing': 'some_thing_value'}

    DateTimePlaceHolderHelper.loop_dirs_with_date(
        start_date_string=start_date_string,
        end_date_string=end_date_string,
        target_dir_with_placeholder=target_dir_parent,
        deal_detail_dir_func=deal_detail_dir,
        **kwargs_for_deal_func
    )
