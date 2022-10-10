class CaseOfDisaster:
    def __init__(self, disNo, year, subtype, country, region, startMonth, endMonth):
        self.disNo = disNo
        self.year = year
        self.subtype = subtype
        self.country = country
        self.region = region
        self.startMonth = startMonth
        self.endMonth = endMonth
        self.level = 1

    def __getitem__(self, item):
        return item
