"""
 * @file   : index.py
 * @time   : 16:09
 * @date   : 2024/3/23
 * @mail   : 9727005@qq.com
 * @creator: ShanDong Xiedali
 * @company: HiLand & RainyTop
"""
from JianYingDraft.core.draft import Draft

if __name__ == '__main__':
    draft = Draft()
    m1 = r"Z:\mm\人民日报金句摘抄｜20240215｜关于.mov"
    draft.add_media(m1)
    draft.save()
