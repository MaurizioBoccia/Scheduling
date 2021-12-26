\ Model BinPackProb
\ LP format - for model browsing. Use MPS format to capture full model detail.
Minimize
  G[0] + G[1]
Subject To
 Assignment[0]: C[0,0] + C[1,0] = 1
 Assignment[2]: C[0,2] + C[1,2] = 1
 Assignment[4]: C[0,4] + C[1,4] = 1
 Assignment[6]: C[0,6] + C[1,6] = 1
 Assignment[8]: C[0,8] + C[1,8] = 1
 Assignment[9]: C[0,9] + C[1,9] = 1
 Capacity[0]: - 6 G[0] + 1.6 C[0,0] + 1.8 C[0,2] + 1.2 C[0,4] + 2.2 C[0,6]
   + 1.3 C[0,8] + 1.2 C[0,9] <= 0
 Capacity[1]: - 6 G[1] + 1.6 C[1,0] + 1.8 C[1,2] + 1.2 C[1,4] + 2.2 C[1,6]
   + 1.3 C[1,8] + 1.2 C[1,9] <= 0
 Sorting[1]: - G[0] + G[1] <= 0
Bounds
Binaries
 G[0] G[1] C[0,0] C[0,2] C[0,4] C[0,6] C[0,8] C[0,9] C[1,0] C[1,2] C[1,4]
 C[1,6] C[1,8] C[1,9]
End
