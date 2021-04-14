# spra_group_project
This document describes how to set up and execute our spra group assignment.

# 0. Get/ update files

The following command is only required once. Execute the following command in a terminal to connect to the repository. It will create a new folder with all the files.
```shell
git clone https://github.com/stffnwhlrs/spra_group_project.git
```

Before running the application you should make sure that the code is up to date and download all updated files. Use the following command to do it.
```shell 
git pull 
```

# 1. Set up Kafka
Run the bash script `setup_kafka_env.sh` to start the Kafka environment and create the needed topics if they don't exist.
```shell
sudo bash setup.sh
```