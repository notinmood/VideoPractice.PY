"""
 * @file   : 1.生成图片转视频的草稿.py
 * @time   : 11:36
 * @date   : 2024/3/6
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
import os.path
import shutil

from BasicLibrary.data.dateTimeHelper import DateTimeHelper
from BasicLibrary.io.dirHelper import DirHelper
from BasicLibrary.io.fileHelper import FileHelper


def replace_content(file_content: str, *args, **kwargs) -> str:
    _args = args

    new_image_full_name = kwargs.get("new_image_full_name")
    new_image_full_name = new_image_full_name.replace("\\", "/")
    new_image_base_name = FileHelper.get_base_name(new_image_full_name)
    new_image_base_name_no_extension = FileHelper.get_base_name_no_extension(new_image_full_name)

    old_image_full_name = r"Z:/MyImages/RMRB.人民日报.素材/99.处理完成的素材/AC25/2023-12-07 13-36-10_今日诗词“且以喜乐 且以永日”-2.webp"
    old_image_base_name = "2023-12-07 13-36-10_今日诗词“且以喜乐 且以永日”-2.webp"
    old_draft_name = "MUBAN"

    file_content = file_content.replace(old_image_full_name, new_image_full_name)
    file_content = file_content.replace(old_image_base_name, new_image_base_name)
    file_content = file_content.replace(old_draft_name, new_image_base_name_no_extension)

    return file_content


pass


def modify_draft_file(dest_draft_dir_full_name: str, target_file_base_name: str, **kwargs_for_func):
    target_file_full_name = os.path.join(dest_draft_dir_full_name, target_file_base_name)
    FileHelper.modify(target_file_full_name, replace_content, **kwargs_for_func)


def convert_image_to_movie(image_full_name: str):
    image_base_name = FileHelper.get_base_name(image_full_name)
    image_base_name_no_extension = FileHelper.get_base_name_no_extension(image_base_name)

    source_draft_dir_full_name = r"Z:\jianying\Data\JianyingPro Drafts\.MUBAN"
    dest_draft_dir_full_name = os.path.join(r"Z:\jianying\Data\JianyingPro Drafts", image_base_name_no_extension)
    # 0.创建新的草稿目录
    if not DirHelper.is_dir(dest_draft_dir_full_name):
        shutil.copytree(source_draft_dir_full_name, dest_draft_dir_full_name)
    pass

    kwargs_for_func = {
        "new_image_full_name": image_full_name,
    }

    # 1.修改草稿内容
    modify_draft_file(dest_draft_dir_full_name, "draft_content.json", **kwargs_for_func)
    modify_draft_file(dest_draft_dir_full_name, "draft_meta_info.json", **kwargs_for_func)

    print(f"✅{image_base_name} 草稿生成完成 - ({DateTimeHelper.get_string()})")


if __name__ == '__main__':
    target_dir = r"Z:\MyImages\RMRB.人民日报.素材\00.OK.V1\01"
    # target_dir = r"Z:\mm"

    image_list = DirHelper.get_files(target_dir, ".jpg,.jpeg,.png,.webp", True)
    for _item in image_list:
        convert_image_to_movie(_item)
    pass
