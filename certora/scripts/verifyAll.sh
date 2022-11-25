#!/bin/bash

script=${0};
echo "${script}";
echo "";

for FILE in certora/scripts/*;
do
    current_file="${FILE}";
    echo "the current file in the loop is: ${current_file}";
    echo "the current script path is: ${script}";
    if [[ "${current_file}" == *"${script}"* ]];
    then
        echo "The two files are the same: current file = ${current_file} and script = ${script}";
    else
        echo "The two files are NOT the same: current file = ${current_file} and script = ${script}";
        ${FILE};
    fi
    echo "";
    echo "";
done