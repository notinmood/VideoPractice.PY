"""
 * @file   : 01.扫描目录.py
 * @time   : 20:54
 * @date   : 2024/3/30
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""

from BasicLibrary.data.dateTimeHelper import DateTimeHelper
from BasicLibrary.data.dateTimePlaceHolderHelper import DateTimePlaceHolderHelper
from BasicLibrary.model.returnResult import ReturnResult

from _localUtils.videoHelper import VideoHelper


def deal_detail_dir(dealing_dir_full_name, dealing_date_string, *args, **kwargs) -> ReturnResult:
    _args = args

    # 获取从调用方传递过来的各种参数
    _some_thing = kwargs.get('some_thing', '')

    draft_name = dealing_date_string

    VideoHelper.generate_video(dealing_dir_full_name, draft_name, **kwargs)

    return ReturnResult.Ok(f"✅【{dealing_date_string}】 处理完成 - {DateTimeHelper.get_string()}")


if __name__ == '__main__':
    # 指定待处理文件夹的开始日期和结束日期，处理这两个日期之间的所有文件夹
    start_date_string = '20240401'
    end_date_string = '20240430'

    #  指定待处理的文件目录
    # target_dir_parent = r'Z:\BD素材同步\BillFish素材库\RMRB.人民日报\00.Published\{dir_ym}\微信.D.辞文之美.D1\{dir_ymd}'
    target_dir_parent = r'Z:\BD素材同步\BillFish素材库\RMRB.人民日报\00.Published\{dir_ym}\视频.M3\{dir_ymd}'
    # target_dir_parent = r'Z:\mm'

    # 给处理函数{deal_detail_dir_func}，传递各种必要的信息
    kwargs_for_deal_func = {
        "some_thing": "some_thing_value",
        "durationFirstMedia": 1_000_000,  # 第一幅图片播放的时长
        "durationEveryMedia": 4_000_000,  # 每幅图片播放的时长
        "transitionName": "[[random]]",  # 视频片段的转场效果之转场名称
        # "excludeFileEndNames": ("00.cover.jpg",),  # 不参与视频生成的文件后缀名
    }

    DateTimePlaceHolderHelper.loop_dirs_with_date(
        start_date_string=start_date_string,
        end_date_string=end_date_string,
        target_dir_with_placeholder=target_dir_parent,
        deal_detail_dir_func=deal_detail_dir,
        **kwargs_for_deal_func
    )
pass
