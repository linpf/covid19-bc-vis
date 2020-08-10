from datetime import date
d1 = date.today()
print("week no",d1.isocalendar()[1])
print("isocalendar",d1.isocalendar())
d2 = date.fromisoformat("2020-06-01")
d3 = date(2020,5,28)
delta = d1 - d2
delta2 = d1 - d3
print(delta.days)
print(delta2.days)
