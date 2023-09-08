import time
from log import setup_logger

# Initialize logger
logger = setup_logger("audioviz")


# Main application loop
def main():
    logger.info("Starting...")

    fps = 60
    interval = 1.0 / fps
    last_frame = 0
    last_update = time.time()

    while True:
        if (time.time() - last_update) > (1.0 / fps):
            logger.debug("Producing frame %s", last_frame)
            last_frame = (last_frame + 1) % 10000
            last_update = time.time()

            # TODO: Create and render a frame
            

        else:
            elapsed = time.time() - last_update
            time.sleep(abs(interval - elapsed) * 0.99)


if __name__ == "__main__":
    main()
