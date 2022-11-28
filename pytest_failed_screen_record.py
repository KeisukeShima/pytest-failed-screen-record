import os
import time
import uuid
import pytest
from pathlib import Path


def pytest_addoption(parser):
    group = parser.getgroup("failed-screen-record", "record of test case failure")
    group.addoption("--record",
                    action="store_true",
                    help="Record if the test case failed.")

    group.addoption("--record-path",
                    default=Path.cwd() / "record",
                    type=Path,
                    help="It will be save in the 'record' directory of current directory. "
                        "If this parameter is set, it will be save in the specified path.")


def pytest_configure(config):
    record_path = config.getvalue("record_path")
    switch = config.getvalue("record")
    if switch:
        record_path.mkdir(exist_ok=True, parents=True)
        # archive_file(record)


record_path_with_stamp = ""
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    print("debug1")
    outcome = yield
    result = outcome.get_result()
    print("debug2: " + result.when)
    if item.config.getvalue("record"):
        global record_path_with_stamp
        if result.when == "setup":
            record_path = item.config.getvalue("record_path")
            record_path_with_stamp = record_path / time.strftime("%Y-%m-%d")
            record_path_with_stamp.mkdir(exist_ok=True)
            start_capture(record_path_with_stamp, item.name)
        elif result.when == "call" and result.failed:
            stop_capture()
            save_capture(record_path_with_stamp, item.name)
        elif result.when == "call" and result.passed:
            stop_capture()


def save_capture(filedir, page_name):
    try:
        img_path = os.path.join(filedir, page_name + "_" + str(uuid.uuid4()).replace("-", "")[:8] + ".png")
        print(f"saved screenshot: {img_path}")
        return img_path
    except (OSError, NameError) as e:
        print(e)


def start_capture(filedir, page_name):
    img_path = os.path.join(filedir, page_name + "_" + str(uuid.uuid4()).replace("-", "")[:8] + ".png")
    print(f"start capture: {img_path}")


def stop_capture():
    print(f"stop capture")


# def archive_file(filepath, pattern=r"[\w\]\[]*\.png") -> None:
#     if not os.path.exists(filepath):
#         os.makedirs(filepath)
#     else:
#         dirs_list = os.listdir(filepath)
#         for dir_name in dirs_list:
#             path = os.path.join(filepath, dir_name)
#             if not os.path.isdir(path):
#                 continue
#             dirs = ';'.join(os.listdir(path))
#             mv_dirs = re.findall(pattern, dirs)
#             if mv_dirs:
#                 history = os.path.join(filepath, "history", dir_name)
#                 if not os.path.exists(history):
#                     os.makedirs(history)
#                 times = 1
#                 while True:
#                     existing = os.path.join(history, str(times))
#                     if not os.path.exists(existing):
#                         os.makedirs(existing)
#                         break
#                     times += 1
#                 for i in mv_dirs:
#                     shutil.move(os.path.join(path, i), existing)
#                 else:
#                     try:
#                         os.removedirs(path)
#                     except OSError as e:
#                         print(f"Delete directory path:{path} error! Track:{e}")
