from kafka import KafkaConsumer
from kafka import KafkaProducer
import click
import json
import time

from .logger import logger
from . import helpers
from . import threadpool
from . import webget


@click.command()
@click.option(
    "--broker-list",
    type=str,
    default="localhost:9092",
    help="all brokens",
    show_default=True,
    show_envvar=True,
    envvar="KAFKA_BROKER_LIST",
    metavar="brokerList",
)
@click.option(
    "--from-topic",
    type=str,
    required=True,
    default="crawler_task",
    help="subscribe topic",
    prompt="Please enter subscribe topic",
    metavar="fromTopic",
)
@click.option(
    "--to-topic",
    type=str,
    required=True,
    default="deal_task",
    help="publish topic",
    prompt="Please enter publish topic",
    metavar="toTopic",
)
@click.option(
    "--group-id", default=None, type=str, help="consumer group id", metavar="groupId",
)
@click.option(
    "--thread-count",
    default=3,
    type=click.IntRange(1, 10, clamp=True),
    help="run thread count",
    metavar="threadCount",
)
@click.option(
    "--level",
    type=click.IntRange(1, 5, clamp=True),
    default=1,
    show_default=True,
    help="log level [1-5]",
    metavar="logLevel",
)
def main(broker_list, from_topic, to_topic, group_id, thread_count, level):

    try:
        # 设置线程池数量
        tpool = threadpool.threadPoolManager(thread_count, 10)

        logger.setLevel((6 - level) * 10)
        brokers = list(map(lambda s: str.strip(s), broker_list.split(",")))

        # 消费者
        consumer = KafkaConsumer(
            from_topic, group_id=group_id, bootstrap_servers=brokers,
        )

        # 生产者
        producer = KafkaProducer(bootstrap_servers=brokers)

        # 消息处理逻辑
        def msg_deal(res, err=None, tasks=None):
            if err is not None:
                print(err)
                return

            if res.status_code != 200:
                print("status_code: %s", res.status_code)
                return

            value = json.dumps(
                {
                    "task": tasks,
                    "content_type": res.headers.get("content-type"),
                    "content": str(res.content, encoding="utf-8"),
                }
            )
            producer.send(to_topic, value=bytes(value, encoding="utf-8"))

        for msg in consumer:
            logger.debug(
                "%s:%s:%s key=%s value=%s"
                % (msg.topic, msg.partition, msg.offset, msg.key, msg.value)
            )

            # 消息数据
            try:
                msg_data = json.loads(msg.value)

            except json.JSONDecodeError as e:
                logger.warning("msg.value[%s] can not decode", msg.value)
                continue

            print(msg_data)

            url = msg_data["url"] if "url" in msg_data else None

            tasks = msg_data["tasks"] if "tasks" in msg_data else []

            is_msg_ok = True

            if url is None or not helpers.is_valid_url(url):
                logger.error("msg_data.url: <%s> is not valid!" % url)
                is_msg_ok = False

            elif type(tasks) != list or len(tasks) == 0:
                logger.error("msg_data.task: <%s> is empty!" % tasks)
                is_msg_ok = False

            if not is_msg_ok:
                continue

            tpool.add_work(webget.WebGet(url, cb=msg_deal, passthrough=tasks))

    except Exception as e:
        logger.error(e)

    finally:
        tpool.close_thread_pool()
