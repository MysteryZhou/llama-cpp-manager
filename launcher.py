# -*- coding: utf-8 -*-
"""
llama.cpp 模型管理台 - GUI 入口（打包 EXE 用）
=================================================
- 启动内嵌 HTTP 后端（server.start_server）
- 用 pywebview 打开原生窗口内嵌页面（WebView2）
- 若 WebView2 不可用，自动回退到系统默认浏览器
"""
import os
import sys
import threading
import webbrowser

import server


def main():
    # 防止重复启动：单实例（检测端口，已在跑则只开窗口）
    import socket
    already = False
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("127.0.0.1", server.PORT_API))
        already = True
    except OSError:
        already = False
    finally:
        s.close()

    srv = None
    if not already:
        srv = server.start_server()
        if srv is None:
            already = True  # 端口被占但连不上？仍尝试打开页面

    url = "http://127.0.0.1:%d" % server.PORT_API
    window = None
    try:
        import webview
        window = webview.create_window(
            "llama.cpp 模型管理台",
            url,
            width=1200, height=820,
            min_size=(940, 620),
            background_color="#0b1220",
        )
        webview.start()
    except Exception:
        webbrowser.open(url)
        # 后端单独跑的话保持进程活着；否则窗口模式结束后关服务
        if srv is not None:
            try:
                while True:
                    threading.Event().wait(3600)
            except KeyboardInterrupt:
                pass

    if srv is not None:
        try:
            srv.shutdown()
        except Exception:
            pass


if __name__ == "__main__":
    main()
