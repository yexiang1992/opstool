

model BasicBuilder -ndm 2 -ndf 3
#reliability


set framemass1 15.0
set framemass2 30.0
set framemass3  4.0

# --�ڵ��  X    Y     ����       X          Y        Z
node  1    0     0    -mass $framemass1 $framemass1 0.0
node  2    0    3.6   -mass $framemass1 $framemass1 0.0
node  3    0    7.2   -mass $framemass1 $framemass1 0.0
node  4   7.0   0.0   -mass $framemass2 $framemass2 0.0
node  5   7.0   3.6   -mass $framemass2 $framemass2 0.0
node  6   7.0   7.2   -mass $framemass2 $framemass2 0.0
node  7  14.0   0.0   -mass $framemass1 $framemass1 0.0
node  8  14.0   3.6   -mass $framemass1 $framemass1 0.0
node  9  14.0   7.2   -mass $framemass1 $framemass1 0.0

node  10  0.0  -2.4   -mass $framemass3 $framemass3 0.0
node  11  0.0  -1.2   -mass $framemass3 $framemass3 0.0
node  12  7.0  -2.4   -mass $framemass3 $framemass3 0.0
node  13  7.0  -1.2   -mass $framemass3 $framemass3 0.0
node  14 14.0  -2.4   -mass $framemass3 $framemass3 0.0
node  15 14.0  -1.2   -mass $framemass3 $framemass3 0.0

# 

recorder Node -file disp6.out   -time  -node 6  -dof 1 2 disp   
recorder Node -file disp5.out   -time  -node 5  -dof 1 2 disp 
recorder Node -file disp4.out   -time  -node 4  -dof 1 2 disp 



set upperload1 [expr -$framemass1*10.0]
set upperload2 [expr -$framemass2*10.0]
set download3  [expr -$framemass3*10.0]


#pattern Plain 2 {Series -time {0.0 2.0 100000.0} -values {0.0 1.0 1.0} } {
pattern Plain 2 "Constant"  {
load 1 0.0 $upperload1 0
load 2 0.0 $upperload1 0
load 3 0.0 $upperload1 0
load 4 0.0 $upperload2 0
load 5 0.0 $upperload2 0
load 6 0.0 $upperload2 0
load 7 0.0 $upperload1 0
load 8 0.0 $upperload1 0
load 9 0.0 $upperload1 0

load 10 0.0 $download3 0
load 11 0.0 $download3 0
load 12 0.0 $download3 0
load 13 0.0 $download3 0
load 14 0.0 $download3 0
load 15 0.0 $download3 0
}





uniaxialMaterial Concrete01  1     -27588.5    -0.002      0.0      -0.008
                                   

uniaxialMaterial Concrete01  2     -34485.6    -0.004     -20691.4  -0.014


uniaxialMaterial Hardening   3      2.0e8       248200.          0.0         1.6129e6 





uniaxialMaterial Concrete01  4     -27588.5     -0.002      0.0      -0.008
                                    


uniaxialMaterial Concrete01  5     -34485.6     -0.004    -20691.4   -0.014



uniaxialMaterial Hardening   6      2.0e8       248200.          0.0         1.6129e6 




section Fiber  1 {
   patch quad  2    1   12 -0.2500  0.2000 -0.2500 -0.2000  0.2500 -0.2000  0.2500  0.2000
   patch quad  1    1   14 -0.3000 -0.2000 -0.3000 -0.2500  0.3000 -0.2500  0.3000 -0.2000
   patch quad  1    1   14 -0.3000  0.2500 -0.3000  0.2000  0.3000  0.2000  0.3000  0.2500
   patch quad  1    1    2 -0.3000  0.2000 -0.3000 -0.2000 -0.2500 -0.2000 -0.2500  0.2000
   patch quad  1    1    2  0.2500  0.2000  0.2500 -0.2000  0.3000 -0.2000  0.3000  0.2000
   layer straight  3    3   0.000645 -0.2000   0.2000    -0.2000   -0.2000
   layer straight  3    3   0.000645  0.2000   0.2000     0.2000   -0.2000
}


