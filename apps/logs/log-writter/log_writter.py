import time
import uuid
from datetime import datetime, timezone

random_string = str(uuid.uuid4())


def timestamp():
    now = datetime.now(timezone.utc)
    return now.strftime("%Y-%m-%dT%H:%M:%S.") + f"{now.microsecond // 1000:03d}Z"


while True:
    with open("/shared/log.txt", "a") as f:
        f.write(f"{timestamp()} {random_string}")

    time.sleep(5)