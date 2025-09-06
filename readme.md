# Hybrid LFSR–BBS Pseudorandom Number Generator  

Combine LFSR with a BBS update rule to produce pseudorandom bits.  
## Algorithm Idea  
1. **Initialize:**  
   - Choose safe primes `p`, `q` and compute `N = p*q`.  
   - Set initial state `s` for the LFSR and a seed `x` for BBS.  

2. **LFSR update:**  
   - Compute feedback bit as the XOR of selected tap positions.  
   - Shift register state left and insert the new bit.  

3. **BBS update:**  
   - Compute `exp = 2 + (lsb(s) XOR lsb(x))`.  
   - Update `x = x^exp mod N`.  

4. **Output bit:**  
   - Take the XOR of the LFSR’s most significant bit and the BBS’s least significant bit.  
   - Append this as the next output bit.  

5. **Repeat** until required number of bits are generated.  


