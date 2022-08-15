from pathlib import Path

from typing import List, Union


def get_file_list(text: Union[str, list], only_exists=True) -> List[Path]:
    res_list = []
    file_flag1 = 'file:///'
    file_flag2 = 'file://'
    file_flag3 = 'file:/'
    if isinstance(text, list):
        files = text
    elif file_flag1 in text:
        files = text.replace(file_flag1, '').split('\n')
    elif file_flag2 in text:
        files = text.replace(file_flag2, '').split('\n')
    elif file_flag3 in text:
        files = text.replace(file_flag3, '').split('\n')
    else:
        files = text.split('\n')
    for file in files:
        p_file = Path(file)
        if not file:
            continue
        if only_exists and not p_file.exists():
            continue
        res_list.append(p_file)
    
    return res_list


def get_all_file_list(text: Union[str, list], only_exists=True, need_suffix=None) -> List[Path]:
    """
    need_suffix
    """
    res_list = []
    
    if not text:
        return res_list
    if need_suffix and not isinstance(need_suffix, list):
        need_suffix = [need_suffix]
    
    file_list = get_file_list(text)
    
    for file in file_list:
        if only_exists and not file.exists():
            continue
        if file.is_file():
            if need_suffix and (file.suffix not in need_suffix and file.suffix.replace('.', '') not in need_suffix):
                continue
            res_list.append(file)
        elif file.is_dir():
            child_file_list = list(file.iterdir())
            
            files = get_all_file_list(child_file_list, only_exists=only_exists, need_suffix=need_suffix)
            if files:
                res_list.extend(files)
    
    return res_list


def get_all_dir_list():
    pass


if __name__ == '__main__':
    """
    Main run
    """
    # a = get_file_list()
    b = r'F:\downloads_file\weixin_work\WXWork\1688850050072449\Cache\File\2022-05\压铸项目ERP'
    a = get_all_file_list(b, need_suffix='.xlsx')
    print(a)
    # file = r'F:\downloads_file\weixin_work\WXWork\1688850050072449\Cache\File\2022-05\压铸项目ERP'
    # # file = r'F:\downloads_file\weixin_work\WXWork\1688850050072449\Cache\File\2022-05\压铸项目ERP\abc'
    # print(Path(file).stat().st_size)
    # print(list(Path(file).iterdir()))
    # file = r'F:\downloads_file\weixin_work\WXWork\1688850050072449\Cache\File\2022-05\压铸项目ERP\abc'
    # print(Path(file).stat().st_size)
    # print(list(Path(file).iterdir()))
    # file = r"F:\downloads_file\weixin_work\WXWork\1688850050072449\Cache\File\2022-05\压铸项目ERP\压铸项目ERP\20220125 CAMEL Quotation for Emerson project_D649.21.xlsx"
    # print(Path(file).stat().st_size)
    # print(list(Path(file).iterdir()))
