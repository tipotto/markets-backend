from services.analyze_service import analyze
import os
import sys
import json
import asyncio
# 絶対パスでのインポートのためにモジュール探索パスを追加
pydir_path = os.path.dirname(__file__)
if pydir_path not in sys.path:
    sys.path.append(pydir_path)


def main():
    try:
        form = json.loads(sys.stdin.readline())
        data = asyncio.run(analyze(form))

        print(json.dumps({
            'status': 'success',
            'result': data,
            'error': ''
        }, ensure_ascii=False))

    except Exception:
        raise


if __name__ == "__main__":
    main()
