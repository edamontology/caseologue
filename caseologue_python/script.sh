#!/bin/bash


EDAM_PATH=./queries/$1_test_data.owl python3 -m unittest caseologue.EdamQueryTest.test_$1
status=$?
if test $status -eq 0
then
	exit 1
else
	exit 0
fi