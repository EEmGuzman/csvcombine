#!/usr/bin/env python3

import sys
import os
import filecmp
import csvcombine
import pytest

###################


@pytest.fixture
def mock_appliances_csv(tmp_path):
    mapp_data = ['"email_address","item","cost"',
                 '"e@email.com","blender","$500"',
                 '"j@email.com","microwave","$1000"\n']
    datafile = tmp_path / "test_appliances.csv"
    datafile.write_text("\n".join(mapp_data))
    return datafile


@pytest.fixture
def mock_appliances_truth_csv(tmp_path):
    mapp_data_truth = ['"email_address","item","cost","filename"',
                       '"e@email.com","blender","$500","test_appliances.csv"',
                       '"j@email.com","microwave","$1000","test_appliances.csv"\n']
    datafile = tmp_path / "test_appliances_truth.csv"
    datafile.write_text("\n".join(mapp_data_truth))
    return datafile


@pytest.fixture
def mock_furniture_csv(tmp_path):
    mfurn_data = ['"item","color"',
                  '"chair","green"',
                  '"desk","brown"',
                  '"sofa","tan"\n']
    datafile = tmp_path / "test_furniture.csv"
    datafile.write_text("\n".join(mfurn_data))
    return datafile


@pytest.fixture
def mock_combined_csv(tmp_path):
    mcombo_data = ['"email_address","item","cost","color","filename"',
                   '"e@email.com","blender","$500","","test_appliances.csv"',
                   '"j@email.com","microwave","$1000","","test_appliances.csv"',
                   '"","chair","","green","test_furniture.csv"',
                   '"","desk","","brown","test_furniture.csv"',
                   '"","sofa","","tan","test_furniture.csv"\n']
    datafile = tmp_path / "test_combined.csv"
    datafile.write_text("\n".join(mcombo_data))
    return datafile

###################


@pytest.mark.parametrize("tpaths", [["./test_data"],
                         ["./test_data/test_appliances.csv",
                          "./test_data/test_furniture.csv"]])
def test_get_csv_paths(mocker, tpaths):
    mocker.patch('os.listdir', return_value=['test_appliances.csv',
                                             'test_furniture.csv'])
    truth = sorted(["./test_data/test_appliances.csv", 
                    "./test_data/test_furniture.csv"])
    assert sorted(csvcombine.get_csv_paths(tpaths)) == truth


def test_get_csv_header(mock_appliances_csv):
    h = csvcombine.get_csv_header(mock_appliances_csv)
    assert h == ["email_address", "item", "cost"]


def test_combine_csv_headers(mock_appliances_csv, mock_furniture_csv):
    ch = csvcombine.combine_csv_headers([mock_appliances_csv, mock_furniture_csv])
    assert ch == ["email_address", "item", "cost", "color"]


def test_read_one_csv(mock_appliances_csv, mock_appliances_truth_csv):
    fnames = mock_appliances_csv
    hnames = ["email_address", "item", "cost"]

    with open('./tmp.csv', 'w', newline='') as sys.stdout:
        csvcombine.read_one_csv(fnames, hnames, wheader=True)

    answer = filecmp.cmp('./tmp.csv', mock_appliances_truth_csv)
    os.remove('./tmp.csv')
    assert answer == True


def test_main(mock_appliances_csv, mock_furniture_csv, mock_combined_csv):
    with open('./tmp_main.csv', 'w') as sys.stdout:
        csvcombine.main([mock_appliances_csv, mock_furniture_csv])
    answer = filecmp.cmp('./tmp_main.csv', mock_combined_csv)
    os.remove('./tmp_main.csv')
    assert answer == True
