ifeq ($(RELEASE_NUMBER),)
	VERSION = 1.0-0
else
	VERSION = $(RELEASE_NUMBER)
endif

release:
	dotnet publish Nanny.Console/Nanny.Console.csproj -c Release --self-contained -r ubuntu.20.04-x64 -o debian_template/opt/kolenkainc/nanny
	cp -R debian_template nanny_$(VERSION)
	dpkg-deb --build nanny_$(VERSION)
	rm -rf nanny_$(VERSION)
