release:
	dotnet publish Nanny.Console/Nanny.Console.csproj -c Release --self-contained -r ubuntu.20.04-x64 -o debian_template/opt/kolenkainc/nanny

debianize:
	cp -R debian_template nanny_1.0-1
	dpkg-deb --build nanny_1.0-1
	rm -rf nanny_1.0-1
