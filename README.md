# COMP6925
## Lab II 
### Part A
#### Variable Formulation
`x` stores amount of mushrooms to be purchased  
Columns record net quantity to be purchased **ON** a day  
Rows record net quantity to be purchased **FOR** a day  

e.g.
<ul style="list-style: none;">
  <li> x[1] + x[2] represents the net quantity bought on Monday </li>
  <li> x[2] + x[3] represents net quantity bought for Tuesday </li> 
  <li> Hence, x[2] (bought <b>ON</b> Monday), is bought <b>FOR</b> Tuesday </li>  
</ul>


| Mon | Tue | Wed | Thu | Fri | Sat | **_Demand(lb)_** | _Day_ | *Cost (per lb)* |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `x[1]` | | | | | | 295 | *Mon* | 16 |
| `x[2]`| `x[3]` | | | | | 240 | *Tue* | 16 |
| | `x[4]` | `x[5]` | | | | 235 | *Wed* | 32 |
| | | `x[6]` | `x[7]` | | | 187 | *Thu* | 23 |
| | | | `x[8]` | `x[9]` | | 152 | *Fri* | 20 |
| | | | | `x[10]` | `x[11]` | 198 | *Sat* | 15 |

#### Objective 
Minimize product of cost-per-day (per pound) and net quantity purchased **ON** all days


**Total Cost:**  22674.54366572725  
**Monday:** 535.72329710955  
**Tuesday:** 235.89462053795  
**Wednesday:** 0.0  
**Thursday:** 187.39292285725  
**Friday:** 152.11896090765  
**Saturday:** 198.4160359665  
