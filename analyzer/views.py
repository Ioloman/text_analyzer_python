import json
from typing import Dict
from django.shortcuts import render
from analyzer.analyzer_class import calculate_compatibility, Thesaurus


def index(request):
    return render(request,
                  'html/index.html')


def analize_one(request):
    return render(request,
                  'html/analysis_one_material/analysis.html')


def analize_two(request):
    return render(request,
                  'html/analysis_two_materials/analysis.html')


def result_analize_one(request):
    return render(request,
                  'html/analysis_one_material/result.html')


def result_analize_two(request):

    one_material_name = request.POST.get('one_material_name', '')
    one_text_area = request.POST.get('one_text_area', '')
    one_uploaded_file = request.FILES.get('one_uploaded_file', None)

    two_material_name = request.POST.get('two_material_name', '')
    two_text_area = request.POST.get('two_text_area', '')
    two_uploaded_file = request.FILES.get('two_uploaded_file', None)

    thesaurus = Thesaurus()

    one_data: Dict[str: float] = thesaurus(one_uploaded_file if one_uploaded_file else one_text_area)
    two_data: Dict[str: float] = thesaurus(two_uploaded_file if two_uploaded_file else two_text_area)

    compatibility = calculate_compatibility(list(one_data.keys()), list(two_data.keys()))

    if not list(one_data) and not list(two_data):
        return render(request, 'html/analysis_two_materials/analysis.html',
                      {'one_material_name': one_material_name,
                       'two_material_name': two_material_name,
                       'one_text_area': one_text_area,
                       'two_text_area': two_text_area,
                       'notification': "alert('Оба текста слишком короткие.')"}
                      )

    json_data = json.dumps([[(key, val) for key, val in one_data.items()], [(key, val) for key, val in two_data.items()]])

    js_code = f"alert('Текст \"{one_material_name if not one_data else two_material_name}\" слишком мал для определения тезауруса')" if not one_data or not two_data else ""

    return render(request,
                  'html/analysis_two_materials/result.html', context={'one_material_name': one_material_name,
                                                                      'two_material_name': two_material_name,
                                                                      'one_data': one_data,
                                                                      'two_data': two_data,
                                                                      'result': compatibility,
                                                                      'json_data': json_data,
                                                                      'notification': js_code})
