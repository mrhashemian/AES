from enum import Enum
from collections import namedtuple

name_tuple = namedtuple("tuple", ['value', 'description'])


class BaseEnum(Enum):
    @classmethod
    def get_value_list(cls):
        return list(map(lambda x: x.value, cls))

    @classmethod
    def get_value_dict(cls):
        return dict(zip(list(a.value for a in cls), list(a.description for a in cls)))

    @property
    def description(self):
        return self._value_.description

    @property
    def value(self):
        return self._value_.value


class AESMode(BaseEnum):
    MODE_ECB = name_tuple(1, "MODE_ECB")
    MODE_CBC = name_tuple(2, "MODE_CBC")
    MODE_CFB = name_tuple(3, "MODE_CFB")
    MODE_OFB = name_tuple(5, "MODE_OFB")
    # MODE_CTR = name_tuple(6, "MODE_CTR")
    # MODE_OPENPGP = name_tuple(7, "MODE_OPENPGP")
    # MODE_CCM = name_tuple(8, "MODE_CCM")
    MODE_EAX = name_tuple(9, "MODE_EAX")
    # MODE_SIV = name_tuple(10, "MODE_SIV")
    MODE_GCM = name_tuple(11, "MODE_GCM")
    # MODE_OCB = name_tuple(12, "MODE_OCB")


class TDESMode(BaseEnum):
    MODE_ECB = name_tuple(1, "MODE_ECB")
    MODE_CBC = name_tuple(2, "MODE_CBC")
    MODE_CFB = name_tuple(3, "MODE_CFB")
    MODE_OFB = name_tuple(5, "MODE_OFB")
    # MODE_CTR = name_tuple(6, "MODE_CTR")
    # MODE_OPENPGP = name_tuple(7, "MODE_OPENPGP")
    MODE_EAX = name_tuple(9, "MODE_EAX")
