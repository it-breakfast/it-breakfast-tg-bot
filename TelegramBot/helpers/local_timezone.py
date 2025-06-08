from datetime import timedelta, tzinfo

class UTC0700(tzinfo):
    _offset = timedelta(seconds = 25200)
    _dst = timedelta(0)
    name_ = "+0700"
    def __repr__(self):
        return self.__class__.name_
    def utcoffset(self, dt):
        return self.__class__._offset
    def dst(self, dt):
        return self.__class__._dst
    def tzname(self, dt):
        return self.__class__._name

bangkok_tz = UTC0700()