# PiConfigurationTool
 Software to Flash Pi's with metering software
   
   (C) Pralish Satyal 2023

    A program to implement all class functions to create the 
    configuration tool for flashing a Raspberry Pi 4 with PiMeter
    specific data. This includes a specific OpenVPN OPVN file,
    a script specific based on this filename,
    MQTT Connection details, global azure-cert.pem (this is usually the same),
    and a connection_details.json file which is what the user parses in as a file.

    PiMeter should read data from the connection_details.json file. 

    We should ask the user where they want to install PiMeter. After this, statically fill the 
    Azure_Connection folder with where it should actually go and fill files in this directory.

    For any information, contact Pralish Satyal

    pralishbusiness@gmail.com
    www.pralish.com
