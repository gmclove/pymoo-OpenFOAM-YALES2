################### blockMeshDic Structure ##################################
# blockMeshDic Header
diff_bMD1 = """
/*--------------------------------*- C++ -*----------------------------------*\
| =========                 |                                                 |
| \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\    /   O peration     | Version:  5                                     |
|   \\  /    A nd           | Web:      www.OpenFOAM.org                      |
|    \\/     M anipulation  |                                                 |
\*---------------------------------------------------------------------------*/
FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}
// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
"""

# Body
diff_bMD2 = """
z1  0.0; 
z2  0.1; 
Nup   110;
Nuu   90;
Ncowl 20;
Naxis 200;
Ninf  140;
Nramp 300;
Ndown 400;

convertToMeters 1;

vertices
(
    (1.0	0.0		$z1) // Point 0
    (2.0	0.0		$z1) // Point 1
    ($DLcO	$LsO	$z1) // Point 2
    ($TLcO	0.1		$z1) // Point 3
    (1.0	0.8		$z1) // Point 4
    (2.0	0.8		$z1) // Point 5
    ($DLcO	0.8		$z1) // Point 6
    ($TLcO	0.8		$z1) // Point 7
    (1.0	0.85	$z1) // Point 8
    (2.0	0.85	$z1) // Point 9
    ($ULcO	0.85	$z1) // Point 10
    ($TLcO	0.85	$z1) // Point 11
    (1.0	2.5   	$z1) // Point 12
    (2.0	2.5	    $z1) // Point 13
    ($ULcO	2.5	    $z1) // Point 14
    ($TLcO	2.5	    $z1) // Point 15

    (1.0	0.0		$z2) // Point 16
    (2.0	0.0		$z2) // Point 17
    ($DLcO	$LsO	$z2) // Point 18
    ($TLcO	0.1		$z2) // Point 19
    (1.0	0.8		$z2) // Point 20
    (2.0	0.8		$z2) // Point 21
    ($DLcO	0.8		$z2) // Point 22
    ($TLcO	0.8		$z2) // Point 23
    (1.0	0.85	$z2) // Point 24
    (2.0	0.85	$z2) // Point 25
    ($ULcO	0.85	$z2) // Point 26
    ($TLcO	0.85	$z2) // Point 27
    (1.0	2.5   	$z2) // Point 28
    (2.0	2.5     $z2) // Point 29
    ($ULcO	2.5	    $z2) // Point 30
    ($TLcO	2.5	    $z2) // Point 31
);

blocks
(
    //block 0
    hex (0 1 5 4 16 17 21 20) ($Ninf $Naxis 1) simpleGrading
    (
        0.27
        (
            (0.10		0.15	1)
            (0.40		0.35	3.2)
            (0.40		0.35	0.3125)
            (0.10		0.15	1)
        )   	
        1
    )    
    //block 1
    hex (1 2 6 5 17 18 22 21) ($Nramp $Naxis 1) simpleGrading
    (
        1
        (
            (0.10		0.15	1)
            (0.40		0.35	3.2)
            (0.40		0.35	0.3125)
            (0.10		0.15	1)
        )   	
        1
    )
    //block 2
    hex (2 3 7 6 18 19 23 22) ($Ndown $Naxis 1) simpleGrading 		
    (
        (
            (0.50       0.50    3.125)
            (0.50       0.50    0.32)
        )
        (
            (0.10		0.15	1)
            (0.40		0.35	3.2)
            (0.40		0.35	0.3125)
            (0.10		0.15	1)
        )   	
        1
    )
    //block 3
    hex (4 5 9 8 20 21 25 24) ($Ninf $Ncowl 1) simpleGrading (0.27 1 1)
    //block 4
    hex (5 6 10 9 21 22 26 25) ($Nramp $Ncowl 1) simpleGrading (1 1 1)
    //block 5
    hex (8 9 13 12 24 25 29 28) ($Ninf $Nup 1) simpleGrading (0.27 30 1)
    //block 6
    hex (9 10 14 13 25 26 30 29) ($Nramp $Nup 1) simpleGrading (1 30 1)
    //block 7
    hex (10 11 15 14 26 27 31 30) ($Nuu $Nup 1) simpleGrading 
    (
        (
            (0.20       0.6    4)
            (0.80       0.4    1)
        )
        30       
        1
    )
);

edges
("""

# End
diff_bMD3 = """
);

boundary
(
    inlet
    {
        type patch;
        faces
        (
            (12 28 24 8)
            (8 24 20 4)
            (4 20 16 0)
        );
    }   

    outlet
    {
        type patch;
        faces
        (
            (31 15 11 27)
        );
    }   

    compressor
    {
        type patch;
        faces
        (
            (23 7 3 19)
        );
    }   

    upper
    {
        type patch;
        faces
        (
            (28 12 13 29)
            (29 13 14 30)
            (30 14 15 31)
        );
    }   

    lower
    {
        type patch;
        faces
        (
            (0 16 17 1)
        );
    }   

    cowl
    {
        type wall;
        faces
        (
            (10 26 27 11)
            (26 10 6 22)
            (22 6 7 23)
        );
    }   

    axis
    {
        type wall;
        faces
        (
            (18 2 1 17)
            (19 3 2 18)
        );
    }   
);

// ************************************************************************* //
"""