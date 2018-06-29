#!/bin/sh

q=2

while read p
do
    r=`python3 -c "print($q * $p)"`
    #r=$p
    echo $r
    time sh -c "echo $r | python3 factor.py >res$PPID.txt"
    test 2 = `tail -1 res$PPID.txt` || {
        echo failed for $r
        break
    }
    cat res$PPID.txt
    q=$p
done <<EOF
2038079033
2038079651
2038080199
2038080659
2038079039
2038079671
2038080203
2038080679
2038079047
2038079677
2038080227
2038080701
2038079093
2038079713
2038080263
2038080757
2038079117
2038079737
2038080281
2038080791
2038079191
2038079789
2038080307
2038080799
2038079203
2038079801
2038080323
2038080827
2038079227
2038079803
2038080329
2038080829
2038079233
2038079819
2038080367
2038080857
2038079273
2038079873
2038080397
2038080893
2038079279
2038079891
2038080413
2038080901
2038079293
2038079959
2038080427
2038080907
2038079341
2038080001
2038080431
2038080929
2038079419
2038080013
2038080463
2038080959
2038079423
2038080019
2038080493
2038080977
2038079453
2038080041
2038080511
2038080983
2038079467
2038080097
2038080529
2038081021
2038079521
2038080103
2038080553
2038081039
2038079551
2038080113
2038080559
2038081051
2038079569
2038080119
2038080563
2038081061
2038079573
2038080131
2038080587
2038081063
2038079587
2038080137
2038080613
2038081079
2038079591
2038080167
2038080617
2038081127
2038079609
2038080181
2038080641
2038081139
2038079623
2038080197
2038080643
2038081147
179424691
179425033
179425601
179426083
179424697
179425063
179425619
179426089
179424719
179425069
179425637
179426111
179424731
179425097
179425657
179426123
179424743
179425133
179425661
179426129
179424779
179425153
179425693
179426141
179424787
179425171
179425699
179426167
179424793
179425177
179425709
179426173
179424797
179425237
179425711
179426183
179424799
179425261
179425777
179426231
179424821
179425319
179425811
179426239
179424871
179425331
179425817
179426263
179424887
179425357
179425819
179426321
179424893
179425373
179425823
179426323
179424899
179425399
179425849
179426333
179424907
179425403
179425859
179426339
179424911
179425423
179425867
179426341
179424929
179425447
179425879
179426353
179424937
179425453
179425889
179426363
179424941
179425457
179425907
179426369
179424977
179425517
179425943
179426407
179424989
179425529
179425993
179426447
179425003
179425537
179426003
179426453
179425019
179425559
179426029
179426491
179425027
179425579
179426081
179426549
EOF
