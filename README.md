# Slots

Modelling of slot- game.

There is an output matrix $N \times M$. 

There are $P$ items(symbols) corresponding for each column.
The probability of the $i$-th item to be on the any row on the $j$-th
column is equal $p_{i,j}$.
The column is formed by the next rule:
at first the bottom row is formed, than another symbol is generated
on the upper row - this symbol cannot be the same that is on bottom row:
so the probality of $i_1$-th item to be there is $p_{i_1}/(1-p_{i})$, where
$i \neq i_1$. The same way, the next symbol cannot equal to any of the previous
ones, therefore, the probabilyty of the $i2$-th item to be on the column is
$p_{i_2}/(1-p_{i}-p_{i_1}))$. By continuing so on, the last probability is
$p_{i_N}/(1-p_{i}-p_{i_1} -p_{i_{N-1}}))$.

If there are same $l$ symbols in the first $K$ columns then the output result
is $S_{l,K}$.