section Fiber  2 {
   patch quad 2   1   10    -0.2000  0.2000 -0.2000 -0.2000  0.2000 -0.2000  0.2000  0.2000
   patch quad 1   1   12    -0.2500 -0.2000 -0.2500 -0.2500  0.2500 -0.2500  0.2500 -0.2000
   patch quad 1   1   12    -0.2500  0.2500 -0.2500  0.2000  0.2500  0.2000  0.2500  0.2500
   patch quad 1   1    2    -0.2500  0.2000 -0.2500 -0.2000 -0.2000 -0.2000 -0.2000  0.2000
   patch quad 1   1    2     0.2000  0.2000  0.2000 -0.2000  0.2500 -0.2000  0.2500  0.2000
   layer straight 3    3   0.00051  -0.2000 0.2000 -0.2000 -0.2000
   layer straight 3    3   0.00051   0.2000 0.2000  0.2000 -0.2000
}


section Fiber  3 {
   patch quad 1  1     12   -0.2500   0.2000  -0.2500  -0.2000  0.2500  -0.2000  0.2500  0.2000
   layer straight 3    2    0.000645 -0.2000   0.2000    -0.2000   -0.2000
   layer straight 3    2    0.000645  0.2000   0.2000     0.2000   -0.2000
}



section Fiber  4 {
   patch quad  5    1   12 -0.2500  0.2000 -0.2500 -0.2000  0.2500 -0.2000  0.2500  0.2000
   patch quad  4    1   14 -0.3000 -0.2000 -0.3000 -0.2500  0.3000 -0.2500  0.3000 -0.2000
   patch quad  4    1   14 -0.3000  0.2500 -0.3000  0.2000  0.3000  0.2000  0.3000  0.2500
   patch quad  4    1    2 -0.3000  0.2000 -0.3000 -0.2000 -0.2500 -0.2000 -0.2500  0.2000
   patch quad  4    1    2  0.2500  0.2000  0.2500 -0.2000  0.3000 -0.2000  0.3000  0.2000
   layer straight  6    3   0.000645 -0.2000   0.2000    -0.2000   -0.2000
   layer straight  6    3   0.000645  0.2000   0.2000     0.2000   -0.2000
}





section Fiber  5 {
   patch quad 5   1   10    -0.2000  0.2000 -0.2000 -0.2000  0.2000 -0.2000  0.2000  0.2000
   patch quad 4   1   12    -0.2500 -0.2000 -0.2500 -0.2500  0.2500 -0.2500  0.2500 -0.2000
   patch quad 4   1   12    -0.2500  0.2500 -0.2500  0.2000  0.2500  0.2000  0.2500  0.2500
   patch quad 4   1    2    -0.2500  0.2000 -0.2500 -0.2000 -0.2000 -0.2000 -0.2000  0.2000
   patch quad 4   1    2     0.2000  0.2000  0.2000 -0.2000  0.2500 -0.2000  0.2500  0.2000
   layer straight 6    3   0.00051  -0.2000 0.2000 -0.2000 -0.2000
   layer straight 6    3   0.00051   0.2000 0.2000  0.2000 -0.2000
}


#
# -----------------------------------------------------------------------------------------------------

set nP 4

geomTransf Linear 1


element dispBeamColumn  1   1   2    $nP   2      1
element dispBeamColumn  2   2   3    $nP   2      1
element dispBeamColumn  3   4   5    $nP   1      1
element dispBeamColumn  4   5   6    $nP   1      1
element dispBeamColumn  5   7   8    $nP   2      1
element dispBeamColumn  6   8   9    $nP   2      1


element dispBeamColumn  7   2   5    $nP   3      1
element dispBeamColumn  8   5   8    $nP   3      1
element dispBeamColumn  9   3   6    $nP   3      1
element dispBeamColumn 10   6   9    $nP   3      1


element dispBeamColumn 11  10  11    $nP   4      1
element dispBeamColumn 12  11   1    $nP   4      1

element dispBeamColumn 13  12  13    $nP   5      1
element dispBeamColumn 14  13   4    $nP   5      1

element dispBeamColumn 15  14  15    $nP   4      1
element dispBeamColumn 16  15   7    $nP   4      1




recorder Element  -ele 1 2  -file Deformation12.out -time section 2 deformations
recorder Element  -ele 1 2  -file Force12.out -time section 2 force

