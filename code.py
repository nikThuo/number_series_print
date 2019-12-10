#!/usr/bin/env python
# coding: utf-8
from __future__ import division
import numpy as np
import pandas as pd
import time
import csv
import logging
import argparse
import traceback
import os
import re

# from IPython.display import clear_output

# nothing much here really...
program_starts = time.time()
FORMAT = '%(asctime)-15s %(levelno)s %(created)f %(lineno)d %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('tcpserver')
logger.setLevel(logging.DEBUG)


def main():
    parser = argparse.ArgumentParser(description="Change Detection")
    parser.add_argument("--modelfile", "-mf", help="Model to load model from", default=None)
    args = parser.parse_args()
    try:
        if args.modelfile is not None:
            # get and read the file
            logger.info("Loading data to file")
            file1 = open('Attack_free_dataset.txt', 'r')
            # push the data to a dataframe
            mydata1 = pd.read_csv(file1, delimiter='\s+', usecols=[3, 1], delim_whitespace=False, header=None)
            logger.info("Sample extracted data with Time Stamp and Arbitration ID:\n{}".format(mydata1))
            file2 = open("Range.txt", "w")
            # ******************************************************************
            '''do analysis on the data. The goal is to go
            through the data, and for every instance of an arb id, less the timestamp above it
            say id A has time stamp 0.5, followed by id B with time stamp 0.7, so we take 0.7 less 0.5
            to get 0.2. Then go through the data again to pick the highest difference in relation to all ids
            and the lowest. Then also get the difference of the highest and lowest.'''
            extractpermode(mydata1, file2, "Snippet")
        else:
            logger.info("--Model file argument was not found")

    except Exception as e:
        traceback.print_exc(e)
        logger.error("Error extracting data from text file with id {}: {}".format(args.modelfile, str(e)))

def extractpermode(df1, outfile, message):
    try:
        logger.info("Writing data to file")
        df2 = pd.DataFrame(df1)
        df2['Range'] = df1[1].diff()
        print('This is DF2\n', df2)
        # ******************************************************************
        # This is the line that does the difference.....question is why do we have a null value on arb id 316?
        df2 = df2.groupby([3]).agg({'Range': [min, max, lambda x: max(x) - min(x)]})
        df2.index.names = ['ArbID']
        df2.rename(columns={'min': 'L_TStamp(L)', 'max': 'H_TStamp(H)', '<lambda>': 'Range(H-L)',
                            'Range': 'Arrival Time With TimeStamp Range'}, inplace=True)
        print('This is DF2 version II\n', df2)
        df2.columns = df2.columns.droplevel(level=0)
        print(df2)
        # Find missing value(s)
        print("Null Values\n", df2.isnull())
        # Fill null value(s)
        df2.fillna(value=0, inplace=True)
        print("DF2 with no Null Value(s)\n", df2)
        outfile.write(df2.to_string(header=None, index=None))
        outfile.close
        logger.info("\n\n.....*****Finito:\n\n{}".format(df2.head()))
        print("\n.....*****Time taken: {0} seconds.\n".format((time.time()) - program_starts))

    except Exception as e:
        traceback.print_exc(e)
        logger.error("Error {}: {}".format(outfile, str(e)))

if __name__ == '__main__':
    #  clear_output()
    main()

