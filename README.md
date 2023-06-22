<h1> Chest-Xray-Web-App </h1>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Azure](https://img.shields.io/badge/azure-%230072C6.svg?style=for-the-badge&logo=microsoftazure&logoColor=white)
![MicrosoftSQLServer](https://img.shields.io/badge/Microsoft%20SQL%20Server-CC2927?style=for-the-badge&logo=microsoft%20sql%20server&logoColor=white)

<!-- ![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white) -->



<h2> 1. Project Description </h2>
This app serves as an web app for registering patient's profile, uploading medical images, and storing and displaying AI model's results. 

The web app involves multiple technologies including artificial intelligence, cloud computing, and web development. 

<h2> 2. System design and main elements </h2>
<h3> 2.1. Tech stack</h3>

```
    Tech stack:
    ├── Cloud: Azure
    ├── Database: Azure SQL Server
    └── Web Development: 
        ├── Front-end: HTML, CSS 
        └── Back-end: Django
```

<h3> 2.2. Design Pattern: Model - View - Template </h3>
<h3> 2.3. Project Structure </h3>

<pre>
    <b>Chest-Xray-Web-App </b>
    ├── <b>media </b>
    │   ├── <b>input_images </b>                            (Directory for local storage of uploaded medical images)
    │   ├── <b>output_images </b>                           (Directory for local storage of resultant medical images)
    │   ├── <b>profile_images </b>                          (Directory for local storage of avatar images)
    │   └── ...
    ├── <b>user_management </b>                             (General settings of this project)
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── <b>user </b>                                        (Chest X-ray Web Application)
    │   ├── <b>azure_dl </b>                                (Module for Azure cloud configuration)
    │   │   ├── <b>config </b>                              
    │   │   │   ├── config_reader.py
    │   │   │   └── config.ini
    │   │   ├── <b>connectors </b>
    │   │   │   └── azure_dl.py
    │   │   ├── <b>src </b>
    │   │   │   └── azure_dl_engine.py
    │   │   ├── sample_download_script.py
    │   │   └── sample_upload_script.py
    │   ├── <b>config_dl_vm </b>                            (Azure Data lake and virtual machine configuration)
    │   │   └── config_dl_vm.json
    │   ├── <b>migrations </b>                              (Tracks of database changes)
    │   ├── <b>templates </b>                               (HTML templates)
    │   │   ├── base.html                                   (Base template)
    │   │   ├── change_password.html
    │   │   ├── home.html                                   (Home template)
    │   │   ├── login.html                                  (Login template)
    │   │   ├── logout.html
    │   │   ├── news_1.html
    │   │   ├── news_2.html
    │   │   ├── news_3.html
    │   │   ├── password_reset_complete.html 
    │   │   ├── password_reset_confirm.html
    │   │   ├── password_reset_email.html
    │   │   ├── password_reset_subject.html
    │   │   ├── password_reset.html
    │   │   ├── prediction_confirm_delete.html
    │   │   ├── prediction_form.html                        (Prediction create template)
    │   │   ├── prediction_submit_success.html
    │   │   ├── prediction_view.html                        (Prediction detail template)
    │   │   ├── prediction.html                             (Prediction history template)
    │   │   ├── profile.html                                (Patient's profile template)
    │   │   ├── register.html                               (Register template)
    │   │   └── test.html
    │   ├── __init__.py
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py                                        (Forms)
    │   ├── models.py                                       (Model module)
    │   ├── signals.py
    │   ├── urls.py                                         (URL list)
    │   └── views.py                                        (Control/Logic module)
    ├── manage.py
    ├── README.md
    └── requirements.txt
</pre>

<h2> 3. Usage <h2>

### 3.1. Access home page
    Click sign in/ sign up button on navigation bar.

### 3.2. Create account in register page
    Input user name, email, and password.

### 3.3. Register patients profile in profile page
    Input biography and upload avatar.

### 3.4. Upload an image in make_prediction page
    Upload image file and choose modality type.

### 3.5. View a list of complete/ incomplete prediction in prediction_history page
    Click on prediction history button on navigation bar.

### 3.6. View predicted image and corresponding diseases in prediction_view page
    Click on view button on the right of each input image on prediction_history page to view the predicted image and disease predictions.  


## 4. Installation and Running
### 4.1. Manual method

Clone the project from github
```
    git clone https://github.com/DatacollectorVN/Chest-Xray-Web-App.git
```

Install conda environment and required dependencies:
```
    conda create -n myenv python=3.8
    conda activate myenv
    pip install -r requirements.txt
```

Move to the project's directory and run
```
    cd Chest-Xray-Web-App
    python manage.py check
    python manage.py runserver
```

Type in browser search bar
```
    http://127.0.0.1:8000/
```

### 4.2. Docker Image

Pull Docker Image
```
    docker pull kosnhan/t_app:latest
```

Run Docker Image
```
    docker run -p 8001:8000 kosnhan/t_app:latest
```

Type in browser search bar
```
    http://127.0.0.1:8001/
```

## 5. Hosting
Updating