recorder Element  -ele 3 4  -file Deformation34.out -time section 2 deformations
recorder Element  -ele 3 4  -file Force34.out -time section 2 force

recorder Element  -ele  7 9 -file Deformation79.out -time section 3 deformations
recorder Element  -ele  7 9 -file Force79.out -time section 3 force



recorder Element -ele 7 -time -file steelstress7.out  section 3 fiber -0.2286 0.2286 stress
recorder Element  -ele 7 -time -file steelstrain7.out section 3 fiber -0.2286 0.2286  strain

recorder Element  -ele 7 -time -file concretestress7.out  section 3 fiber 0.0 0.0 stress
recorder Element  -ele 7 -time -file concretestrain7.out section 3 fiber 0.0 0.0  strain

 



set g -19.6
model basic -ndm 2 -ndf 2



node 16    -9.2      -7.2
node 17    -7.2      -7.2
node 18    -5.2      -7.2
node 19    -3.2      -7.2
node 20    -1.2      -7.2
node 21     0.0      -7.2
node 22     1.2      -7.2
node 23     3.5      -7.2
node 24     5.8      -7.2
node 25     7.0      -7.2
node 26     8.2      -7.2
node 27    10.5      -7.2
node 28    12.8      -7.2
node 29    14.0      -7.2
node 30    15.2      -7.2
node 31    17.2      -7.2
node 32    19.2      -7.2
node 33    21.2      -7.2
node 34    23.2      -7.2

node 35    -9.2      -4.8
node 36    -7.2      -4.8
node 37    -5.2      -4.8
node 38    -3.2      -4.8
node 39    -1.2      -4.8
node 40     0.0      -4.8
node 41     1.2      -4.8
node 42     3.5      -4.8
node 43     5.8      -4.8
node 44     7.0      -4.8
node 45     8.2      -4.8
node 46    10.5      -4.8
node 47    12.8      -4.8
node 48    14.0      -4.8
node 49    15.2      -4.8
node 50    17.2      -4.8
node 51    19.2      -4.8
node 52    21.2      -4.8
node 53    23.2      -4.8

node 54    -9.2      -2.4
node 55    -7.2      -2.4
node 56    -5.2      -2.4
node 57    -3.2      -2.4
node 58    -1.2      -2.4
node 59     0.0      -2.4
node 60     1.2      -2.4
node 61     3.5      -2.4
node 62     5.8      -2.4
node 63     7.0      -2.4
node 64     8.2      -2.4
node 65    10.5      -2.4
node 66    12.8      -2.4
node 67    14.0      -2.4
node 68    15.2      -2.4
node 69    17.2      -2.4
node 70    19.2      -2.4
node 71    21.2      -2.4
node 72    23.2      -2.4


node 73    -9.2      -1.2
node 74    -7.2      -1.2
node 75    -5.2      -1.2
node 76    -3.2      -1.2
node 77    -1.2      -1.2
node 78     0.0      -1.2
node 79     1.2      -1.2
node 80     3.5      -1.2
node 81     5.8      -1.2
node 82     7.0      -1.2
node 83     8.2      -1.2
node 84    10.5      -1.2
node 85    12.8      -1.2
node 86    14.0      -1.2
node 87    15.2      -1.2
node 88    17.2      -1.2
node 89    19.2      -1.2
node 90    21.2      -1.2
node 91    23.2      -1.2

node 92    -9.2      0
node 93    -7.2      0
node 94    -5.2      0
node 95    -3.2      0
node 96    -1.2      0
node 97     0.0      0
node 98     1.2      0
node 99     3.5      0
node 100    5.8      0
node 101    7.0      0
node 102    8.2      0
node 103   10.5      0
node 104   12.8      0
node 105   14.0      0
node 106   15.2      0
node 107   17.2      0
node 108   19.2      0
node 109   21.2      0
node 110   23.2      0




fix 16 1 1
fix 17 1 1
fix 18 1 1
fix 19 1 1
fix 20 1 1
fix 21 1 1
fix 22 1 1
fix 23 1 1
fix 24 1 1
fix 25 1 1
fix 26 1 1
fix 27 1 1
fix 28 1 1
fix 29 1 1
fix 30 1 1
fix 31 1 1
fix 32 1 1
fix 33 1 1
fix 34 1 1

 



