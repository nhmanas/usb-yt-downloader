Step-by-Step Guide to Triggering a USB Plug Event and Executing a Script on Debian 11 using udev and Systemd:

1. **Write the Python Script:**
   - Begin by creating a Python script (e.g., `yt.py`) that downloads videos and converts them to MP3 files according to your requirements.

2. **Create a Virtual Environment (Optional):**
   - Consider creating a virtual environment (venv) to isolate Python dependencies for the script. This ensures that required packages (such as `pytube`, `moviepy`, etc.) are installed within the venv and do not interfere with system-wide Python packages.

3. **Test the Python Script:**
   - Before integrating the script with udev, it's essential to test the Python script manually to confirm that it functions as intended. This step helps identify and resolve any issues or errors in the script.

4. **Identify USB Device Information:**
   - Plug in the USB flash drive and run the following command to gather information about the USB device:
   
      ```
      udevadm info -a /dev/sdb1
      ```


5. **Create the udev Rule:**
   - Create a udev rule file (e.g., `/etc/udev/rules.d/99-custom.rules`) with the following content:

     ```
     ACTION=="add", SUBSYSTEM=="usb", KERNEL=="sdb1", TAG+="systemd", ENV{SYSTEMD_WANTS}+="custom_script.service"
     ```

   - This rule instructs udev to trigger the `custom_script.service` whenever a USB device with the kernel name `sdb1` (your USB flash drive) is added.

6. **Create the Systemd Service:**
   - Create a Systemd service file (e.g., `/etc/systemd/system/custom_script.service`) with the following content:

     ```
      [Unit]
      Description=Custom Script Service
      After=media-yourusername-yourusbname.mount

      [Service]
      Type=oneshot
      ExecStart=/path/to/your/script.sh

      [Install]
      WantedBy=media-yourusername-yourusbname.mount

     ```

   - This Systemd service is responsible for executing the `ytstart.sh` script when triggered by the udev rule. It specifies that the service should be executed after the mount point (`media-yourusername-yourusbname.mount`) is activated.

7. **Create the Shell Script (ytstart.sh):**
   - Write a shell script (e.g., `script.sh`) that sets up the virtual environment (if applicable), activates it, runs the Python script (`yt.py`), and deactivates the virtual environment.

8. **Make Shell Script Executable:**
   - Make the shell script executable using the chmod command:

     ```
     chmod +x /path/to/your/script.sh
     ```

9. **Reload udev Rules:**
   - Reload the udev rules to apply the changes:

     ```
     udevadm control --reload-rules
     sudo systemctl restart systemd-udevd
     
     ```

10. **Test the Setup:**
   - Finally, test the setup by plugging in the USB flash drive and monitoring log files (e.g., `/tmp/your_debug.log` and `/tmp/your_python_version.log`) to ensure that the Python script is executed successfully.

Following these steps will allow the Python script to be automatically triggered when a USB flash drive is plugged in, and it will carry out its designated tasks on the device.
