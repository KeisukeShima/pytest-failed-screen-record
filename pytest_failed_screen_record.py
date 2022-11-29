import time
import uuid
import pytest
from pathlib import Path
import pyautogui
import cv2
import numpy as np
from multiprocessing import Manager, Process, Event


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

    group.addoption("--record-fps",
                    default=1.0,
                    type=float,
                    help="Specifies the frame rate of the recording. Default is 1.0. Limitations depend on the processing power of the computer.")


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(early_config, parser, args):
    options = early_config.known_args_namespace
    plugin = RecordPlugin(options, early_config.pluginmanager)
    early_config.pluginmanager.register(plugin, '_record')


class RecordPlugin:
    def __init__(self, options, pluginmanager):
        self.options = options
        self.fps = options.record_fps


    def pytest_configure(self, config):
        record_path = config.getvalue("record_path")
        switch = config.getvalue("record")
        if switch:
            record_path.mkdir(exist_ok=True, parents=True)


    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        result = outcome.get_result()
        record_path = item.config.getvalue("record_path")
        if item.config.getvalue("record"):
            if result.when == "setup":
                self.start_capture()
            elif result.when == "call" and result.failed:
                self.stop_capture()
                self.save_capture(record_path)
            elif result.when == "call" and result.passed:
                self.stop_capture()


    def save_capture(self, save_dir):
        fourcc = cv2.VideoWriter_fourcc(*"MP4V")
        writer = cv2.VideoWriter(
            str(save_dir / ('capture' + str(uuid.uuid4()).replace("-", "")[:8] + '.mp4')),
            fourcc,
            self.fps,
            (self.img_width, self.img_height),
        )
        # キャプチャー画像を読み出して出力動画ファイルに追記
        for img in self.capture_list:
            writer.write(img)
        writer.release()


    def start_capture(self):
        # ウィンドウサイズを取得するため、一度Captureする
        capture = pyautogui.screenshot()
        image_array = np.asarray(capture)
        self.img_height, self.img_width, self.channels = image_array.shape

        # Start Process
        self.manager = Manager()
        self.capture_list = self.manager.list()
        self.stop_flag = Event()
        self.process = Process(
            target=capture_func,
            kwargs={
                "capture_list": self.capture_list,
                "stop_flag": self.stop_flag,
                "fps": self.fps,
            }
        )
        self.process.start()


    def stop_capture(self):
        self.stop_flag.set()
        self.process.join()


def capture_func(capture_list, stop_flag, fps):
    interval = 1.0 / fps
    while True:
        loop_start_time = time.time()
        if stop_flag.is_set():
            break
        capture = pyautogui.screenshot()
        image = cv2.cvtColor(np.asarray(capture), cv2.COLOR_RGB2BGR)
        capture_list.append(image)

        time_diff = time.time() - loop_start_time
        if time_diff < interval:
            time.sleep(interval - time_diff)
