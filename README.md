# SQLAlchemy Homework - Surfs Up!

## Overview
I've decided to treat myself to a long holiday vacation in Honolulu, Hawaii! To help with my trip planning, I need to do some climate analysis on the area. I used Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis will be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.

## Analysis
The first paet consisted in obtaining the precipitation scores during the last year of data and save these results into a Panda's DataFrame. The first 5 rows of the DataFrame created in shown below
|  | prec  |
| :---:   | :-: |
| date |  |
| 2016-08-23 | 0.00 |
| 2016-08-23 | 1.79 |
| 2016-08-23 | 0.05 |
| 2016-08-23 | 0.15 |
| 2016-08-23 | 0.70 |

The plot of Precipitation values in the last year of data is shown in the next Figure:

![ScreenShot](/screenshots/prcp_plot.png)

### Summary Statistics for the Precipitation Data
|  | prcp  |
| count |2021.000000 |
| mean | 0.177279 |
| std | 0.461190 |
| min | 0.000000 |
| 25% | 0.000000 |
| 50% | 0.020000 |
| 75% | 0.130000 |
| max | 6.700000 |

### Bar plot for most-active stations
![ScreenShot](/screenshots/bar_plot.png)
