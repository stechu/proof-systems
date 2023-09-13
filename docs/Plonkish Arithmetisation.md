## Plonkish Arithmetisation

Halo2 uses Plonkish Arithmetisation (see other kinds of arithmetisations [here](https://github.com/stechu/zk-study-notes/blob/main/arithmetisations.pdf)).  In addition to GWC19 (so called Vallina Plonk), Halo2 also supports many advanced Plonk features, like customized gates, lookup tables, which we will introduce in sequence. 

### Vallina Plonk

A Plonkish circuit consists of a table/matrix with the following fixed columns and nearly arbitrary number of rows:

| $a$ | $b$ | $c$ | $q_L$ | $q_R$ | $q_M$ | $q_C$ | $q_O$ | 
| -------- | -------- | -------- | -- | -- | -- | -- | -- |
|   .   |  .    |  .    |     |    |    |    |    |

where the numbers in the columns $q_L, \dotsc, q_O$ are **fixed** once and for all at compile time. Meanwhile the numbers in columns $a, b,c$ are called **witnesses** and specified by the prover each time a new proof is generated. The circuit represents a constraint satisfaction problem (a NP relation), that is expressed by asserting that the following equation holds for each row $i$:

$$
q_L \cdot a + q_R \cdot b + q_M \cdot a \cdot b + q_C = q_O \cdot c 
$$
Since the $q$s are fixed once and for all, specifying these numbers allows you to "mold" the circuit to constrain the witnesses $a,b,c$ to perform certain computations. 

For example, if you want to add $a_i + b_i = c_i$ in row $i$, put:

| $a$ | $b$ | $c$ | $q_L$ | $q_R$ | $q_M$ | $q_C$ | $q_O$ | 
| -------- | -------- | -------- | -- | -- | -- | -- | -- |
| $a_i$ | $b_i$ | $c_i$ | 1 | 1 | 0 | 0 | 1 |

To multiply $a_i \cdot b_i = c_i$ in row $i$, put:

| $a$ | $b$ | $c$ | $q_L$ | $q_R$ | $q_M$ | $q_C$ | $q_O$ | 
| -------- | -------- | -------- | -- | -- | -- | -- | -- |
| $a_i$ | $b_i$ | $c_i$ | 0 | 0 | 1 | 0 | 1 |

To force $a_i$ to be a known constant $A$, put:

| $a$ | $b$ | $c$ | $q_L$ | $q_R$ | $q_M$ | $q_C$ | $q_O$ | 
| -------- | -------- | -------- | -- | -- | -- | -- | -- |
| $a_i$ | * | * | 1 | 0 | 0 | $-A$ | 0 |

Note that $b_i, c_i$ can be any numbers and it doesn't matter. 

Next, these single line equations needs to be "connected" through copy constraints: one can also specify once and for all that certain predetermined cells in the table above are always equal. For example for some $i_0$, we must have $c_{i_0} = a_{i_0 + 1}$. This now allows us to carry results of previous computations into new computations, "chaining" to create longer computations. 



