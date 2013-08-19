ni results -type directory -Force
rm results\* -Recurse -Force
foreach ($x in "1a","1g","2a1","2a2","2b","2c","2d","2e1","2e2","2e3","2e4","2e5","2f","3b","3c","3d","3e","3f","3g1","3g2")
{
	cd $x
	7z a ..\results\$x.zip *txt
	cd ..
}