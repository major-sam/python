import peewee as pw

proxy = pw.Proxy()


class BaseModel(pw.Model):
    class Meta:
        database = proxy


class Date(BaseModel):
    date = pw.CharField(index=True, unique=True)


class DayStats(BaseModel):
    date = pw.ForeignKeyField(Date, index=True, unique=True)
    daytime = pw.CharField()
    humidity = pw.CharField()
    pressure = pw.CharField()
    rain_probability = pw.CharField()
    sky = pw.CharField()
    temperature = pw.CharField()
    temperature_feeling = pw.CharField()


class NightStats(BaseModel):
    date = pw.ForeignKeyField(Date, index=True, unique=True)
    daytime = pw.CharField()
    humidity = pw.CharField()
    pressure = pw.CharField()
    rain_probability = pw.CharField()
    sky = pw.CharField()
    temperature = pw.CharField()
    temperature_feeling = pw.CharField()
