ifeq ($(PACKAGE_FILENAME_WITHOUT_EXTENSION),)
	FILENAME = nanny_1.0-0
else
	FILENAME = $(PACKAGE_FILENAME_WITHOUT_EXTENSION)
endif

release:
	dotnet publish Nanny.Console/Nanny.Console.csproj -c Release --self-contained -r ubuntu.20.04-x64 -o debian_template/opt/kolenkainc/nanny
	cp -R debian_template $(FILENAME)
	dpkg-deb --build $(FILENAME)
	rm -rf $(FILENAME)
