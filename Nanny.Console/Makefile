release:
	dotnet publish -c Release --self-contained -r ubuntu.20.04-x64 -o ../nanny_1.0-1/opt/kolenkainc/nanny

debianize:
	dpkg-deb --build nanny_1.0-1

