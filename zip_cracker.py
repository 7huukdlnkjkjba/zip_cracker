import zipfile
import itertools
import time
from threading import Thread


def extract_zip(zip_file, password):
    try:
        zip_file.extractall(pwd=password.encode())
        print(f"\n[+] 密码破解成功: {password}")
        return True
    except (RuntimeError, zipfile.BadZipFile):
        return False
    except Exception as e:
        return False


def dictionary_attack(zip_path, dict_path):
    zip_file = zipfile.ZipFile(zip_path)
    with open(dict_path, 'r', encoding='utf-8', errors='ignore') as f:
        for password in f.readlines():
            password = password.strip()
            if extract_zip(zip_file, password):
                return True
    return False


def brute_force_attack(zip_path, min_len=4, max_len=6, chars=None):
    if chars is None:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789'

    zip_file = zipfile.ZipFile(zip_path)
    for length in range(min_len, max_len + 1):
        for attempt in itertools.product(chars, repeat=length):
            password = ''.join(attempt)
            if extract_zip(zip_file, password):
                return True
    return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="ZIP密码破解工具")
    parser.add_argument("zipfile", help="目标ZIP文件路径")
    parser.add_argument("-d", "--dict", help="使用字典攻击模式（字典文件路径）")
    parser.add_argument("-b", "--brute", action="store_true",
                        help="使用暴力破解模式（默认4-6位小写字母+数字）")
    parser.add_argument("-min", type=int, default=4, help="最小密码长度")
    parser.add_argument("-max", type=int, default=6, help="最大密码长度")
    parser.add_argument("-c", "--charset",
                        default='abcdefghijklmnopqrstuvwxyz0123456789',
                        help="自定义字符集")

    args = parser.parse_args()

    start_time = time.time()

    if args.dict:
        print("[*] 正在使用字典攻击...")
        if dictionary_attack(args.zipfile, args.dict):
            print("[*] 攻击成功！")
        else:
            print("[-] 字典攻击失败")

    elif args.brute:
        print("[*] 正在使用暴力破解...")
        print(f"[*] 字符集: {args.charset}")
        print(f"[*] 密码长度范围: {args.min}-{args.max}")
        if brute_force_attack(args.zipfile, args.min, args.max, args.charset):
            print("[*] 攻击成功！")
        else:
            print("[-] 暴力破解失败")

    else:
        print("[-] 请选择攻击模式（-d 或 -b）")

    print(f"[*] 耗时: {time.time() - start_time:.2f}秒")