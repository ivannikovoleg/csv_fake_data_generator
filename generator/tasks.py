import boto3
from csv_data_generator.celery import app
from faker import Faker
import csv
import os
from csv_data_generator import settings
from celery import shared_task
from celery_progress.backend import ProgressRecorder


def fake_data(a, from_range='18', to_range='100'):
    f = Faker()
    if a == 'name':
        return f.name()
    elif a == 'job':
        return f.job()
    elif a == 'email':
        return f.email()
    elif a == 'phone':
        return f.msisdn()
    elif a == 'company':
        return f.company()
    elif a == 'text':
        return f.text()
    elif a == 'integer':
        if from_range != '' and to_range != '':
            return f.random_int(int(from_range), int(to_range))
        else:
            return f.random_int(18, 100)
    elif a == 'address':
        return f.address()


def aws_session():
    return boto3.session.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                 )


def upload_file_to_bucket(bucket_name, file_path):
    session = aws_session()
    s3_resource = session.resource('s3')
    file_dir, file_name = os.path.split(file_path)

    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(
        Filename=file_path,
        Key=file_name,
        ExtraArgs={'ACL': 'public-read'}
    )

    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name}"
    return s3_url


# @shared_task(bind=True)
@app.task(bind=True)
def create_csv(self, d: dict, rows, file_name):
    progress_recorder = ProgressRecorder(self)
    del d['schema_name']
    col_names = []

    data_types = {}
    for v in d.values():
        col_names.append(v[1])
        data_types[v[1]] = [v[2], v[3], v[4]]
    print(data_types)
    with open(file_name, 'w', newline="") as file:
        writer = csv.DictWriter(file, fieldnames=col_names)
        writer.writeheader()
        for i in range(rows):
            user_data = {
                col_name: fake_data(data_types[col_name][0],
                                    data_types[col_name][1],
                                    data_types[col_name][2]) for col_name in col_names}
            writer.writerow(user_data)
            progress_recorder.set_progress(i + 1, rows, f'On row: {i}')
    upload_file_to_bucket(settings.AWS_STORAGE_BUCKET_NAME, file_name)

    return "Done!"
