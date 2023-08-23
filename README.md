# WebaltoPositioning

WebaltoPositioning is a Python package that contains a class object "Position" to get positioning data from webalto.

There are 3 kinds of positioning that could be obtained:
* Fx Positions
* Credit Positions (by sector & by currencies)
* Rates Positions (by maturiy & by currencies)

## Installation

Open CMD prompt and us below command to the direct

```bash
cd C:\where you have downlaod the package
```

Then run
```bash
python setup.py install
```

## Usage

For class Position, you need to input the belows variable:

* ticker: fund code of the portfolio you would like to update, e.g. "X2947"
* updatetype: default "ALL", positioning type ("Rates", "Credit", "Fx" or "All") you would like to update, 
* date: default "datetime.date.today()", update until which day
* days: default "5", download how many days of data
* file_path: default "P:\\Product Specialists\\Tools\\Position Monitor\\", indicates where to read and save the file

```python
from WebaltoPositioning import Positioning

from datetime import datetime
from datetime import date

date_str = "2023-08-09"
date_object = datetime.strptime(date_str, '%Y-%m-%d').date()

Positioning.Position(ticker = "X2947",
         updatetype = "All",
         date = date_object,
         days = 5,
         file_path = "P:\\Product Specialists\\Tools\\Position Monitor\\")
```

## Attributes

Position objects have below attributes:
* Position.ticker: indicate the portfolio of the positions
* Position.updatetype: indicated which kind of position has been updated
* Position.file_path: indicate where to read and save the database
* Position.fx: Fx position
* Position.credit: Credit position by sector
* Position.rates: Rates position

```python
print(X2947.ticker)

print(X2947.updatetype)

print(X2947.file_path)

print(X2947.rates)

print(X2947.credit)

print(X2947.fx)
```

## Export

To export the data, use SavePosition. You can choose to save "Rates", "Fx", "Credit" or "All"

```python
X2947.SavePosition("Fx")

X2947.SavePosition("Rates")

X2947.SavePosition("Credit")

X2947.SavePosition("All")
```

## License

[MIT](https://choosealicense.com/licenses/mit/)
