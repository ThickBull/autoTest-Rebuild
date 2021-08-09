__all__ = ['var', 'helper', 'CheckPoint', 'Step']

from core.log import Logger


def CheckPoint(obj):
    Logger.get_logger().info(obj)


def Step(obj):
    Logger.get_logger().info(obj)
