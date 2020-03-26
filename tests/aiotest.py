import os
import sys
import logging
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import crawler.helperz as helperz


logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    logging.debug("ssss")

    value = json.dumps(
        {
            "task": ["hello", "world"],
            "content_type": "xxxx",
            "content": str(b'xxssss', encoding='utf-8'),
        }
    )

    print(value)
