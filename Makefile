ifeq ($(VERSION),)
	FILENAME = nanny_1.0.0.0
else
	FILENAME = nanny_$(VERSION)
endif

release:
	make release-deb

release-deb:
	sed -e "s|VERSION|$VERSION|" ./Packaging/debian/DEBIAN/control.txt > ./Packaging/debian/DEBIAN/control
	cat ./Packaging/debian/DEBIAN/control
	dotnet publish Nanny.Console/Nanny.Console.csproj -c Release --self-contained -r ubuntu.20.04-x64 -o Packaging/debian/opt/kolenkainc/nanny
	cp -R Packaging/debian $(FILENAME)
	dpkg-deb --build $(FILENAME)
	rm -rf $(FILENAME)

release-brew:
	dotnet publish Nanny.Console/Nanny.Console.csproj -c Release --self-contained -r osx.10.12-x64 -o Packaging/brew