nDMaterial MultiYieldSurfaceClay   101   2       0.0         54450	1.6e5     33.           .1          
nDMaterial MultiYieldSurfaceClay   102   2       0.0         33800	1.0e5     26.           .1          
nDMaterial MultiYieldSurfaceClay   103   2       0.0         61250	1.8e5     35.           .1    
nDMaterial MultiYieldSurfaceClay   104   2       0.0         96800	2.9e5     44.           .1   





 
nDMaterial MultiYieldSurfaceClay   100   2       0.0          2e7	1.0e6    21000.  50.0     0 100 0   2

element quadWithSensitivity  17   16   17   36   35   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  18   17   18   37   36   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  19   18   19   38   37   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  20   19   20   39   38   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  21   20   21   40   39   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  22   21   22   41   40   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  23   22   23   42   41   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  24   23   24   43   42   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  25   24   25   44   43   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  26   25   26   45   44   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  27   26   27   46   45   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  28   27   28   47   46   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  29   28   29   48   47   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  30   29   30   49   48   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  31   30   31   50   49   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  32   31   32   51   50   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  33   32   33   52   51   0.60     "PlaneStrain" 104     0       2.0        0  $g
element quadWithSensitivity  34   33   34   53   52   0.60     "PlaneStrain" 104     0       2.0        0  $g


element quadWithSensitivity  35   35   36   55   54   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  36   36   37   56   55   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  37   37   38   57   56   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  38   38   39   58   57   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  39   39   40   59   58   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  40   40   41   60   59   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  41   41   42   61   60   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  42   42   43   62   61   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  43   43   44   63   62   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  44   44   45   64   63   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  45   45   46   65   64   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  46   46   47   66   65   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  47   47   48   67   66   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  48   48   49   68   67   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  49   49   50   69   68   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  50   50   51   70   69   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  51   51   52   71   70   0.60     "PlaneStrain" 103     0       2.0        0  $g
element quadWithSensitivity  52   52   53   72   71   0.60     "PlaneStrain" 103     0       2.0        0  $g


element quadWithSensitivity  53   54   55   74   73   0.60     "PlaneStrain" 102     0       2.0        0  $g
element quadWithSensitivity  54   55   56   75   74   0.60     "PlaneStrain" 102     0       2.0        0  $g
element quadWithSensitivity  55   56   57   76   75   0.60     "PlaneStrain" 102     0       2.0        0  $g
element quadWithSensitivity  56   57   58   77   76   0.60     "PlaneStrain" 102     0       2.0        0  $g
  
element quadWithSensitivity  57   58   59   78   77   0.60     "PlaneStrain" 100     0       2.0        0  $g
element quadWithSensitivity  58   59   60   79   78   0.60     "PlaneStrain" 100     0       2.0        0  $g

element quadWithSensitivity  59   60   61   80   79   0.60     "PlaneStrain" 102     0       2.0        0  $g
element quadWithSensitivity  60   61   62   81   80   0.60     "PlaneStrain" 102     0       2.0        0  $g

element quadWithSensitivity  61   62   63   82   81   0.60     "PlaneStrain" 100     0       2.0        0  $g
element quadWithSensitivity  62   63   64   83   82   0.60     "PlaneStrain" 100     0       2.0        0  $g

element quadWithSensitivity  63   64   65   84   83   0.60     "PlaneStrain" 102     0       2.0        0  $g
element quadWithSensitivity  64   65   66   85   84   0.60     "PlaneStrain" 102     0       2.0        0  $g
   
element quadWithSensitivity  65   66   67   86   85   0.60     "PlaneStrain" 100     0       2.0        0  $g
element quadWithSensitivity  66   67   68   87   86   0.60     "PlaneStrain" 100     0       2.0        0  $g

element quadWithSensitivity  67   68   69   88   87   0.60     "PlaneStrain" 102     0       2.0        0  $g
element quadWithSensitivity  68   69   70   89   88   0.60     "PlaneStrain" 102     0       2.0        0  $g
element quadWithSensitivity  69   70   71   90   89   0.60     "PlaneStrain" 102     0       2.0        0  $g
element quadWithSensitivity  70   71   72   91   90   0.60     "PlaneStrain" 102     0       2.0        0  $g

