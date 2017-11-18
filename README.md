# eclipse_j2ee
A Docker build of __Eclipse for Java 2 EE Developers__ accessible via [xpra](https://xpra.org/).

## Features
* The build checks the sha512 signature of the eclipse download to ensure the download mirror hasn't been compromised.
* The eclipse process won't start until an xpra client attaches.  This keeps DPI sane, which is especially important if you have a HighDPI monitor.

## Recommended Usage
1. Start the container.
	```bash
	$ docker run --rm -it -p 127.0.0.1:9999:9999 -v eclipse:/opt/eclipse -v ~/workspace:/opt/workspace aronahl/eclipse_j2ee
	```
	* The eclipse install will be copied to the eclipse volume.
		* If no eclipse volume exists, it will be created and filled with a copy of eclipse from the image.
		* You'll want to keep the eclipse volume around to persist any updates or package installs between runs.
	* The workspace will exist in a local workspace subdir of your home directory.

2. Attach to tcp:localhost:9999 with an xpra client.


## Alternative Usage With HTML5 Client

1. Start the container.
	```bash
	$ docker run --rm -it -p 127.0.0.1:9999:9999 -e HTTP=1 -v eclipse:/opt/eclipse -v ~/workspace:/opt/workspace aronahl/eclipse_j2ee
	```
	* The eclipse install will be copied to the eclipse volume.
		* If no eclipse volume exists, it will be created and filled with a copy of eclipse from the image.
		* You'll want to keep the eclipse volume around to persist any updates or package installs between runs.
	* The workspace will exist in a local workspace subdir of your home directory.

2. Browse to http://127.0.0.1:9999
3. Reloading the page can help with resizing the workspace and making maximize match your browser window size.
4. Popups will hide behind the main eclipse window.  Use the maximize/roll-up button to get to them.