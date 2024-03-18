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
from BasicLibrary.projectHelper import ProjectHelper


def replace_content(file_content: str, *args, **kwargs) -> str:
    _args = args

    new_image_full_name = kwargs.get("new_image_full_name")
    new_image_full_name = new_image_full_name.replace("\\", "/")
    new_image_base_name = FileHelper.get_base_name(new_image_full_name)
    new_image_base_name_no_extension = FileHelper.get_base_name_no_extension(new_image_full_name)

    old_image_base_name = FileHelper.get_base_name(old_image_full_name)

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

    dest_draft_dir_full_name = os.path.join(draft_root_dir_full_name, image_base_name_no_extension)
    # 0.创建新的草稿目录
    if not DirHelper.is_dir(dest_draft_dir_full_name):
        shutil.copytree(draft_template_dir_full_name, dest_draft_dir_full_name)
    pass

    kwargs_for_func = {
        "new_image_full_name": image_full_name,
    }

    # 1.修改草稿内容
    modify_draft_file(dest_draft_dir_full_name, "draft_content.json", **kwargs_for_func)
    modify_draft_file(dest_draft_dir_full_name, "draft_meta_info.json", **kwargs_for_func)

    print(f"✅{image_base_name} 草稿生成完成 - ({DateTimeHelper.get_string()})")


def get_setting_every_poem():
    _draft_template_dir_full_name = os.path.join(root_path, r"剪映/0.模板替换/_res/.MUBAN-meiriyiju")
    _old_image_full_name = r"Z:/mm/每天坚持背一句｜20240302：.jpg"
    _old_draft_name = ".MUBAN-meiriyiju"

    return {
        "draft_template_dir_full_name": _draft_template_dir_full_name,
        "old_image_full_name": _old_image_full_name,
        "old_draft_name": _old_draft_name
    }


def get_setting_fang_xie():
    _draft_template_dir_full_name = os.path.join(root_path, r"剪映/0.模板替换/_res/.MUBAN-央视仿写")
    _old_image_full_name = r"Z:/mm/2024_02_25_13_21_19_67_跟着央视练文笔_坚持每天仿写练习写作提升_1.png"
    _old_draft_name = "仿写央视"

    return {
        "draft_template_dir_full_name": _draft_template_dir_full_name,
        "old_image_full_name": _old_image_full_name,
        "old_draft_name": _old_draft_name
    }


def get_setting_old_style():
    _draft_template_dir_full_name = os.path.join(root_path, r"剪映/0.模板替换/_res/.MUBAN-m1-B")
    _old_image_full_name = r"Z:/mm/1_每天坚持打卡_一个_后惊艳所有人_[00_00_02][20240314-160441].png"
    _old_draft_name = "MUBAN-M1"

    return {
        "draft_template_dir_full_name": _draft_template_dir_full_name,
        "old_image_full_name": _old_image_full_name,
        "old_draft_name": _old_draft_name
    }


if __name__ == '__main__':
    root_path = ProjectHelper.get_root_physical_path()
    draft_root_dir_full_name = r"Z:\jianying\Data\JianyingPro Drafts"

    # target_dir = r"Z:\MyImages\RMRB.人民日报.素材\00.OK.V1\01"
    target_dir = r"Z:\mm"

    # 需要修改的文件名和模板名
    # settings = get_setting_every_poem()
    settings = get_setting_fang_xie()
    # settings = get_setting_old_style()

    draft_template_dir_full_name = settings["draft_template_dir_full_name"]
    old_image_full_name = settings["old_image_full_name"]
    old_draft_name = settings["old_draft_name"]

    image_list = DirHelper.get_files(target_dir, True, ".jpg,.jpeg,.png,.webp")
    for image_file_full_name in image_list:
        convert_image_to_movie(image_file_full_name)
    pass
