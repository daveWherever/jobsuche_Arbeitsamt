import requests
import base64
import pandas as pd
from datetime import date, timedelta

# GitHub: https://github.com/bundesAPI/jobsuche-api

columns = ['beruf', 'titel', 'arbeitgeber',
   'aktuelleVeroeffentlichungsdatum', 'arbeitsort.plz',
   'arbeitsort.ort', 'arbeitsort.region', 'arbeitsort.land',
   'arbeitsort.entfernung', 'externeUrl', 'arbeitsort.strasse']

date_today = date.today()
def get_jwt():
    """fetch the jwt token object"""
    headers = {
        'User-Agent': 'Jobsuche/2.9.2 (de.arbeitsagentur.jobboerse; build:1077; iOS 15.1.0) Alamofire/5.4.4',
        'Host': 'rest.arbeitsagentur.de',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }

    data = {
      'client_id': 'c003a37f-024f-462a-b36d-b001be4cd24a',
      'client_secret': '32a39620-32b3-4307-9aa1-511e3d7f48a8',
      'grant_type': 'client_credentials'
    }

    response = requests.post('https://rest.arbeitsagentur.de/oauth/gettoken_cc', headers=headers, data=data, verify=False)

    return response.json()

def search(jwt, what, where):
    """search for jobs. params can be found here: https://jobsuche.api.bund.dev/"""
    params = (
        ('angebotsart', '1'),
        ('page', '1'),
        ('pav', 'false'),
        ('size', '200'),
        ('umkreis', '25'),
        ('was', what),
        ('wo', where)
    )

    headers = {
        'User-Agent': 'Jobsuche/2.9.2 (de.arbeitsagentur.jobboerse; build:1077; iOS 15.1.0) Alamofire/5.4.4',
        'Host': 'rest.arbeitsagentur.de',
        'OAuthAccessToken': jwt,
        'Connection': 'keep-alive',
    }

    response = requests.get('https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v4/app/jobs',
                            headers=headers, params=params, verify=False)
    return response.json(), what, where


def job_details(jwt, job_ref):

    headers = {
        'User-Agent': 'Jobsuche/2.9.3 (de.arbeitsagentur.jobboerse; build:1078; iOS 15.1.0) Alamofire/5.4.4',
        'Host': 'rest.arbeitsagentur.de',
        'OAuthAccessToken': jwt,
        'Connection': 'keep-alive',
    }

    response = requests.get(
        f'https://rest.arbeitsagentur.de/jobboerse/jobsuche-service/pc/v2/jobdetails/{(base64.b64encode(job_ref.encode())).decode("UTF-8")}',
        headers=headers, verify=False)

    return response.json()

def jobs_config(was, wo):
    jwt = get_jwt()
    result = search(jwt["access_token"], was, wo)
    reff = pd.json_normalize(result[0]['stellenangebote'])
    df = pd.DataFrame(data=reff, columns=columns)

    df["aktuelleVeroeffentlichungsdatum"] = pd.to_datetime(df["aktuelleVeroeffentlichungsdatum"])
    df_date = df[(df["aktuelleVeroeffentlichungsdatum"] == pd.to_datetime(date_today - timedelta(1)))]

    return df_date

def job_loop():
    df_merge = pd.DataFrame()

    jobs = ["machine learning", "data science", "ai", "ki", "deep learning"]
    for job in jobs:
        df_merge = pd.concat([df_merge, jobs_config(job, "Stuttgart")], ignore_index=True)

    # df_merge.to_csv(f"01_data/{date_today}_jobs.csv")

    return df_merge
