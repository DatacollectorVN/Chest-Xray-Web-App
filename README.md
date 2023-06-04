# Chest-Xray-Web-App


User guide:

## Install Python 3.8 and required packages.
''' 
conda create -n myenv python=3.8
conda activate myenv
pip install -r requirements.txt
'''



## Current work
27/05/2023
Modify html files for home page:
    1. Add image of BME school to homepage
    2. Add a page of technology introduction
    3. Understand code in HTML files

30/05/2023
1)	Add a new column to users_profile
    1.1)	Bio2: TextField
    -> Add Bio2 to TextField: Problem: not understand why my change work without making a migration.

    1.2)	Add a new table: disease_prediction (primarykey: id, foregnkey: user_id (auth_user: not create constraint)), category: x_ray, …, url: link of image-> real image saves in datalake)

2)	Create a new page html, prediction.html
    2.1) Button for loading image (temporarily saved at local)
    2.2) How to get user_id (show on html) 

3)	Create user_id directory under profile_images dir
    profile_images/ 
        —user_id_1/
            avatar.png 
        —user_id_2/
            avatar.png
    (lưu đè tên)

    Problem: avatar_dfsidfsd.png after resize:
        check resize and save function.

4)  Commit to a new branch called tran/dev -> Done
    

