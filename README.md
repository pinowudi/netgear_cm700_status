# Netgear CM700 Cable Modem DOCSIS Status Scraper
## Purpose
This code scrapes the DocsysStatus.htm page of the CM700 web administration address. This may be useful for scheduling regular collection and monitoring of status to help troubleshoot negotiation, reset, and power issues with cable provider support staff. Target use for the script to feed a log collector.

## A note on security
These devices have a small embedded linux on board and an exposed web adminsitration interface on a staticly-routed default IP address. This makes the devices an easy target for javascript redirects from web pages looking to pwn devices configured with default credentials. I recommend changing the default credentials of your cable modem as soon as possible. [Do so for this model](http://admin:password@192.168.100.1/SetPassword.htm "Reset CM700 Password")

# Configuation

## Create a pipenv environment
Make sure pipenv is installed and has the dependent libraries.

```shell
$ pip install --user pipenv
$ pipenv install requests config
```

## Cable modem settings
The default address and credentials for the CM700 are provided in the `config.py.default` file. Just copy it to `config.py` and adjust the address and password to fit your configuation.
```python
NETGEAR_URL='http://192.168.100.1/DocsisStatus.htm'
USERNAME='admin'
PASSWORD='password'
```

## Splunk settings
In addition to JSON output to STDOUT, there is also a Splunk HTTP Event Collector output provided based on [George Starcher's Splunk-Class-httpevent module](https://github.com/georgestarcher/Splunk-Class-httpevent.git). Be sure to add that as a dependency if using this module. To enable, you have to set up [Splunk HTTP Event Collector](http://docs.splunk.com/Documentation/Splunk/latest/Data/AboutHEC) and define the following variables in config.py.
```
SPLUNK_HEC_KEY='fill_token_provided_by_HEC_setup'
SPLUNK_HEC_HOST='fill_splunk_ip_or_hostname'
SPLUNK_HEC_INDEX='index_this_is_going_to'
SPLUNK_EVENT_HOST='my_local_hostname'
```

## Set up first run
```shell
$ cp config.py.default config.py
[ edit config.py with credentials]
$ pipenv run python ngcm700_status.py
```

The `launch.sh` script has been provided to help wrap the initiation of the pipenv environment. 

# Output
Output will be a JSON dump of the parsed configuraiton settings from the DocsisStatus.htm page of the cable modem. 

Example:
```json
{
    "bios": {
        "0": {
            "acquire_ds_channel_comment": "Locked", 
            "acquire_ds_channel_status": "813000000", 
            "boot_state_comment": "Operational", 
            "boot_state_status": "Ok", 
            "configuration_file_comment": "^1/A7520309/126/001", 
            "configuration_file_status": "Ok", 
            "connectivity_state_comment": "Operational", 
            "connectivity_state_status": "Ok", 
            "current_system_time": "Sun Oct  1 18:05:48 2017", 
            "downstream_bonded_channels_partials": "0", 
            "ip_prov_mode_comment": "honorMdd(4)", 
            "ip_prov_mode_status": "Honor MDD", 
            "provision_mode": "0", 
            "security_comment": "BPI+", 
            "security_status": "Enabled", 
            "startup_freq": "", 
            "upstream_bonded_channels_partials": "0"
        }
    }, 
    "downstream": {
        "1": {
            "SNR": "37.6", 
            "channel": "1", 
            "channel_id": "1", 
            "correctables": "6756", 
            "frequency": "771000000 Hz", 
            "lock_status": "Locked", 
            "modulation": "QAM 256", 
            "power": "-4.0", 
            "uncorrectables": "30272"
        }, 
        "2": {
            "SNR": "37.3", 
            "channel": "2", 
            "channel_id": "2", 
            "correctables": "334765", 
            "frequency": "777000000 Hz", 
            "lock_status": "Locked", 
            "modulation": "QAM 256", 
            "power": "-4.2", 
            "uncorrectables": "2242283"
        }, 
...
        "32": {
            "SNR": "0.0", 
            "channel": "32", 
            "channel_id": "N/A", 
            "correctables": "0", 
            "frequency": "0 Hz", 
            "lock_status": "Not Locked", 
            "modulation": "N/A", 
            "power": "0.0", 
            "uncorrectables": "0"
        }
    }, 
    "upstream": {
        "1": {
            "channel": "1", 
            "channel_id": "1", 
            "channel_type": "TDMA_and_ATDMA", 
            "frequency": "17154000 Hz", 
            "lock_status": "Locked", 
            "power": "40.0", 
            "symbol_rate": "2560"
        }, 
        "2": {
            "channel": "2", 
            "channel_id": "2", 
            "channel_type": "ATDMA", 
            "frequency": "21984000 Hz", 
            "lock_status": "Locked", 
            "power": "39.5", 
            "symbol_rate": "5120"
...
        }
    }
}

```

## License
This code is licensed under the MIT license.
