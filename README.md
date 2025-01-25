Office Activator
================

These are the currenlty supported Office versions this product can activate

### Office

- LTSC Standard 2024
- LTSC Professional Plus 2024
- LTSC Standard 2021
- LTSC Professional Plus 2021
- Standard 2019
- Professional Plus 2019

#### How to order the versions

Each XML file in `/website/xml/` contains a 2 digit number at the start example `01Office Standard 2019.xml` that will be order the item will be listed in the `/client/main.py` Activation and Installation.

#### Host your own Office files

The `/website/versions/` directory contains office installations if you want to install office from your own website. To download a specific versions use the `/website/setup.exe` file and as an `Administrator` run the command `setup.exe /download version.xml` and then upload the selected version to `/website/versions/`. Each verison takes about 2-5 GB of storage.


---



### How to setup your website

**System Requirements**

- **PHP Version**: >= 5.3
- **PHP Extensions**:
  - **SimpleXML** enabled
  - **JSON** enabled
  - **mbstring** enabled
- **Storage**:
  - **15GB** recommended if hosting your own Office files this is for about 6 installations.
  - **20MB** recommended if just going to host xml files.

By default the python script will look for `yourdomain.com/kms/office/` if you want to change this edit line `8` in the file `/client/main.py` by changing `r`.

```python
def setup(h="http://au.ldtp.com",kh="au.ldtp.com",r="/kms/office"):
```

Also set  `h` and `kh` to your domain and KMS server. Include `https://` or `http://` for `h`.

In the `/website/index.php` file change line `2` include a `/` at the start and the end.

```php
$root = "/kms/office/versions/"
```

These are all the prameters and what they do in the `/website/idndex.php` file.


|  Parameter  |                      Action                      | Required |                      Example                      |
| :-----------: | :------------------------------------------------: | :--------: | :--------------------------------------------------: |
|    ?id=    |         Gets the key for the selected ID         |    ✓    |      ?id=Office%20Professional%20Plus%202019      |
|   &hosted   |           Returns true/false if hosted           |    x    |   ?id=Office%20Professional%20Plus%202019&hosted   |
|    &xml    |               Return the XML file               |    x    |    ?id=Office%20Professional%20Plus%202019&xml    |
| &xml&hosted | If hosted, returns XML with self-hosted settings |    x    | ?id=Office%20Professional%20Plus%202019&xml&hosted |

---


### Want to host your own KMS Server?

If you would like to host your own KMS server visit https://au.ldtp.com/kms/server/ and follow the instructions
When running the client make sure it is run as an administrator otherwise it will fail activation and installation.
###
Thanks to [@Wind4](https://github.com/Wind4) for the KMS server
