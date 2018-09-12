"""cSHAKE test script
    Author: Ran Pang
    
    Test vectors are from NIST: http://csrc.nist.gov/groups/ST/toolkit/documents/Examples/cSHAKE_samples.pdf
"""

from cSHAKE import *
import rdtsc

start1 = rdtsc.get_cycles()
sample1 = cSHAKE128(unhexlify('00010203'), 256, '', 'Email Signature')
stop1 = rdtsc.get_cycles()
if sample1 == 'c1c36925b6409a04f1b504fcbca9d82b4017277cb5ed2b2065fc1d3814d5aaf5':
    print 'Sample1 correct!'
else:
    print 'Sample1 incorrect!'

start2 = rdtsc.get_cycles()
sample2 = cSHAKE128(unhexlify('000102030405060708090a0b0c0d0E0f101112131415161718191a1b1c1d1E1f202122232425262728292a2b2c2d2E2f303132333435363738393a3b3c3d3E3f404142434445464748494a4b4c4d4E4f505152535455565758595a5b5c5d5E5f606162636465666768696a6b6c6d6E6f707172737475767778797a7b7c7d7E7f808182838485868788898a8b8c8d8E8f909192939495969798999a9b9c9d9E9fa0a1a2a3a4a5a6a7a8a9aaabacadaEafb0b1b2b3b4b5b6b7b8b9babbbcbdbEbfc0c1c2c3c4c5c6c7'), 256, '', 'Email Signature')
stop2 = rdtsc.get_cycles()
if sample2 == 'c5221d50e4f822d96a2e8881a961420f294b7b24fe3d2094baed2c6524cc166b':
    print 'Sample2 correct!'
else:
    print 'Sample2 incorrect!'

start3 = rdtsc.get_cycles()
sample3 = cSHAKE128(unhexlify(''), 256, '', '')
stop3 = rdtsc.get_cycles()
if sample3 == '7f9c2ba4e88f827d616045507605853ed73b8093f6efbc88eb1a6eacfa66ef26':
    print 'Sample3 correct!'
else:
    print 'Sample3 incorrect!'

start4 = rdtsc.get_cycles()
sample4 = cSHAKE256(unhexlify('00010203'), 512, '', 'Email Signature')
stop4 = rdtsc.get_cycles()
if sample4 == 'd008828e2b80ac9d2218ffee1d070c48b8e4c87bff32c9699d5b6896eee0edd164020e2be0560858d9c00c037e34a96937c561a74c412bb4c746469527281c8c':
    print 'Sample4 correct!'
else:
    print 'Sample4 incorrect!'

start5 = rdtsc.get_cycles()
sample5 = cSHAKE256(unhexlify('000102030405060708090a0b0c0d0E0f101112131415161718191a1b1c1d1E1f202122232425262728292a2b2c2d2E2f303132333435363738393a3b3c3d3E3f404142434445464748494a4b4c4d4E4f505152535455565758595a5b5c5d5E5f606162636465666768696a6b6c6d6E6f707172737475767778797a7b7c7d7E7f808182838485868788898a8b8c8d8E8f909192939495969798999a9b9c9d9E9fa0a1a2a3a4a5a6a7a8a9aaabacadaEafb0b1b2b3b4b5b6b7b8b9babbbcbdbEbfc0c1c2c3c4c5c6c7'), 512, '', 'Email Signature')
stop5 = rdtsc.get_cycles()
if sample5 == '07dc27b11e51fbac75bc7b3c1d983e8b4b85fb1defaf218912ac86430273091727f42b17ed1df63e8ec118f04b23633c1dfb1574c8fb55cb45da8e25afb092bb':
    print 'Sample5 correct!'
else:
    print 'Sample5 incorrect!'

start6 = rdtsc.get_cycles()
sample6 = cSHAKE256(unhexlify(''), 512, '', '')
stop6 = rdtsc.get_cycles()
if sample6 == '46b9dd2b0ba88d13233b3feb743eeb243fcd52ea62b81b82b50c27646ed5762fd75dc4ddd8c0f200cb05019d67b592f6fc821c49479ab48640292eacb3b7c4be':
    print 'Sample6 correct!'
else:
    print 'Sample6 incorrect!'

print 'Sample1: ', (stop1 - start1), '|', 'Sample2: ', (stop2 - start2), '|', 'Sample3: ', (stop3 - start3), '|', 'Sample4: ', (stop4 - start4), '|', 'Sample5: ', (stop5 - start5), '|', 'Sample6: ', (stop6 - start6)
