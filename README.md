# csvcombine
[![CI](https://github.com/EEmGuzman/csvcombine/actions/workflows/test.yml/badge.svg)](https://github.com/EEmGuzman/csvcombine/actions/workflows/test.yml)

Combines multiple CSV files into a single one by printing to standard out. A new column, "filename", is added to the combined CSV to signify the origin file of a row of data.

## Usage

There are two primary ways to provide the CSV files that will be combined.

#### - Directory method
Place all of your CSV files into a single directory and pass it as an argument to csvcombine.py

```
python csvcombine.py ./fixtures/
```
#### - List files method
The paths to the files can be listed as multiple arguments

```
python csvcombine.py ./fixtures/accessories.csv ./fixtures/clothing.csv ./fixtures/household_cleaners.csv
````

**Note**: <ins>The methods cannot be combined</ins>. You must either include a single directory containing the relevant CSV files or each individual file path.


To save the newly combined CSV file, one should redirect the output standard output to a file. For example,


```
python csvcombine.py ./fixtures/accessories.csv ./fixtures/clothing.csv ./fixtures/household_cleaners.csv > combined_output.csv
```

## Output

If we have two files, appliances.csv and furniutre.csv:

|email_address|item|cost|
|-------------|----|----|
|e@email.com|blender|$500|
|m@email.com|microwave|$1000|

|item|color|
|----------|--------|
|chair|green|
|desk|brown|
|sofa|tan|

then csvcombine will output

|email_address|item|cost|color|filename|
|-------------|----|----|-----|--------|
|e@email.com|blender|$500||appliances.csv|
|m@email.com|microwave|$1000||appliances.csv|
||chair||green|furniture.csv|
||desk||brown|furniture.csv|
||sofa||tan|furniture.csv|

## Developer Dependencies
* pytest
* pytest-mock

