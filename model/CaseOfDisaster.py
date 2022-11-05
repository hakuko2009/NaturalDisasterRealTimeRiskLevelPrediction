class CaseOfDisaster:
    def __init__(self, disNo, year, subtype, region, value, scale, startMonth, endMonth):
        self.disNo = disNo
        self.year = year
        self.subtype = subtype
        self.region = region
        self.value = value
        self.scale = scale
        self.startMonth = startMonth
        self.endMonth = endMonth
        self.level = 1

    def __getitem__(self, item):
        return item
