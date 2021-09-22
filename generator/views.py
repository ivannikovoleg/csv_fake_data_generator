from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from celery.result import AsyncResult
from .models import Schema, DataSet
from .tasks import create_csv
import json
import time


def index(request):
    return render(request, 'generator/index.html')


@login_required
def generate(request):
    if request.method == 'GET':
        return render(request, 'generator/generate.html')
    elif request.method == "POST":
        r_dict = dict(request.POST.lists())
        tmp_dict = {'schema_name': r_dict['schema_name'][0]}
        del r_dict['schema_name']
        del r_dict['csrfmiddlewaretoken']
        zp = list(zip(r_dict['order'], r_dict['column_name'], r_dict['type'], r_dict['from'], r_dict['to']))
        for i in range(len(r_dict['column_name'])):
            tmp_dict[r_dict['order'][i]] = zp[i]
        schema = Schema()
        schema.schema_name = request.POST['schema_name']
        schema.schema_json = json.dumps(tmp_dict)
        schema.owner = request.user
        schema.save()
        return render(request, 'generator/generate.html')


@login_required()
def schemas(request):
    schema = Schema.objects.filter(owner=request.user)
    data_sets = DataSet.objects.filter(schema=schema)
    context = {
        'schemas': schema,
        'data_sets': data_sets,
    }
    return render(request, 'generator/schemas.html', context)


@login_required
def schema_view(request, pk):
    if request.method == 'GET':
        schema = Schema.objects.get(id=pk)
        name = schema.schema_name
        schema_json = json.loads(schema.schema_json)
        print(type(schema_json))
        del schema_json['schema_name']
        for i in schema_json.values():
            print(i)

        context = {'schema_name': name, 'schema_json': schema_json.values()}
        if schema.owner != request.user:
            raise Http404
        return render(request, 'generator/schema_view.html', context)

    elif request.method == "POST":
        r_dict = dict(request.POST.lists())
        tmp_dict = {'schema_name': r_dict['schema_name'][0]}
        del r_dict['schema_name']
        del r_dict['csrfmiddlewaretoken']
        zp = list(zip(r_dict['order'], r_dict['column_name'], r_dict['type'], r_dict['from'], r_dict['to']))
        for i in range(len(r_dict['column_name'])):
            tmp_dict[r_dict['order'][i]] = zp[i]
        schema = Schema.objects.get(id=pk)
        schema.schema_name = request.POST['schema_name']
        schema.schema_json = json.dumps(tmp_dict)
        schema.owner = request.user
        schema.save()
        return redirect('generator:schemas')


@login_required
def create_file(request, pk):
    if request.method == 'GET':
        schema = Schema.objects.get(id=pk)
        name = schema.schema_name
        data_sets = DataSet.objects.filter(schema=schema).order_by('-uploaded_at')
        context = {'schema_name': name, 'data_sets': data_sets}
        if schema.owner != request.user:
            raise Http404
        return render(request, 'generator/create_file.html', context)
    elif request.method == 'POST':
        rows_number = dict(request.POST.lists())['rows-number'][0]
        file_name = f'file-{str(time.time())}.csv'
        url = f'https://csv-static-files.s3.amazonaws.com/{file_name}'
        print(rows_number)

        schema = Schema.objects.get(id=pk)

        schema_json = json.loads(schema.schema_json)
        print(type(schema_json))
        task = create_csv.delay(schema_json, int(rows_number), file_name)
        print(task.task_id)
        # task = create_csv.apply_async(queue='high_priority', args=(schema_json, int(rows_number)))
        # res = task.collect()
        # print(list(res))
        # print(res[0])
        data_set = DataSet.objects.create(url=url, schema=schema, owner=request.user)
        context = {'task_id': task.task_id}

        return render(request, 'generator/progress.html', context)


@login_required
def delete_schema(request, pk):
    if request.method == 'GET':
        schema = Schema.objects.get(id=pk)
        name = schema.schema_name
        context = {'schema_name': name}
        if schema.owner != request.user:
            raise Http404
        return render(request, 'generator/delete.html', context)
    elif request.method == 'POST':
        schema = Schema.objects.get(id=pk)
        schema.delete()
        return redirect('generator:schemas')

@login_required
def data_set_list(request, pk):
    if request.method == 'GET':
        schema = Schema.objects.get(id=pk)
        name = schema.schema_name
        data_sets = DataSet.objects.filter(schema=schema).order_by('-uploaded_at')
        context = {'schema_name': name, 'data_sets': data_sets}
        if schema.owner != request.user:
            raise Http404
        return render(request, 'generator/data_set_list.html', context)