element quadWithSensitivity  71   73   74   93   92   0.60     "PlaneStrain" 101     0       2.0        0  $g
element quadWithSensitivity  72   74   75   94   93   0.60     "PlaneStrain" 101     0       2.0        0  $g
element quadWithSensitivity  73   75   76   95   94   0.60     "PlaneStrain" 101     0       2.0        0  $g
element quadWithSensitivity  74   76   77   96   95   0.60     "PlaneStrain" 101     0       2.0        0  $g

element quadWithSensitivity  75   77   78   97   96   0.60     "PlaneStrain" 100     0       2.0        0  $g
element quadWithSensitivity  76   78   79   98   97   0.60     "PlaneStrain" 100     0       2.0        0  $g

element quadWithSensitivity  77   79   80   99   98   0.60     "PlaneStrain" 101     0       2.0        0  $g
element quadWithSensitivity  78   80   81  100   99   0.60     "PlaneStrain" 101     0       2.0        0  $g

element quadWithSensitivity  79   81   82  101  100   0.60     "PlaneStrain" 100     0       2.0        0  $g
element quadWithSensitivity  80   82   83  102  101   0.60     "PlaneStrain" 100     0       2.0        0  $g

element quadWithSensitivity  81   83   84  103  102   0.60     "PlaneStrain" 101     0       2.0        0  $g
element quadWithSensitivity  82   84   85  104  103   0.60     "PlaneStrain" 101     0       2.0        0  $g

element quadWithSensitivity  83   85   86  105  104   0.60     "PlaneStrain" 100     0       2.0        0  $g
element quadWithSensitivity  84   86   87  106  105   0.60     "PlaneStrain" 100     0       2.0        0  $g

element quadWithSensitivity  85   87   88  107  106   0.60     "PlaneStrain" 101     0       2.0        0  $g
element quadWithSensitivity  86   88   89  108  107   0.60     "PlaneStrain" 101     0       2.0        0  $g
element quadWithSensitivity  87   89   90  109  108   0.60     "PlaneStrain" 101     0       2.0        0  $g
element quadWithSensitivity  88   90   91  110  109   0.60     "PlaneStrain" 101     0       2.0        0  $g



 
equalDOF  16 34 1 2
equalDOF  35 53 1 2
equalDOF  54 72 1 2
equalDOF  73 91 1 2
equalDOF  92 110 1 2

equalDOF   1  97 1 2
equalDOF  11  78 1 2
equalDOF  10  59 1 2
equalDOF   4 101 1 2
equalDOF  13  82 1 2
equalDOF  12  63 1 2
equalDOF   7 105 1 2
equalDOF  15  86 1 2
equalDOF  14  67 1 2


 
 
foreach theNode { 6 5 4 13 12 99 80 61 42 23} {
    
    recorder Node -file node$theNode.out -time -node $theNode -dof 1 2 disp 
        
}



 


 
recorder Element -ele 23 -time -file stress23.out -time   material 2 stress 
recorder Element -ele 41 -time -file stress41.out -time   material 2 stress 
recorder Element -ele 59 -time -file stress59.out -time   material 2 stress 
recorder Element -ele 77 -time -file stress77.out -time   material 2 stress 

recorder Element -ele 37 -time -file stress37.out -time   material 2 stress 
recorder Element -ele 37 -time -file strain37.out -time   material 2 strain 



constraints Transformation
numberer RCM
test NormDispIncr 1.E-6 25  2
integrator LoadControl 1 1 1 1
algorithm Newton
system BandGeneral

 

analysis Static 
analyze 3
 
puts "soil gravity nonlinear analysis completed ..."


wipeAnalysis

constraints Transformation
test NormDispIncr 1.E-6 25  2
algorithm Newton
numberer RCM
system BandGeneral

integrator Newmark  0.55 0.275625
 
 analysis Transient

set startT [clock seconds]


pattern UniformExcitation    1     1    -accel "Series -factor 3 -filePath elcentro.txt -dt 0.01"
analyze 2400 0.005

set endT [clock seconds]









