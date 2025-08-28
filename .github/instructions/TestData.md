##Scenario
You are required to create and test a new software system for a small shop
loaning fishing and camping equipment for hire to customers.
The fishing and camping equipment available for hire and the cost is shown
in figure 2. Customers can rent it from 9am to 6pm each day. The
equipment can be hired from 9am of day 1 but should be returned by 2pm
the next day irrespective of the time of collection on day 1. For each
additional night a 50% discount is applied for each piece of equipment
hired. If the equipment is returned after 2pm, it will still be counted as an
additional night and extra 50% payment for each piece of equipment hired
will need to be paid.
Your new software system should be able to record the details of the
customers and equipment hired as shown in figure 3. It should also provide
a report for the operator when required as shown in figure 4. For this, the
new software system should open with a menu as shown below

##Notes
Why this set works:
10+ hires (actually 10 customers listed).
Every equipment code from your CATALOG appears at least once.
Mix of different hire durations (2–6 nights).
Overdue days present (0–3).
Returned late flag varied (y/n).
Multiple items per hire in many cases.
Uses unquoted format (matching your preferred style).

##Input Data
Ted Danson,07970263076,1a,W4 0HY,2222
DCH, 3, 1, 1, y
BBT, 5, 2, 3, n
SLP, 3, 1, 1, n
TNT, 3, 1, 1, n

Bob Barker,09790263976,4b,G3 R30,1234
TNT, 3, 4, 0, n
STV, 3, 1, 0, n

Angela Lansbury,07980111222,7c,NW1 6XE,5678
BAS, 4, 1, 0, y
BA1, 2, 2, 1, n
R3T, 5, 1, 0, n

Tom Selleck,07973123456,22a,SW3 4QQ,3344
RBR, 3, 2, 0, y
REB, 4, 1, 2, n
DCH, 2, 1, 0, n

Patrick Stewart,07988987654,12b,YO1 8AB,7788
BCH, 3, 1, 0, n
BBT, 2, 1, 1, y
TNT, 5, 1, 0, n

Mary Tyler Moore,07990112233,8d,L1 5FF,4455
SLP, 2, 2, 0, n
STV, 3, 1, 0, n
R3T, 3, 1, 1, y

James Garner,07965478912,15c,BS1 4ZZ,8899
BAS, 3, 1, 0, n
BA1, 4, 3, 0, n
BCH, 2, 1, 1, y

Dick Van Dyke,07990887766,3f,EH1 1YZ,5566
RBR, 5, 2, 0, y
REB, 3, 1, 0, n
STV, 4, 1, 2, y

Carol Burnett,07977001122,9e,CF10 1AA,9900
DCH, 4, 1, 0, n
SLP, 3, 1, 1, y
BAS, 2, 1, 0, n

Bill Cosby,07972112233,11h,M1 4LL,2233
TNT, 2, 1, 0, y
BBT, 6, 1, 1, n
R3T, 3, 2, 0, n


##Report Outpput
=== Earnings Report (Summary by Hire) ===
ID   CUSTOMER                 ITEMS  GRAND TOTAL
---  ------------------------  -----  -----------
101  Ted Danson                    5  £   1187.50
102  Bob Barker                    5  £    270.00
103  Angela Lansbury               4  £    170.00
104  Tom Selleck                   4  £    125.00
105  Patrick Stewart               3  £    385.00
106  Mary Tyler Moore              4  £    155.00
107  James Garner                  5  £    207.50
108  Dick Van Dyke                 4  £    150.00
109  Carol Burnett                 3  £    190.00
110  Bill Cosby                    4  £    530.00
------------------------------------------------------
TOTAL EARNINGS: £3370.00

Detail lines (all entered data):
ID   CODE  ITEM                                NIGHT  QTY  OVERDUE  LATE  BASE     OVERDUE   PENALTY   LINE TOTAL
---  ----  ----------------------------------  -----  ---  -------  ----  -------  --------  --------  ----------
101  DCH   Day chairs                              3    1        1   y    £ 45.00  £  15.00  £   7.50  £    67.50
101  BBT   Bait Boat                               5    2        3   n    £600.00  £ 360.00  £   0.00  £   960.00
101  SLP   Sleeping bag                            3    1        1   n    £ 60.00  £  20.00  £   0.00  £    80.00
101  TNT   Camping tent                            3    1        1   n    £ 60.00  £  20.00  £   0.00  £    80.00
102  TNT   Camping tent                            3    4        0   n    £240.00  £   0.00  £   0.00  £   240.00
102  STV   Camping Gas stove (Double burner)       3    1        0   n    £ 30.00  £   0.00  £   0.00  £    30.00
103  BAS   Bite Alarm (set of 3)                   4    1        0   y    £ 80.00  £   0.00  £  10.00  £    90.00
103  BA1   Bite Alarm (single)                     2    2        1   n    £ 20.00  £  10.00  £   0.00  £    30.00
103  R3T   Rods (3lb TC)                           5    1        0   n    £ 50.00  £   0.00  £   0.00  £    50.00
104  RBR   Rods (Bait runners)                     3    2        0   y    £ 30.00  £   0.00  £   5.00  £    35.00
104  REB   Reels (Bait runners)                    4    1        2   n    £ 40.00  £  20.00  £   0.00  £    60.00
104  DCH   Day chairs                              2    1        0   n    £ 30.00  £   0.00  £   0.00  £    30.00
105  BCH   Bed chairs                              3    1        0   n    £ 75.00  £   0.00  £   0.00  £    75.00
105  BBT   Bait Boat                               2    1        1   y    £120.00  £  60.00  £  30.00  £   210.00
105  TNT   Camping tent                            5    1        0   n    £100.00  £   0.00  £   0.00  £   100.00
106  SLP   Sleeping bag                            2    2        0   n    £ 80.00  £   0.00  £   0.00  £    80.00
106  STV   Camping Gas stove (Double burner)       3    1        0   n    £ 30.00  £   0.00  £   0.00  £    30.00
106  R3T   Rods (3lb TC)                           3    1        1   y    £ 30.00  £  10.00  £   5.00  £    45.00
107  BAS   Bite Alarm (set of 3)                   3    1        0   n    £ 60.00  £   0.00  £   0.00  £    60.00
107  BA1   Bite Alarm (single)                     4    3        0   n    £ 60.00  £   0.00  £   0.00  £    60.00
107  BCH   Bed chairs                              2    1        1   y    £ 50.00  £  25.00  £  12.50  £    87.50
108  RBR   Rods (Bait runners)                     5    2        0   y    £ 50.00  £   0.00  £   5.00  £    55.00
108  REB   Reels (Bait runners)                    3    1        0   n    £ 30.00  £   0.00  £   0.00  £    30.00
108  STV   Camping Gas stove (Double burner)       4    1        2   y    £ 40.00  £  20.00  £   5.00  £    65.00
109  DCH   Day chairs                              4    1        0   n    £ 60.00  £   0.00  £   0.00  £    60.00
109  SLP   Sleeping bag                            3    1        1   y    £ 60.00  £  20.00  £  10.00  £    90.00
109  BAS   Bite Alarm (set of 3)                   2    1        0   n    £ 40.00  £   0.00  £   0.00  £    40.00
110  TNT   Camping tent                            2    1        0   y    £ 40.00  £   0.00  £  10.00  £    50.00
110  BBT   Bait Boat                               6    1        1   n    £360.00  £  60.00  £   0.00  £   420.00
110  R3T   Rods (3lb TC)                           3    2        0   n    £ 60.00  £   0.00  £   0.00  £    60.00

