# Protect_Your_App_From_Stealing
The following code "binds" the computer's hardware to the application, ensuring that if the application is installed on a different computer, authentication cannot be performed, and the application will not run.

The process consists of two parts:

1. The first part involves an application called "Activator," which must be run with administrator privileges. This application accesses the C: drive and creates a `configuration.txt` file, where it writes three lines of data: the MAC address of the Ethernet adapter, the MAC address of the Wi-Fi adapter, and the serial number of the first hard drive, all hashed using SHA-256.

2. In the second part, within the main application, the same code is executed, but instead of writing the data to a `.txt` file, it compares the current hardware information with the data stored in the `configuration.txt` file. If at least one of the three values matches, the application is allowed to run.
